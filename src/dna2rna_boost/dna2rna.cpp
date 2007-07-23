#include "dnalist.hpp"
#include <vector>
#include <string>
#include <sstream>
#include <iostream>

class tmpl
{
public:
	tmpl(std::string s="", int l=-1, int n=-1) : s(s), l(l), n(n) {}
	std::string s;
	int l;
	int n;
};

typedef std::vector<tmpl> tvec;

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
    
std::string constsrec(DNAList& dna)
{
	char d = dna[0];		
	if (d == 'C')
	{
		dna.popfront(1);
		std::string seq = constsrec(dna);
		seq.push_back('I');
		return seq;
	}
	else if (d == 'F')
	{
		dna.popfront(1);
		std::string seq = constsrec(dna);
		seq.push_back('C');
		return seq;
	}
	else if (d == 'P')
	{
		dna.popfront(1);
		std::string seq = constsrec(dna);
		seq.push_back('F');
		return seq;
	}
	else if (d == 'I' && dna[1] == 'C')
	{
		dna.popfront(2);
		std::string seq = constsrec(dna);
		seq.push_back('P');
		return seq;
	}
	else
	{
		return "";
	}
}

std::string consts(DNAList& dna)
{
	std::string s = constsrec(dna);
	std::reverse(s.begin(), s.end());
	return s;
}


void patternfcn(DNAList& dna, svec& rna, svec& p)
{
	unsigned int lvl = 0;
		//std::cout << "Pattern " << dna.size() << std::endl;
    for (;;)
	{
		char d = dna[0];
        if (d == 'C')
		{
            dna.popfront(1);
            p.push_back("I");
		}
        else if (d == 'F')
		{
            dna.popfront(1);
            p.push_back("C");
		}
        else if (d == 'P')
		{
            dna.popfront(1);
            p.push_back("F");
		}
        else if (d == 'I')
        {
        	d = dna[1];
        	if (d == 'C')
			{
	            dna.popfront(2);
	            p.push_back("P");
			}
	        else if (d == 'P')
			{
	            dna.popfront(2);
	            int n = nat(dna);
				std::stringstream str;
				str << "!" << n;
				std::string s = str.str();
	            p.push_back(s);
			}
	        else if (d == 'F')
			{
	            dna.popfront(3); // NOTE: Three bases consumed here.
				std::string s("?");
				s.append(consts(dna));
				p.push_back(s);
			}
	        else if (d == 'I')
	        {
	        	d = dna[2];
	        	if  (d == 'P')
				{
		            dna.popfront(3);
		            ++lvl;
		            p.push_back("(");
				}
				else if (d == 'C' || d == 'F')
				{
		            dna.popfront(3);
		            if (lvl > 0)
					{
		                --lvl;
		                p.push_back(")");
					}
		            else
					{
		                break;
					}
				}
		        else if (d == 'I')
				{
					std::string rnacmd = dna.getstr(3, 10);
		            dna.popfront(10);
					rna.push_back(rnacmd);
				}
	        }
        }
	}
	//std::cout << "Pattern " << dna.size() << std::endl;
}


void templatefcn(DNAList& dna, svec& rna, tvec& t)
{
    for (;;)
	{
		char d = dna[0];
        if (d == 'C')
		{
            dna.popfront(1);
            t.push_back(tmpl("I"));
		}
        else if (d == 'F')
		{
            dna.popfront(1);
            t.push_back(tmpl("C"));
		}
        else if (d == 'P')
		{
            dna.popfront(1);
            t.push_back(tmpl("F"));
		}
        else if (d == 'I')
        {
        	d = dna[1];
        	if (d == 'C')
			{
	            dna.popfront(2);
	            t.push_back(tmpl("P"));
			}
	        else if (d == 'P' || d == 'F')
			{
	            dna.popfront(2);
	            int l = nat(dna);
	            int n = nat(dna);
	            t.push_back(tmpl("", l, n));
			}
	        else if (d == 'I')
	        {
	        	d = dna[2];
	        	if (d == 'P')
				{
		            dna.popfront(3);
		            int n = nat(dna);
					t.push_back(tmpl("", -1, n));
				}
				else if (d == 'C' || d == 'F')
				{
		            dna.popfront(3);
					break;
				}
		        else if (d == 'I')
				{
					std::string rnacmd = dna.getstr(3, 10);
		            dna.popfront(10);
					rna.push_back(rnacmd);
				}
	        }
        }
	}
	//std::cout << "Template" << dna.size() << std::endl;
}

