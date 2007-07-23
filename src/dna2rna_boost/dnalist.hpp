#ifndef DNALIST_HPP_
#define DNALIST_HPP_

#include <vector>
#include <boost/shared_ptr.hpp>

typedef std::vector<char> dnaseq;
typedef boost::shared_ptr<std::vector<char> > dnaseqptr;
typedef std::pair<dnaseq::const_iterator, dnaseq::const_iterator> dnaseqrange; 

class DNARefEmpty
{
public:
	DNARefEmpty(size_t start, size_t stop) : m_start(start), m_stop(stop) {}
	virtual ~DNARefEmpty() {}
	
	size_t getstart() const { return m_start; }
	size_t getstop() const { return m_stop; }

	size_t size() const
	{
		return m_stop-m_start;
	}
	
protected:
	size_t m_start;
	size_t m_stop;
private:
	DNARefEmpty();
};

class DNARef : public DNARefEmpty
{
public:
	DNARef(size_t start, size_t stop, dnaseqptr data) : DNARefEmpty(start, stop), m_data(data) {}
	
	DNARef(const DNARefEmpty& ref, dnaseqptr data) : DNARefEmpty(ref), m_data(data) {} 
	
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
	
	dnaseqptr getdata()
	{
		return m_data;
	}
	
	void offset(size_t offs)
	{
		m_start += offs;
		m_stop += offs;
	}
	
protected:
	dnaseqptr m_data;
};

typedef std::vector<DNARef> dnareflist;
typedef std::vector<DNARefEmpty*> dnainsertlist;

class DNAList
{
public:
	DNAList() {}

	size_t size() const;
    void flatten();
    void popfront(size_t num);
    void popfromitem(size_t num, size_t item);
	char operator[](size_t ref) const;
    void insertfrontreflistandpopold(dnainsertlist reflist, size_t pop);
    void insertfront(DNARefEmpty* ref);
    int find(const dnaseq&, size_t startpos) const;
protected:
	dnareflist m_list;        
};

#endif /*DNALIST_HPP_*/
