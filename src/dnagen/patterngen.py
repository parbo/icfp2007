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
    return (ix, n)
    
def getnumberpair(p, ix):
    ix, n1 = getnumber(p, ix)
    while (not p[ix].isdigit()):
        ix += 1
    ix, n2 = getnumber(p, ix)
    return (ix, n1, n2)
    
def getconsts(p, ix):
    pc = p[ix]
    seq = ['IFF']
    while (ix < len(p)) and (pc in 'ICFP'):
        seq.append(primitive[pc])
        ix += 1
        pc = p[ix]
    return (ix, ''.join(seq))
    
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
            ps.append('IP')
            ps.append(numberseq(n))
        elif (pc == '?'):
            ix, s = getconsts(p, ix + 1)
            ps.append(s)
        else:
            ix += 1
    ps.append('IIC')
    return ''.join(ps)
    
def template(t):
    ts = []
    ix = 0
    while (ix < len(t)):
        tc = t[ix]
        if (tc in 'ICFP'):
            ts.append(primitive[tc])
            ix += 1
        elif tc.isdigit():
            ix, n = getnumber(t, ix)
            ts.append('IIP')
            ts.append(numberseq(n))
        elif tc == 'n': # encode number as bases
            ix, n = getnumber(t, ix)
            ts.append(numberseq(n))
        elif (tc == '('):
            ix, n1, n2 = getnumberpair(t, ix + 1)
            ts.append('IP')
            ts.append(numberseq(n1))
            ts.append(numberseq(n2))
        else:
            ix += 1
    ts.append('IIC')
    return ''.join(ts)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        infilename = sys.argv[1]
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
        print template('(0,0)CCCIC')
