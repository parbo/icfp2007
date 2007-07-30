#include "rna2fuun.hpp"



#include <iostream>
#include <string>
#include <fstream>
#include <ios>
#include <time.h>

int main(int argc, char* argv[])
{
	std::vector<std::string> d;
	std::cout << "Loading rna" << std::endl;
	std::ifstream f(argv[1], std::ios::in|std::ios::binary);
	while (1)
	{
		std::string s;
		for (unsigned int i = 0; i < 7; ++i)
		{
			char v;
			f.read(&v, 1);
			if (f.eof())
			{
				break;
			}			
			s.push_back(v);
		}
		if (f.eof())
		{
			break;
		}			
		d.push_back(s);
	}
	
	time_t before = time(0);
	std::cout << "Executing..." << std::endl;
	rna2fuun r2f;
	for (unsigned int ix = 0; ix < d.size(); ++ix)
	{
		std::string s = d[ix];
	//	std::cout << ix << ": " << s << std::endl;
	//	std::cout.flush();
		r2f.buildstep(s);
	} 
	time_t after = time(0);
	std::cout << "Finished in: " << after-before << " seconds" << std::endl;
	return 0;
}

