#include "dnalist.hpp"
#include "dna2rna.hpp"

#include <iostream>
#include <string>
#include <fstream>
#include <ios>
#include <time.h>

int main(int argc, char* argv[])
{
	dnaseqptr d(new dnaseq());
    if (argc > 3)
    {
    	std::cout << "Loading prefix" << std::endl;
		std::ifstream f(argv[3], std::ios::in|std::ios::binary);
		while (1)
		{
			char v;
			f.read(&v, 1);
			if (f.eof())
			{
				break;
			}
			d->push_back(v);
		}
    }
    if (argc > 2)
    {
    	std::cout << "Loading dna" << std::endl;
		std::ifstream f(argv[1], std::ios::in|std::ios::binary);
		while (1)
		{
			char v;
			f.read(&v, 1);
			if (f.eof())
			{
				break;
			}			
			d->push_back(v);
		}
        svec rna;
        DNAList dna;
    	std::cout << "Total size: " << d->size() << std::endl;        
        dna.insertfront(new DNARef(0, d->size(), d));
		time_t before = time(0);
    	std::cout << "Executing..." << std::endl;
        execute(dna, rna, true);
		time_t after = time(0);
		std::cout << "Finished in: " << after-before << " seconds" << std::endl;
	}        
    else
	{
		{
			std::cout << "Test pattern function:" << std::endl;
			svec sv;
			sv.push_back("CIIC");
			sv.push_back("IIPIPICPIICICIIF");
			for (size_t i = 0; i < sv.size(); ++i)
			{
	            svec rna;
				dnaseqptr d(new dnaseq());
				str2dnaseq(sv[i], *d);
	            DNAList dna;
	            dna.insertfront(new DNARef(0, d->size(), d));
				svec p;
				try
				{
	            	patternfcn(dna, rna, p);
				}
				catch (...)
				{
					std::cout << "Finished" << std::endl;
				}
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
				dnaseqptr d(new dnaseq());
				str2dnaseq(sv[i], *d);
	            DNAList dna;
	            dna.insertfront(new DNARef(0, d->size(), d));
	            execute(dna, rna, true);
				std::cout << sv[i] << " -> ";
				//for (size_t ii = 0; ii < dna.size(); ++ii)
				//{
				//	std::cout << dna.get(ii);
				//}
				std::cout << std::endl;
			}
		}
	}
	return 0;
}

