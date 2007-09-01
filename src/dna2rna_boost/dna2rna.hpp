#ifndef DNA2RNA_HPP_
#define DNA2RNA_HPP_

#include "dnalist.hpp"
    
extern bool dna_debug;
extern unsigned int dna_skip;

class ptn
{
public:
	enum ptntype
	{
		SKIP,
		FIND,
		BASE,
		LPAREN,
		RPAREN,
	};
	ptntype t;
	virtual ~ptn() {}
	virtual std::ostream& print(std::ostream& s) const = 0;
	friend std::ostream& operator<<(std::ostream& s, const ptn& p);
protected:
	ptn(ptntype t) : t(t) {}
private:
	ptn();
};

class ptnbase : public ptn
{
public:
	ptnbase(char b) : ptn(BASE), b(b) {}
	char b;
	std::ostream& print(std::ostream& s) const
	{
		s << b;
		return s;
	}
private:
	ptnbase();
};

class ptnskip : public ptn
{
public:
	ptnskip(size_t n) : ptn(SKIP), n(n) {}
	size_t n;
	std::ostream& print(std::ostream& s) const
	{
		s << "!" << n;
		return s;
	}
private:
	ptnskip();
};

class ptnfind : public ptn
{
public:
	ptnfind(const std::string& str) : ptn(FIND), str(str) {}
	std::string str;
	std::ostream& print(std::ostream& s) const
	{
		s << "?" << str;
		return s;
	}
private:
	ptnfind();
};

class ptnparen : public ptn
{
public:
	ptnparen(ptntype t) : ptn(t) {}
	std::ostream& print(std::ostream& s) const
	{
		if (t == LPAREN)
		{
			s << "(";
		}
		else
		{
			s << ")";
		}
		return s;
	}
private:
	ptnparen();
};

class tmpl
{
public:
	tmpl(char c=0, int l=-1, int n=-1) : c(c), l(l), n(n) {}
	char c;
	int l;
	int n;
};

typedef std::vector<tmpl> tvec;
typedef std::vector<ptn*> pvec;

void patternfcn(DNAList& dna, svec& rna, pvec& p);
unsigned int execute(DNAList& dna, svec& rna, bool progress = false, int iterations = -1);

#endif /*DNA2RNA_HPP_*/
