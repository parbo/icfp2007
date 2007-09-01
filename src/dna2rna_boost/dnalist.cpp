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
}

void DNAList::release()
{
	{
		dnareflist::const_iterator it = m_list.begin();
		dnareflist::const_iterator end = m_list.end();
		for (; it != end; ++it)
		{
			delete *it;
		}
		m_list.clear();
	}
	{
		std::vector<dnaseq*>::iterator it = m_allocated.begin();
		std::vector<dnaseq*>::iterator end = m_allocated.end();
		for (; it != end; ++it)
		{
			delete *it;
		}
		m_allocated.clear();
	}
}

size_t DNAList::size() const
{
    size_t len = 0;
	dnareflist::const_iterator it = m_list.begin();
	dnareflist::const_iterator end = m_list.end();
    for (; it != end; ++it)
    {
		size_t sz = (*it)->size();
        len += sz;
    }
    return len;
}

void DNAList::flatten()
{
    size_t tsz = size();
    dnaseq* data = new dnaseq;
	data->reserve(tsz);
	dnareflist::iterator it = m_list.begin();
	dnareflist::iterator end = m_list.end();
    for (; it != end; ++it)
    {
        dnaseqrange r = (*it)->get();
        std::copy(r.first, r.second, std::back_inserter(*data));
    }
	release();
	m_allocated.push_back(data);
	dnareflist rl;
	rl.push_back(new DNARef(0, tsz, data));
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
	dnareflist::iterator it = m_list.begin();
	dnareflist::iterator end = m_list.end();
    for (; it != end; ++it)
    {
        size_t sz = (*it)->size();
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
		for (dnareflist::iterator it = m_list.begin(); it != m_list.begin()+n; ++it)
		{
			delete *it;
		}
        m_list.erase(m_list.begin(), m_list.begin()+n);
    }
    if (num > 0)
    {
        m_list[0]->popfront(num);
    }
}    

char DNAList::operator[](size_t ref) const throw(int)
{
    size_t ix = 0;
	dnareflist::const_iterator it = m_list.begin();
	dnareflist::const_iterator end = m_list.end();
    for (; it != end; ++it)
    {
        size_t lr = (*it)->size();
        if (ix + lr > ref)
        {
            return (**it)[ref-ix];
        }
        else
        {
            ix += lr;
        }
    }
    throw 1;
}

void DNAList::getreflist(dnareflist& rl, size_t rstrt, size_t rstp) const
{
    size_t ix = 0;
	dnareflist::const_iterator it = m_list.begin();
	dnareflist::const_iterator end = m_list.end();
    for (; it != end; ++it)
    {
        const DNARef& r = **it;
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
				if (start != stop)
				{
					rl.push_back(new DNARef(start, stop, r.getdata()));
				}
				else
				{
					//std::cout << "WTF!!!!" << std::endl;
				}
				return;
            }
            else
            {
                stop = r.getstop();
            }
			
			if (start != stop)
			{
				rl.push_back(new DNARef(start, stop, r.getdata()));
			}
			else
			{
				//std::cout << "WTF!!!!" << std::endl;
			}
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
	std::copy(reflist.rbegin(), reflist.rend(), std::front_inserter(m_list));
    size_t ls = m_list.size();
    if (ls > 350)
    {
        flatten();
    }
}        

int DNAList::find(const std::string& substr, size_t startpos) const
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
	size_t li = 0;
	size_t ll = m_list.size();
    size_t ix = 0;
	size_t findli = 0;
	size_t findix = 0;
	while (li < ll)
    {
        DNARef* r = m_list[li];
        size_t lr = r->size();
        if (ix + lr < i)
        {
            ; 
        }
        else
        {
            while (i - ix < lr)
            {
                if ((*r)[i-ix] == c)
                {
                    if (subpos == 0)
                    {
                        findpos = i;
						findli = li;
						findix = ix;
                    } 
                    ++subpos;
                    if (subpos == ls)
                    {
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
					if (li != findli)
					{
						li = findli;
						ix = findix;
						r = m_list[li];
						lr = r->size();
					}
                    subpos = 0;
                    c = substr[subpos];
                }
            	i += 1;
            }
        }
        ix += lr;
		++li;
    }
    return -1;
}

