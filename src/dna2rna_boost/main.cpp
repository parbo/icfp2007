#include "dnalist.hpp"
#include "dna2rna.hpp"

#include <iostream>
#include <string>

int main(int argc, char argv[])
{
    //prefix = ""
    //if len(sys.argv) > 3:
    //    prefixfile = file(sys.argv[3], 'r')
    //    prefix = prefixfile.read()
    //    prefixfile.close()
    //if len(sys.argv) > 2:
    //    dnafile = file(sys.argv[1], 'r')
    //    dna = DNAList(prefix + dnafile.read())
    //    dnafile.close()
    //    rna = []
    //    try:
    //        dna = execute(dna, rna, True)
    //    except KeyboardInterrupt:
    //        rnafile = file(sys.argv[2], 'w')
    //        rnafile.write(''.join(rna))
    //        rnafile.close()
    //        sys.exit(1)
    //    rnafile = file(sys.argv[2], 'w')
    //    rnafile.write(''.join(rna))
    //    rnafile.close()
    //    
    //else:
        // Run tests
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
            patternfcn(dna, rna, p);
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
	return 0;
}

