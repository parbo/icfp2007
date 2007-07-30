%module rna2fuun_c

%include stl.i
%include std_string.i

%{
#include "rna2fuun.hpp"
%}

%typemap(out) pixelbuffer {
    $result = PyString_FromStringAndSize($1.data,$1.size);
}

%template() std::vector<std::string>;

class rna2fuun
{
public:
	rna2fuun();
	~rna2fuun();

	void buildstep(std::string rna);
	void buildsteps(std::vector<std::string> rna);
	pixelbuffer getImage() const;
};
