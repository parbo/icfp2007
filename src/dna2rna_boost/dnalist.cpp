#include "dnalist.hpp"
#include <algorithm>
#include <iostream>

void str2dnaseq(std::string s, dnaseq& v)
{
    for (size_t i = 0; i < s.size(); ++i)
    {
        v.push_back(s[i]);
    }
}

std::string dnaseq2str(const dnaseq& v)
{
    std::string s;
    for (dnaseq::const_iterator it = v.begin(); it != v.end(); ++it)
    {
        s.push_back(*it);
    }
    return s;
}

DNAList::~DNAList()
{
	release();
}

void DNAList::clear()
{
	release();
	m_list.clear();

}

void DNAList::release()
{
	for (std::vector<dnaseq*>::iterator it = m_allocated.begin(); it != m_allocated.end(); ++it)
	{
		delete *it;
	}
	m_allocated.clear();
}

size_t DNAList::size() const
{
    size_t len = 0;
	std::cout << "Size: (" << std::endl;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
    {
		size_t sz = (*it).size();
		std::cout << "  " << sz << std::endl;
        len += sz;
    }
	std::cout << ")" << std::endl;
    return len;
}

void DNAList::flatten()
{
    size_t tsz = size();
    dnaseq* data = new dnaseq(tsz);
    dnaseq::iterator dit = data->begin();
    for (dnareflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
    {
        dnaseqrange r = (*it).get();
        dit = std::copy(r.first, r.second, dit);
    }
    m_list.clear();
	release();
	m_allocated.push_back(data);
	dnareflist rl;
	rl.push_back(DNARef(0, tsz, data));
    insertfront(rl);
}

dnaseq* DNAList::allocate()
{
	dnaseq* d = new dnaseq;
	m_allocated.push_back(d);
	return d;
}

void DNAList::popfront(size_t num)
{
    size_t n = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
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
        m_list.erase(m_list.begin(), m_list.begin()+n);
    }
    if (num > 0)
    {
        m_list[0].popfront(num);
    }
}    

char DNAList::operator[](size_t ref) const
{
    size_t ix = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
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
    throw "No more data";
}

std::string DNAList::getstr(size_t rstrt, size_t rstp) const
{
    std::string tmp;
    size_t ix = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
    {
        const DNARef& r = *it;
        size_t lr = r.size();
        if (ix + lr < rstrt)
        {
            if (ix + lr >= rstp)
            {
                return tmp;
            }
        }
        else
        {
            size_t start = 0;
            size_t stop = 0;
            if (ix <= rstrt)
            {
                start = r.getstart()+rstrt-ix;
            }
            else
            {
                start = r.getstart();
            }
            
            if (ix + lr >= rstp)
            {
                stop = r.getstart()+rstp-ix;
            }
            else
            {
                stop = r.getstop();
            }
            
            if (ix + lr >= rstp)
            {
            	dnaseqrange rng = r.getrange(start, stop);
            	std::copy(rng.first, rng.second, std::back_inserter(tmp));
                return tmp;
            }
            dnaseqrange rng = r.getrange(start, stop);
            std::copy(rng.first, rng.second, std::back_inserter(tmp));
        }        	
        ix += lr;
    }
}

void DNAList::getreflist(dnareflist& rl, size_t rstrt, size_t rstp) const
{
    size_t ix = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
    {
        const DNARef& r = *it;
        size_t lr = r.size();
        if (ix + lr < rstrt)
        {
			;
        }
        else
        {
            size_t start = 0;
            size_t stop = 0;
            if (ix <= rstrt)
            {
                start = r.getstart()+rstrt-ix;
            }
            else
            {
                start = r.getstart();
            }
            
            if (ix + lr >= rstp)
            {
                stop = r.getstart()+rstp-ix;
				rl.push_back(DNARef(start, stop, r.getdata()));
				return;
            }
            else
            {
                stop = r.getstop();
            }
			
			rl.push_back(DNARef(start, stop, r.getdata()));
        }        	
		if (ix + lr >= rstp)
		{
			return;
		}
        ix += lr;
    }
}

void DNAList::insertfront(const dnareflist& reflist)
{
	// Note: front_inserter reverses the copied list, which is what we want!
	std::copy(reflist.begin(), reflist.end(), std::front_inserter(m_list));
    size_t ls = m_list.size();
    if (ls > 200)
    {
        flatten();
    }
}        

int DNAList::find(std::string substr, size_t startpos) const
{
    size_t ls = substr.size();
    if (ls == 0)
    {
    	return -1;
    }
    size_t subpos = 0;
    char c = substr[subpos];
    size_t findpos = 0;
    size_t i = startpos;
    size_t ix = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
    {
        const DNARef& r = *it;
        size_t lr = r.size();
        if (ix + lr < i)
        {
            ; 
        }
        else
        {
            while (i - ix < lr)
            {
                if (r[i-ix] == c)
                {
                    if (subpos == 0)
                    {
                        findpos = i;
                    } 
                    ++subpos;
                    if (subpos == ls)
                    {
                    	//std::cout << "found " << findpos << std::endl;
                        return findpos;
                    }
                    else
                    {
                        c = substr[subpos];
                    }
                }
                else if (subpos > 0)
                {
                    i = findpos;
                    subpos = 0;
                    c = substr[subpos];
                }
            	i += 1;
            }
        }
        ix += lr;
    }
    return -1;
}