dnaseq asnat(int n)
{
    dnaseq d;
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
    return d;
}


dnaseq quote(dnaseq& d)
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
	}
	return nd;
}


void protect(int l, dnaseq& d)
{
	if (l > 0)
	{
		while (l > 0)
		{
			d = quote(d);
			l -= 1;
		}
	}
}
        
void replacefcn(DNAList& dna, const tvec& tpl, evec& e, size_t i)
{
    dnainsertlist r;
    for (tvec::const_iterator it = tpl.begin(); it != tpl.end(); ++it)
    {
    	const tmpl& t =*it; 
    	if (!t.s.empty())
    	{
            // Base
          	dnaseqptr d(new dnaseq);
        	for (size_t ix = 0; ix < t.s.size(); ++ix)
        	{
        		d->push_back(t.s[ix]);
        	}
            r.push_back(new DNARef(0, d->size(), d));
    	}
    	else if (t.l == -1)
        {
            // |n|
            if (t.n >= e.size())
            {
            	dnaseqptr d(new dnaseq);
            	*d = asnat(0);
                r.push_back(new DNARef(0, d->size(), d));
            }
            else
            {
            	dnaseqptr d(new dnaseq);
            	*d = asnat(0);
                r.push_back(new DNARef(0, d->size(), d));
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
                	std::pair<size_t, size_t>& a = e[t.n];
                	r.push_back(new DNARefEmpty(a.first, a.second));
                }
                else
                {
                	dnaseq tmp;
                	std::pair<size_t, size_t>& a = e[t.n];
	            	for (size_t ix = a.first; ix < a.second; ++ix)
	            	{
	            		tmp.push_back(dna[ix]);
	            	}
	            	protect(t.l, tmp);
	            	dnaseqptr d(new dnaseq(tmp));	            	
	                r.push_back(new DNARef(0, d->size(), d));
                }
            }
		}
    }
        
    size_t rsz = 0;
    for (dnainsertlist::iterator it = r.begin(); it != r.end(); ++it)
    {
    	size_t sz = (*it)->size();
    	rsz += sz;
    	//std::cout << sz << std::endl; 
    }
    //std::cout << "length before " << dna.size() << " pop " << i << " adding " << rsz << std::endl; 
    dna.insertfrontreflistandpopold(r, i);
}

    


void matchreplace(DNAList& dna, const svec& pat, tvec& t)
{
    evec e;
    ivec c;
    size_t i = 0;
//    std::cout << "Pattern: ";
//    for (svec::const_iterator it = pat.begin(); it != pat.end(); ++it)
//	{
//		std::string p = *it;
//		std::cout << p;
//	}
//	std::cout << std::endl;
//    std::cout << "Template: ";
//    for (tvec::const_iterator it = t.begin(); it != t.end(); ++it)
//	{
//		tmpl tt = *it;
//		std::cout << tt.s << " " << tt.l << " " << tt.n;
//	}	
//	std::cout << std::endl;
    for (svec::const_iterator it = pat.begin(); it != pat.end(); ++it)
	{
		std::string p = *it;
        if (p[0] == '!')
		{
            int n = atoi(p.substr(1).c_str());
            i += n;
            if (i > dna.size())
			{
				// Match failed.
                return;
			}
		}
        else if (p[0] == '?')
		{
			std::string substr = p.substr(1);
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
        else if (p[0] == '(')
		{
            c.push_back(i);
		}
        else if (p[0] == ')')
		{
//			std::cout << "e[" << e.size() << "] ";
//			for (size_t ix = c.back(); ix < std::min(c.back()+10, i) ; ++ix)
//			{
//				std::cout << dna[ix];
//			}
//			 std::cout << std::endl;
            e.push_back(std::make_pair(c.back(), i));
			c.pop_back();
		}
        else
		{
            // Base
            if (dna[i] == p[0])
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
    
  

    
void execute(DNAList& dna, svec& rna, bool progress = false)
{
    unsigned int n = 0;
    for (;;)
	{
        ++n;
		svec p;
		tvec t;
		try
		{
			patternfcn(dna, rna, p);
			templatefcn(dna, rna, t);
			matchreplace(dna, p, t);
			if (progress)
			{
				std::cout << "Iterations: " << n << " DNA remaining: " << dna.size() << " RNA commands: " << rna.size() << std::endl;
				for (size_t i = 0; i < 10; ++i)
				{
					std::cout << dna[i];
				}
				std::cout << std::endl;
			}
		}
		catch(...)
		{
			std::cout << "Finished!" << std::endl;
			break;
		}
	}
}

