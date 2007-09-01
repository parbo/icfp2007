#include "dnalist.hpp"
#include "dna2rna.hpp"

#include <iostream>
#include <string>
#include <fstream>
#include <ios>
#include <iterator>
#include <time.h>


int main(int argc, char* argv[])
{
	DNAList dna;
	dnaseq* d = dna.allocate();
    if (argc > 3)
    {
    	std::cout << "Loading prefix" << std::endl;
		std::ifstream f(argv[3], std::ios::in|std::ios::binary);
		std::copy(std::istream_iterator<char>(f), std::istream_iterator<char>(), std::back_inserter(*d));
    }
    if (argc > 2)
    {
    	std::cout << "Loading dna" << std::endl;
		std::ifstream f(argv[1], std::ios::in|std::ios::binary);
		std::copy(std::istream_iterator<char>(f), std::istream_iterator<char>(), std::back_inserter(*d));
        svec rna;
    	std::cout << "Total size: " << d->size() << std::endl;        
		dnareflist rl;
		rl.push_back(new DNARef(0, d->size(), d));
        dna.insertfront(rl);
		time_t before = time(0);
    	std::cout << "Executing..." << std::endl;
		dna_debug = false;
		dna_skip = 10000;
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
				dna.clear();
				dnaseq* d = dna.allocate();
				str2dnaseq(sv[i], *d);
				dnareflist rl;
				rl.push_back(new DNARef(0, d->size(), d));
	            dna.insertfront(rl);
				pvec p;
				try
				{
	            	patternfcn(dna, rna, p);
				}
				catch (int e)
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
	
/*		{
	
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
			} */
	}
	return 0;
}

