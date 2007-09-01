#include "dnalist.hpp"
#include "dna2rna.hpp"
#include <vector>
#include <string>
#include <sstream>
#include <iostream>

bool dna_debug = false;
unsigned int dna_skip = 1;

std::ostream& operator<< (std::ostream& s, const ptn& p)
{
	return p.print(s);
}


int nat(DNAList& dna)
{
	char d = dna[0];
    dna.popfront(1);
    if (d == 'P')
	{
        return 0;
	}
    else if (d == 'I' || d == 'F')
	{
        return 2 * nat(dna);
	}
    else if (d == 'C')
	{
        return 1 + 2 * nat(dna);
	}
}    

void consts(DNAList& dna, std::string& seq)
{
    while (1)
	{
		std::string dnastr;
		dna.get<std::string>(dnastr, 0u, 2u);
        char d = dnastr[0];
		if (d == 'C')
		{
			dna.popfront(1);
            seq.push_back('I');
		}
		else if (d == 'F')
		{
			dna.popfront(1);
            seq.push_back('C');
		}
		else if (d == 'P')
		{
			dna.popfront(1);
            seq.push_back('F');
		}
		else if (d == 'I')
		{
			d = dnastr[1];
			if (d == 'C')
			{
				dna.popfront(2);
				seq.push_back('P');
			}
			else
			{
				return;
			}
		}
	}
}


void patternfcn(DNAList& dna, svec& rna, pvec& p)
{
	unsigned int lvl = 0;
    for (;;)
	{
		char d = dna[0];
        if (d == 'C')
		{
            dna.popfront(1);
            p.push_back(new ptnbase('I'));
		}
        else if (d == 'F')
		{
            dna.popfront(1);
            p.push_back(new ptnbase('C'));
		}
        else if (d == 'P')
		{
            dna.popfront(1);
            p.push_back(new ptnbase('F'));
		}
        else if (d == 'I')
        {
        	d = dna[1];
        	if (d == 'C')
			{
	            dna.popfront(2);
	            p.push_back(new ptnbase('P'));
			}
	        else if (d == 'P')
			{
	            dna.popfront(2);
	            int n = nat(dna);
	            p.push_back(new ptnskip(n));
			}
	        else if (d == 'F')
			{
	            dna.popfront(3); // NOTE: Three bases consumed here.
				std::string s;
				consts(dna, s);
				p.push_back(new ptnfind(s));
			}
	        else if (d == 'I')
	        {
	        	d = dna[2];
	        	if  (d == 'P')
				{
		            dna.popfront(3);
		            ++lvl;
		            p.push_back(new ptnparen(ptn::LPAREN));
				}
				else if (d == 'C' || d == 'F')
				{
		            dna.popfront(3);
		            if (lvl > 0)
					{
		                --lvl;
		                p.push_back(new ptnparen(ptn::RPAREN));
					}
		            else
					{
		                break;
					}
				}
		        else if (d == 'I')
				{
					std::string rnacmd;
					dna.get<std::string>(rnacmd, 3, 10);
		            dna.popfront(10);
					rna.push_back(rnacmd);
				}
	        }
        }
	}
}


void templatefcn(DNAList& dna, svec& rna, tvec& t)
{
    for (;;)
	{
		char d = dna[0];
        if (d == 'C')
		{
            dna.popfront(1);
            t.push_back(tmpl('I'));
		}
        else if (d == 'F')
		{
            dna.popfront(1);
            t.push_back(tmpl('C'));
		}
        else if (d == 'P')
		{
            dna.popfront(1);
            t.push_back(tmpl('F'));
		}
        else if (d == 'I')
        {
        	d = dna[1];
        	if (d == 'C')
			{
	            dna.popfront(2);
	            t.push_back(tmpl('P'));
			}
	        else if (d == 'P' || d == 'F')
			{
	            dna.popfront(2);
	            int l = nat(dna);
	            int n = nat(dna);
	            t.push_back(tmpl(0, l, n));
			}
	        else if (d == 'I')
	        {
	        	d = dna[2];
	        	if (d == 'P')
				{
		            dna.popfront(3);
		            int n = nat(dna);
					t.push_back(tmpl(0, -1, n));
				}
				else if (d == 'C' || d == 'F')
				{
		            dna.popfront(3);
					break;
				}
		        else if (d == 'I')
				{
					std::string rnacmd;
					dna.get<std::string>(rnacmd, 3, 10);
		            dna.popfront(10);
					rna.push_back(rnacmd);
				}
	        }
        }
	}
}

void asnat(dnaseq& d, int n)
{
    while (n > 0)
	{
        if ((n % 2) == 0)
		{
            d.push_back('I');
		}
        else
		{
            d.push_back('C');
		}
        n /= 2;
	}
    d.push_back('P');
}


void quote(dnaseq& d)
{
	dnaseq nd;
	dnaseq::iterator it = d.begin();
    while (it != d.end())
	{
        if (*it == 'I')
		{
            nd.push_back('C');
		}
        else if (*it == 'C')
		{
			nd.push_back('F');
		}
        else if (*it == 'F')
		{
            nd.push_back('P');
		}
        else
		{
            // P
            nd.push_back('I');
            nd.push_back('C');
		}
		++it;
	}
	d.clear();
	std::copy(nd.begin(), nd.end(), std::back_inserter(d));
}


void protect(int l, dnaseq& d)
{
	if (l > 0)
	{
		while (l > 0)
		{
			quote(d);
			l -= 1;
		}
	}
}
        
