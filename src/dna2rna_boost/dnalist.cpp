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

size_t DNAList::size() const
{
    size_t len = 0;
    for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
    {
        len += (*it).size();
    }
    return len;
}

void DNAList::flatten()
{
    size_t tsz = size();
    dnaseqptr data(new dnaseq(tsz));
    dnaseq::iterator dit = data->begin();
    for (dnareflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
    {
        dnaseqrange r = (*it).get();
        dit = std::copy(r.first, r.second, dit);
    }
    m_list.clear();
    insertfront(new DNARef(0, tsz, data));
}

void DNAList::popfront(size_t num)
{
    size_t n = 0;
    for (dnareflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
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
        m_list.erase(m_list.begin()+m_list.size()-n, m_list.end());
    }
    if (num > 0)
    {
        m_list.back().popfront(num);
    }
}    

void DNAList::popfromitem(size_t num, size_t item)
{
    if (num == 0)
    {
        return;
    }

    size_t n = 0;
    size_t start = m_list.size()-item-1;
    for (int i = start; i >= 0; --i)
    {
        DNARef& r = m_list[i];
        size_t lr = r.size();
        if (num == lr)
        {
            // exact match, pop this too
            m_list.erase(m_list.begin()+i, m_list.begin()+start+1);
            break;
        }
        else if (num < lr)
        {
            // popfront on item is needed
            if (n > 0)
            {
                m_list.erase(m_list.begin()+i+1, m_list.begin()+start+1);
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

char DNAList::operator[](size_t ref) const
{
    size_t ix = 0;
    for (dnareflist::const_reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
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
    for (dnareflist::const_reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
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

void DNAList::insertfrontreflistandpopold(dnainsertlist reflist, size_t pop)
{
    size_t offs = 0;
    size_t oldlen = m_list.size();
    for (dnainsertlist::reverse_iterator r = reflist.rbegin(); r != reflist.rend(); ++r)
    {
    	if (!dynamic_cast<DNARef*>(*r))
    	{   
            (*r)->offset(offs);
    	}
        offs += (*r)->size();	
        insertfront((*r));
    }
    size_t ls = m_list.size();
    popfromitem(pop, ls-oldlen);
    if (true || ls > 200)
    {
        flatten();
    }
}        

void DNAList::insertfront(DNARefEmpty* ref)
{
    DNARef* rp = dynamic_cast<DNARef*>(ref);
    if (rp != 0)
    {
        m_list.push_back(*rp);
    }
    else
    {
        dnareflist tmpreflist;
        size_t ix = 0;
        for (dnareflist::reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
        {
            DNARef& r = *it;
            size_t lr = r.size();
            if (ix + lr <= ref->getstart())
            {
            	;
            }
            else
            {
                size_t start = 0;
                size_t stop = 0;
                if (ix <= ref->getstart())
                {
                    start = r.getstart()+ref->getstart()-ix;
                }
                else
                {                    
                    start = r.getstart();
                }
                
                if (ix + lr >= ref->getstop())
                {
                    stop = r.getstart()+ref->getstop()-ix;
                }
                else
                {
                    stop = r.getstop();
                }                   
                  
                tmpreflist.push_back(DNARef(start, stop, r.getdata()));
//                std::cout << "Adding " << start << " " << stop << std::endl;
            }
            if (ix + lr >= ref->getstop())
            {
            	for (dnareflist::reverse_iterator it = tmpreflist.rbegin(); it != tmpreflist.rend(); ++it)
            	{
                    m_list.push_back(*it);
            	}
            	//std::copy(tmpreflist.rbegin(), tmpreflist.rend(), std::back_inserter(m_list));
                break;
            }
            ix += lr;
        }
    }
    delete ref;
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
    for (dnareflist::const_reverse_iterator it = m_list.rbegin(); it != m_list.rend(); ++it)
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

