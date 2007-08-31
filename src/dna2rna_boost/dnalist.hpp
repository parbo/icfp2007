#ifndef DNALIST_HPP_
#define DNALIST_HPP_

#include <vector>
#include <deque>
#include <string>

typedef std::vector<char> dnaseq;
typedef std::pair<dnaseq::const_iterator, dnaseq::const_iterator> dnaseqrange; 

typedef std::vector<std::string> svec;
typedef std::vector<size_t> ivec;
typedef std::vector<std::pair<size_t, size_t> > evec;


void str2dnaseq(std::string s, dnaseq& v);
std::string dnaseq2str(const dnaseq& v);

class DNARef
{
public:
	DNARef(size_t start, size_t stop, const dnaseq* data) : m_start(start), m_stop(stop), m_data(data) {}

    void popfront(size_t num)
	{
        m_start += num;
	}
        
	char operator[](size_t ix) const
	{
		return m_data->at(m_start + ix);
	}
	
	dnaseqrange getrange(size_t start, size_t stop) const
	{
		return std::make_pair(m_data->begin()+start, m_data->begin()+stop);
	}

	dnaseqrange get() const
	{
		return getrange(m_start, m_stop);
	}
	
	const dnaseq* getdata() const
	{
		return m_data;
	}
		
	size_t getstart() const { return m_start; }
	size_t getstop() const { return m_stop; }

	size_t size() const
	{
		return m_stop-m_start;
	}
	
	void offset(size_t offs)
	{
		m_start += offs;
		m_stop += offs;
	}
protected:
	size_t m_start;
	size_t m_stop;
	const dnaseq* m_data;
};

typedef std::deque<DNARef> dnareflist;

class DNAList
{
public:
	DNAList() {}
	~DNAList();

	size_t size() const;
	void clear();
    void flatten();
    void popfront(size_t num);
    void getreflist(dnareflist& rl, size_t start, size_t stop) const;
	char operator[](size_t ref) const;
    void insertfront(const dnareflist& reflist);
    int find(std::string substr, size_t startpos) const;
	template <class T> 
	void get(T& tmp, size_t rstrt, size_t rstp) const
	{
		size_t ix = 0;
		for (dnareflist::const_iterator it = m_list.begin(); it != m_list.end(); ++it)
		{
			const DNARef& r = *it;
			size_t lr = r.size();
			if (ix + lr < rstrt)
			{
				if (ix + lr >= rstp)
				{
					return;
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
					return;
				}
				dnaseqrange rng = r.getrange(start, stop);
				std::copy(rng.first, rng.second, std::back_inserter(tmp));
			}        	
			ix += lr;
		}
	}

	dnaseq* allocate();
protected:
	void release();

	dnareflist m_list; 
	std::vector<dnaseq*> m_allocated;
};

#endif /*DNALIST_HPP_*/
