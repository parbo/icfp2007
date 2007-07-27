from dna2rna_ref import pattern, template
import dnareflist
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dnafile = file(sys.argv[1], 'r')
        dnastr = dnafile.read()
        dna = dnareflist.DNAList()
        dna.insertfront([dnareflist.DNARef(0, len(dnastr), list(dnastr))])
        dnafile.close()
        rna = []
        p = pattern(dna, rna)
        t = template(dna, rna)
        print 'pattern  =', p
        print 'template =', t
        
