// dna2rna_c.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <string>

class DNARef
{
public:
	char* m_data;
	size_t m_start;
	size_t m_stop;

	DNARef(size_t start, size_t stop, char* data = 0) : m_start(start), m_stop(stop), m_data(data) {}

	size_t size() const
	{
		return m_stop - m_start;
	}
    
    void popfront(size_t num)
	{
        m_start += num;
	}
        
	char operator[](size_t ix) const
	{
		return m_data[m_start + ix];
	}

	char& operator[](size_t ix)
	{
		return m_data[m_start + ix];
	}        
};

typedef std::vector<DNARef> reflist;

class DNAList
{
public:
	reflist m_list; 

	DNAList() {}

	size_t size() const
	{
		size_t len = 0;
		for (reflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
		{
			len += (*it).size();
		}
		return len;
	}

    void flatten()
	{
		size_t tsz = size();
		char* data = new char[tsz];
		size_t i = 0;
		for (reflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
		{
			size_t sz = (*it).size();
			for (size_t ix = 0; ix < sz; ++ix)
			{
				data[i++] = (*it)[ix];
			}
		}
		DNARef r(0, tsz, data);
		m_list.clear();
		insertfront(r);
	}


    void popfront(size_t num=1)
	{
		size_t n = 0;
		for (reflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
		{
			size_t sz = (*it).size();
			if (num == sz)
			{
				++n;
				num = 0;
				break;
			}
			else if (num < sz)
			{
				break;
			}
			else
			{
				++n;
				num -= sz;
			}
		}
		if (n > 0)
		{
            m_list.erase(m_list.end()-n, m_list.end());
		}
		if (num > 0)
		{
			m_list.back().popfront(num);
		}
	}    

    void popfromitem(size_t num, size_t item)
	{
        if (num == 0)
		{
            return;
		}

        size_t n = 0;
        start = size()-item-1;

		size_t n = 0;
		for (int i = start; i >= 0; --i)
		{
			DNARef& r = m_list[i];
            lr = r.size();
            if (num == lr)
			{
                // exact match, pop this too
                m_list.erase(m_list.begin()+i, m_begin()+start+1);
                break;
			}
            else if (num < lr)
			{
                // popfront on item is needed
                if (n > 0)
				{
	                m_list.erase(m_list.begin()+i+1, m_begin()+start+1);
				}
                r.popfront(num);
                break;
			}
            else
			{
                ++n;
                num -= lr;
			}
		}
	}

	char&operator[](size_t ref) const
	{
		size_t ix = 0;
		for (reflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
		{
			size_t lr = (*it).size();
            if (ix + lr > ref)
			{
                return (*it)[ref-ix];
			}
			else
			{
				ix += lr;
			}
		}
	}

    def insertfrontreflistandpopold(self, reflist, pop):
        offs = 0
        oldlen = len(self.list)
        for r in reflist:   
            if not r.data:
                r.start+=offs				
                r.stop+=offs
            offs += len(r)	
            self.insertfront(r)
        ls = len(self.list)
        self.popfromitem(pop, ls-oldlen)
        self.lencache = None
        if ls > 1000:
            self.flatten()

    def insertfront(self, ref):
        if ref.data:
            self.list.append(ref)
            self.lencache = None
        else:
            tmpreflist = []
            ix = 0
            for r in reversed(self.list):
                lr = len(r)
                # skip
                if ix + lr <= ref.start:
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
                        start = r.start+ref.start-ix
                    else:
                        start = r.start
                    if ix + lr >= ref.stop:
                        stop = r.start+ref.stop-ix
                    else:
                        stop = r.stop
                    tmp = DNARef(start, stop, r.data)  
                    tmpreflist.append(tmp)
                if ix + lr >= ref.stop:
                    self.list.extend(reversed(tmpreflist))
                    self.lencache = None
                    return
                ix += lr
            print "Noooo"
        
    def find(self, substr, startpos):
        ls = len(substr)
        if ls == 0:
            return
        subpos = 0
        c = substr[subpos]
        findpos = 0
        i = startpos
        ix = 0
        for r in reversed(self.list):
            lr = len(r)
            if ix + lr < i:                
                pass
            else:
                while i - ix < lr:
                    if (r.data[r.start+i-ix] == c):
                        if (subpos == 0):
                            findpos = i 
                        subpos += 1
                        if (subpos == ls):
##                            print "Found", substr, "at:", findpos
                            return findpos
                        else:
                            c = substr[subpos]
                    elif (subpos > 0):
                        i = findpos
                        subpos = 0
                        c = substr[subpos]
                    i += 1
            ix += lr
        print "NOT FOUND!!!!!!!!"
        return -1
    

if __name__=="__main__":
    a = range(10)
    r = DNARef(0, len(a),a)
    dna = DNAList()
    dna.insertfront(r)    
    print "dna 1:", dna
    print
    for i in "qwertyuiopasdfghjkl":
        r = DNARef(0, 1,[i])
        dna.insertfront(r)
    print "dna 2:", dna
    print
    dna.insertfrontreflistandpopold([DNARef(2,5), DNARef(4,7), DNARef(0,1,['a']), DNARef(0,8), DNARef(4,7)], 18)    
    print "dna 3:", dna



class tmpl
{
public:
	tmpl(std::string s="", int l=-1, int n=-1) : s(s), l(l), n(n) {}
	std::string s;
	int l;
	int n;
};

typedef std::vector<char> vec;
typedef std::vector<size_t> ivec;
typedef std::vector<std::vector<char> > evec;
typedef std::vector<std::string> svec;
typedef std::vector<std::string>::const_iterator csveciter;
typedef std::vector<tmpl> tvec;
typedef std::vector<tmpl>::const_iterator ctveciter;
typedef std::vector<char>::iterator veciter;
typedef std::vector<char>::const_iterator cveciter;

void str2vec(std::string s, vec& v)
{
	for (size_t i = 0; i < s.size(); ++i)
	{
		v.push_back(s[i]);
	}
}


class DNAList
{
public:
	size_t m_offset;
	vec m_vec;



	DNAList(vec& v) : m_offset(0)
	{
		m_vec = v;
	}
        
	size_t size() const
	{
		return m_vec.size()+m_offset;
	}
    
    void popfront(size_t num=1)
	{
		m_offset += num;
	}

	char get(size_t ix) const
	{
		return m_vec.at(ix+m_offset);
	}

	std::string getstr(size_t start, size_t stop) const
	{
		std::string s;
		for (cveciter it = m_vec.begin()+start; it != m_vec.begin()+stop; ++it)
		{
			s.push_back(*it);
		}
		return s;
	}

	void getvec(vec& v, size_t start, size_t stop) const
	{
		v.assign(m_vec.begin()+start, m_vec.begin()+stop);
	}

    void insertfront(const vec& iterable)
	{
		m_vec.insert(m_vec.begin(), iterable.begin(), iterable.end());
	}

	size_t find(std::string substr, size_t i) const
	{
		size_t ls = substr.size();
        if (ls == 0)
		{
            return -1;
		}

        size_t ix = 0;

        for (size_t ii = m_offset + 1; ii < m_vec.size(); ++ii)
		{
            if (memcmp(&m_vec[ii], &substr[0], ls) == 0)
			{
				return ii - m_offset;
			}
		}
        return -1;
	}
private:
	DNAList();
};


int nat(DNAList& dna)
{
	char d = dna.get(0);
    dna.popfront();
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
	if (dna.get(0) == 'C')
	{
		dna.popfront();
		std::string seq = constsrec(dna);
		seq.push_back('I');
		return seq;
	}
	else if (dna.get(0) == 'F')
	{
		dna.popfront();
		std::string seq = constsrec(dna);
		seq.push_back('C');
		return seq;
	}
	else if (dna.get(0) == 'P')
	{
		dna.popfront();
		std::string seq = constsrec(dna);
		seq.push_back('F');
		return seq;
	}
	else if (dna.get(0) == 'I' && dna.get(1) == 'C')
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
    for (;;)
	{
        if (dna.get(0) == 'C')
		{
            dna.popfront();
            p.push_back("I");
		}
        else if (dna.get(0) == 'F')
		{
            dna.popfront();
            p.push_back("C");
		}
        else if (dna.get(0) == 'P')
		{
            dna.popfront();
            p.push_back("F");
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'C')
		{
            dna.popfront(2);
            p.push_back("P");
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'P')
		{
            dna.popfront(2);
            int n = nat(dna);
			std::stringstream str;
			str << "!" << n;
			std::string s = str.str();
            p.push_back(s);
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'F')
		{
            dna.popfront(3); // NOTE: Three bases consumed here.
			std::string s("?");
			s.append(consts(dna));
			p.push_back(s);
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'I' && dna.get(2) == 'P')
		{
            dna.popfront(3);
            ++lvl;
            p.push_back("(");
		}
		else if (dna.get(0) == 'I' && dna.get(1) == 'I' && (dna.get(2) == 'C' || dna.get(2) == 'F'))
		{
            dna.popfront(3);
            if (lvl > 0)
			{
                --lvl;
                p.push_back(")");
			}
            else
			{
                return;
			}
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'I' && dna.get(2) == 'P')
		{
			std::string rnacmd = dna.getstr(3, 10);
            dna.popfront(10);
			rna.push_back(rnacmd);
		}
	}
}


void templatefcn(DNAList& dna, svec& rna, tvec& t)
{
    for (;;)
	{
        if (dna.get(0) == 'C')
		{
            dna.popfront();
            t.push_back(tmpl("I"));
		}
        else if (dna.get(0) == 'F')
		{
            dna.popfront();
            t.push_back(tmpl("C"));
		}
        else if (dna.get(0) == 'P')
		{
            dna.popfront();
            t.push_back(tmpl("F"));
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'C')
		{
            dna.popfront(2);
            t.push_back(tmpl("P"));
		}
        else if (dna.get(0) == 'I' && (dna.get(1) == 'P' || dna.get(1) == 'F'))
		{
            dna.popfront(2);
            int l = nat(dna);
            int n = nat(dna);
            t.push_back(tmpl("", l, n));
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'I' && dna.get(2) == 'P')
		{
            dna.popfront(3);
            int n = nat(dna);
			t.push_back(tmpl("", -1, n));
		}
		else if (dna.get(0) == 'I' && dna.get(1) == 'I' && (dna.get(2) == 'C' || dna.get(2) == 'F'))
		{
            dna.popfront(3);
			return;
		}
        else if (dna.get(0) == 'I' && dna.get(1) == 'I' && dna.get(2) == 'P')
		{
			std::string rnacmd = dna.getstr(3, 10);
            dna.popfront(10);
			rna.push_back(rnacmd);
		}
	}
}

vec asnat(int n)
{
    vec d;
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


void quote(vec& d, vec& nd)
{
    for (cveciter it = d.begin(); it != d.end(); ++it)
	{
		char item = *it;
        if (item == 'I')
		{
            nd.push_back('C');
		}
        else if (item == 'C')
		{
			nd.push_back('F');
		}
        else if (item == 'F')
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
}


vec protect(int l, vec& d)
{
	if (l > 0)
	{
		vec t;
		while (l > 0)
		{
			quote(d, t);
			l -= 1;
		}
	}
	else
	{
		return d;
	}
}
        
void replacefcn(DNAList& dna, tvec& tpl, evec& e)
{
	vec r;
	for (ctveciter it = tpl.begin(); it != tpl.end(); ++it)
	{
		tmpl t = *it;
		if (t.s.size() == 0)
		{
			if (t.l == -1)
			{
				// |n|
				int a = 0;
				if (t.n < e.size())
				{	
					a = e[t.n].size();
				}
				vec an = asnat(a);
				for (cveciter ii = an.begin(); ii != an.end(); ++ii)
				{
					r.push_back(*ii);
				}
			}
			else
			{
				// n(l)
				if (t.n < e.size())
				{
					vec an = protect(t.l, e[t.n]);
					for (cveciter ii = an.begin(); ii != an.end(); ++ii)
					{
						r.push_back(*ii);
					}
				}
			}
		}
        else
		{
            // Base
            r.push_back(t.s[0]);
		}
	}
    dna.insertfront(r);
}

    


void matchreplace(DNAList& dna, svec& pat, tvec& t)
{
    evec e;
    ivec c;
    size_t i = 0;
    for (csveciter it = pat.begin(); it != pat.end(); ++it)
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
			vec tmp;
			dna.getvec(tmp, c.back(), i); 
			c.pop_back();
            e.push_back(tmp);
		}
        else
		{
            // Base
            if (dna.get(i) == p[0])
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
    dna.popfront(i);
    replacefcn(dna, t, e);
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
			}
		}
		catch(...)
		{
			std::cout << "Finished!" << std::endl;
			break;
		}
	}
}

int _tmain(int argc, _TCHAR* argv[])
{
    //prefix = ""
    //if len(sys.argv) > 3:
    //    prefixfile = file(sys.argv[3], 'r')
    //    prefix = prefixfile.read()
    //    prefixfile.close()
    //if len(sys.argv) > 2:
    //    dnafile = file(sys.argv[1], 'r')
    //    dna = DNAList(prefix + dnafile.read())
    //    dnafile.close()
    //    rna = []
    //    try:
    //        dna = execute(dna, rna, True)
    //    except KeyboardInterrupt:
    //        rnafile = file(sys.argv[2], 'w')
    //        rnafile.write(''.join(rna))
    //        rnafile.close()
    //        sys.exit(1)
    //    rnafile = file(sys.argv[2], 'w')
    //    rnafile.write(''.join(rna))
    //    rnafile.close()
    //    
    //else:
        // Run tests
	{
		std::cout << "Test pattern function:" << std::endl;
		svec sv;
		sv.push_back("CIIC");
		sv.push_back("IIPIPICPIICICIIF");
		for (size_t i = 0; i < sv.size(); ++i)
		{
            svec rna;
			vec dnavec;
			str2vec(sv[i], dnavec);
            DNAList dna(dnavec);
			svec p;
            patternfcn(dna, rna, p);
			std::string s = sv[i];
			std::cout << s << " -> ";
			for (size_t ii = 0; ii < p.size(); ++ii)
			{
				std::cout << p[ii];
			}
			std::cout << std::endl;
			std::cout.flush();
		}
	}

	{

		std::cout << "Test dna execution function:" << std::endl;
		svec sv;
		sv.push_back("IIPIPICPIICICIIFICCIFPPIICCFPC");
		sv.push_back("IIPIPICPIICICIIFICCIFCCCPPIICCFPC");
		sv.push_back("IIPIPIICPIICIICCIICFCFC");
		for (size_t i = 0; i < sv.size(); ++i)
		{
            svec rna;
			vec dnavec;
			str2vec(sv[i], dnavec);
            DNAList dna(dnavec);
            execute(dna, rna, true);
			std::cout << sv[i] << " -> ";
			//for (size_t ii = 0; ii < dna.size(); ++ii)
			//{
			//	std::cout << dna.get(ii);
			//}
			std::cout << std::endl;
		}
	}
	return 0;
}

