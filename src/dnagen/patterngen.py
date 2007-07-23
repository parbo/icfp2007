import sys

primitive = {
    '(' : 'IIP',
    ')' : 'IIC',
    'I' : 'C',
    'C' : 'F',
    'F' : 'P',
    'P' : 'IC'
}

def getnumber(p, ix):
    pc = p[ix]
    n = 0
    while (ix < len(p)) and (pc.isdigit()):
        n = 10 * n + int(pc)
        ix += 1
        pc = p[ix]
    return ix, n
    
def getconsts(p, ix):
    pc = p[ix]
    seq = ['IFF']
    while (ix < len(p)) and (pc in 'ICFP'):
        seq.append(primitive[pc])
        ix += 1
        pc = p[ix]
    return ix, ''.join(seq)
    
def numberseq(n):
    seq = []
    while (n > 0):
        if (n % 2) == 0:
            seq.append('I')
        else:
            seq.append('C')
        n /= 2
    seq.append('P')
    return ''.join(seq)
    
def pattern(p):
    ps = []
    ix = 0
    while (ix < len(p)):
        pc = p[ix]
        if (pc in primitive):
            ps.append(primitive[pc])
            ix += 1
        elif (pc == '!'):
            ix, n = getnumber(p, ix + 1)
            ps.append(numberseq(n))
        elif (pc == '?'):
            ix, s = getconsts(p, ix + 1)
            ps.append(s)
            print s
        else:
            ix += 1
    ps.append('IIC')
    return ''.join(ps)
    
def template(t):
    return ''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infilename = int(sys.argv[1])
        infile = file(infilename, 'r')
        p = pattern(infile.readline())
        t = template(infile.readline())
        print p + t
        outfile = file(infilename + '.dna', 'w')
        outfile.write(p + t)
        outfile.close()
        
    else:
        print pattern('I')
        print pattern('(!2)P')
        print pattern('(?IFPCFFP)IIIII')