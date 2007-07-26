import sys
import re
import os
        
def numstr(n):
    seq = []
    for ix in range(8):
        if (n % 2) == 0:
            seq.append('I')
        else:
            seq.append('C')
        n /= 2
    seq.append('P')
    return ''.join(seq)
    
def nat(dna):
    dnastr = dna.pop(0)
    if (dnastr == 'P'):
        return 0
    elif (dnastr == 'I') or (dnastr == 'F'):
        n = nat(dna)
        return 2 * n
    elif (dnastr == 'C'):
        n = nat(dna)
        return 2 * n + 1
        
def consts(dna):
    def constsrec(dna):
        dnastr = ''.join(dna[0:2])
        if dnastr.startswith('C'):
            dna.pop(0)
            seq = constsrec(dna)
            seq.append('I')
            return seq
        elif dnastr.startswith('F'):
            dna.pop(0)
            seq = constsrec(dna)
            seq.append('C')
            return seq
        elif dnastr.startswith('P'):
            dna.pop(0)
            seq = constsrec(dna)
            seq.append('F')
            return seq
        elif dnastr.startswith('IC'):
            dna.pop(0)
            dna.pop(0)
            seq = constsrec(dna)
            seq.append('P')
            return seq
        else:
            return []
            
    seq = constsrec(list(dna))
    seq.reverse()
    return ''.join(seq)
        
def quote(d):
    d = list(d)
    nd = []    
    for item in d:
        if (item == 'I'):
            nd.append('C')
        elif (item == 'C'):
            nd.append('F')
        elif (item == 'F'):
            nd.append('P')
        else:
            # P
            nd.append('I')
            nd.append('C')
    return ''.join(nd)
    
def ascii(s):
    out = []
    s = list(s)
    while s:
        out.append(ch.get(nat(s), '_'))
    return ''.join(out)
    
def splitrna(rna):
    for i in xrange(3, len(rna), 10):
        yield rna[i:i+7] 

if __name__ == '__main__':
    if len(sys.argv) > 1:
        dnafile = file(sys.argv[1], 'r')
        dna = dnafile.read()
        dnafile.close()
        
        print '"Long" RNA sequences:'
        
        regexp = r"(III[I|C|F|P]{7}){100,}"
        r = re.compile(regexp)

        m = r.search(dna)
        
        rnadir = os.getcwd()+os.path.sep+"rna"
        if not os.path.exists(rnadir):
            os.mkdir(rnadir)

        while m:
            x = len(m.group(0))/10
            print "Saving RNA sequence of length %04d"%x
            f = open(rnadir+os.path.sep+"rna_sequence_%04d_%04d.rna"%(m.start(), x), "w")
            f.write(''.join(splitrna(m.group(0))))
            f.close()
            m = r.search(dna, m.end())            
        
        
