import sys
import re

chset = [10, 11, 12, 13, 14, 15,
         16, 26, 28, 29, 30, 31,
         32, 33, 43, 44, 45, 46, 47,
         57, 58, 59, 60, 61, 62, 63,
         65, 66, 67, 68, 69, 70, 71, 72, 73,
         81, 82, 83, 84, 85, 86, 87, 88, 89,
         98, 99, 100, 101, 102, 103, 104, 105,
         123,
         129, 130, 131, 132, 133, 134, 135, 136, 137,
         145, 146, 147, 148, 149, 150, 151, 152, 153,
         162, 163, 164, 165, 166, 167, 168, 169,
         176, 177, 178, 179, 180, 181, 182, 183, 184, 185]
         
ch = { 65 : 'a',
       66 : 'b',
       67 : 'c',
       68 : 'd',
       69 : 'e',
       70 : 'f',
       71 : 'g',
       72 : 'h',
       73 : 'i',
       81 : 'j',
       82 : 'k',
       83 : 'l',
       84 : 'm',
       85 : 'n',
       86 : 'o',
       87 : 'p',
       88 : 'q',
       89 : 'r',
       98 : 's',
       99 : 't',
      100 : 'u',
      101 : 'v',
      102 : 'w',
      103 : 'x',
      104 : 'y',
      105 : 'z',
      129 : 'A',
      130 : 'B',
      131 : 'C',
      132 : 'D',
      133 : 'E',
      134 : 'F',
      135 : 'G',
      136 : 'H',
      137 : 'I',
      145 : 'J',
      146 : 'K',
      147 : 'L',
      148 : 'M',
      149 : 'N',
      150 : 'O',
      151 : 'P',
      152 : 'Q',
      153 : 'R',
      162 : 'S',
      163 : 'T',
      164 : 'U',
      165 : 'V',
      166 : 'W',
      167 : 'X',
      168 : 'Y',
      169 : 'Z',
      176 : '0',
      177 : '1',
      178 : '2',
      179 : '3',
      180 : '4',
      181 : '5',
      182 : '6',
      183 : '7',
      184 : '8',
      185 : '9'}
         
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
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        dnafile = file(sys.argv[1], 'r')
        dna = dnafile.read()
        dnafile.close()
        
        print 'Quoted strings:'
        
        regexp = '(' + '|'.join([quote(numstr(c)) for c in chset]) + ')+' + quote(numstr(255))
        r = re.compile(regexp)

        m = r.search(dna)
        
        while m:
            print str(m.start()).rjust(10) + '   ' + ascii(consts(m.group()))
            m = r.search(dna, m.end())
        
        print ''
        print 'Unquoted strings:'
        
        regexp = '(' + '|'.join([numstr(c) for c in chset]) + ')+' + numstr(255)
        r = re.compile(regexp)

        m = r.search(dna)
        
        while m:
            print str(m.start()).rjust(10) + '   ' + ascii(m.group())
            m = r.search(dna, m.end())
            
        
        