void replacefcn(DNAList& dna, const tvec& tpl, evec& e, size_t i)
{
    dnareflist r;
	dnaseq* d = 0;
    for (tvec::const_iterator it = tpl.begin(); it != tpl.end(); ++it)
    {
    	const tmpl& t =*it; 
    	if (t.c != 0)
    	{
            // Base
			if (d == 0)
			{
				d = dna.allocate();
			}
			d->push_back(t.c);
		}
    	else if (t.l == -1)
        {
            // |n|
            if (t.n >= e.size())
            {
				if (d == 0)
				{
					d = dna.allocate();
				}
            	asnat(*d, 0);
			}
			else
			{
				if (d == 0)
				{
					d = dna.allocate();
				}
				std::pair<size_t, size_t>& a = e[t.n];
                asnat(*d, a.second-a.first);
            }
        }
        else
		{
            // n(l)
            if (t.n >= e.size())
            {
            	;
            }
            else
            {
                if (t.l == 0)
                {
					if (d)
					{
						r.push_back(new DNARef(0, d->size(), d));
						d = 0;
					}
                	std::pair<size_t, size_t>& a = e[t.n];
					dnareflist rl;
					dna.getreflist(rl, a.first, a.second);
					std::copy(rl.begin(), rl.end(), std::back_inserter(r));
                }
                else
                {
                	std::pair<size_t, size_t>& a = e[t.n];
					if (d)
					{
						r.push_back(new DNARef(0, d->size(), d));
					}
					d = dna.allocate();
					dna.get<dnaseq>(*d, a.first, a.second);
	            	protect(t.l, *d);
                }
            }
		}
    }
	if (d)
	{
		r.push_back(new DNARef(0, d->size(), d));
	}
    
	dna.popfront(i);
    dna.insertfront(r);
}

    


void matchreplace(DNAList& dna, const pvec& pat, tvec& t)
{
    evec e;
    ivec c;
    size_t i = 0;
	if (dna_debug)
	{
		std::cout << "pattern ";
		for (pvec::const_iterator it = pat.begin(); it != pat.end(); ++it)
		{
			ptn* p = *it;
			std::cout << *p;
		}
		std::cout << std::endl;
		std::cout << "template ";
		for (tvec::const_iterator it = t.begin(); it != t.end() && it != t.begin()+10; ++it)
		{
			tmpl tt = *it;
			if (tt.n == -1 && tt.l == -1)
			{
				std::cout << tt.c;
			}
			else
			{
				std::cout << "(" << tt.l << "," << tt.n << ")";
			}
		}	
		std::cout << "..." << std::endl;
	}
    for (pvec::const_iterator it = pat.begin(); it != pat.end(); ++it)
	{
		ptn* p = *it;
        if (p->t == ptn::SKIP)
		{
            i += static_cast<ptnskip*>(p)->n;
            if (i > dna.size())
			{
				// Match failed.
                return;
			}
		}
        else if (p->t == ptn::FIND)
		{
			std::string& substr = static_cast<ptnfind*>(p)->str;
            size_t n = dna.find(substr, i);
            if (n >= 0)
			{
                i = n + substr.size();
			}
            else
			{
                // Match failed.
                return;
			}
		}
        else if (p->t == ptn::LPAREN)
		{
            c.push_back(i);
		}
        else if (p->t == ptn::RPAREN)
		{
			if (dna_debug)
			{
				std::cout << "e[" << e.size() << "] ";
				for (size_t ix = c.back(); ix < std::min(c.back()+10, i) ; ++ix)
				{
					std::cout << dna[ix];
				}
				std::cout << "... (" << i - c.back() << " bases)" << std::endl;
			}
            e.push_back(std::make_pair(c.back(), i));
			c.pop_back();
		}
        else
		{
            // Base
            if (dna[i] == static_cast<ptnbase*>(p)->b)
			{
                i += 1;
			}
            else
			{
                // Match failed.
                return;
			}
		}
	}
    replacefcn(dna, t, e, i);
}
    
  
void progress(DNAList& dna, svec& rna, unsigned int n)
{
	if (n % dna_skip == 0)
	{
		std::cout << "iteration " << n << std::endl;
		size_t sz = dna.size();
		std::cout << "dna = ";
		for (size_t i = 0; i < std::min(10u, sz); ++i)
		{
			std::cout << dna[i];
		}
		std::cout << "... (" << sz << " bases)" << std::endl;
		std::cout << "len(rna) == " << rna.size() << std::endl;
	}
}
    
void execute(DNAList& dna, svec& rna, bool prog, int iterations)
{
    unsigned int n = 0;
	if (prog)
	{
		progress(dna, rna, n);
	}
    for (;;)
	{
        ++n;
		pvec p;
		tvec t;
		try
		{
			patternfcn(dna, rna, p);
			templatefcn(dna, rna, t);
			matchreplace(dna, p, t);
			if (prog)
			{
				progress(dna, rna, n);
			}
			pvec::iterator end = p.end();
			for (pvec::iterator it = p.begin(); it != end; ++it)
			{
				delete *it;
			}
			if (iterations == n)
			{
				break;
			}
		}
		catch(int)
		{
			if (prog)
			{
				progress(dna, rna, n);
			}
			pvec::iterator end = p.end();
			for (pvec::iterator it = p.begin(); it != end; ++it)
			{
				delete *it;
			}
			std::cout << "Finished!" << std::endl;
			break;
		}
	}
}

