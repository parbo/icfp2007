import sys
from rna2fuun.rna2fuun import commands as rnacommands

class DNAList(list):
    def __init__(self, iterable):
        list.__init__(self, iterable)
        self.reverse()
        
    def __str__(self):
        return list.__str__(list(reversed(self)))

    def popfront(self, num=0):
##        print "popfront", num, len(self)
        if num == 0:
            return self.pop()
        else:
            r = self[-num:]
            del self[-num:]
            return r
        
    def reflen(self, ref):
        return abs(ref.stop-ref.start)
    
    def reference(self, start, stop):
        return (start, stop)
    
    def getref(self, ref):
        ls = len(self)
        return reversed(self[ls - ref[0] - 1: ls - ref[1] - 1])
        
    def get(self, i):
        return self[-i-1]
    
    def prepend(self, iterable):
        self.extend(reversed(iterable))  
        
    def find(self, substr, i):
        if not substr:
            return -1
        ix = 0
        for i in xrange(i, len(self)):
            if self[-i] == substr[ix]:
                ix += 1
                if ix == len(substr):
                    return i
            else:
                ix = 0
        return -1

class NoMoreData(Exception):
    pass

# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
# The 'rna' parameter is also modified during the process.
def pattern(dna, rna):
    p = []
    lvl = 0
    while dna:
        d = dna.popfront()
        if d == 'C':
            p.append('I')
        elif d == 'F':
            p.append('C')
        elif d == 'P':
            p.append('F')
        elif d == 'I':
            d = dna.popfront()
            if d == 'C':
                p.append('P')
            elif d == 'P':
                n = nat(dna)
                p.append('!' + str(n))
            elif d == 'F':
                dna.popfront() # NOTE: Three bases consumed here.
                s = consts(dna)
                p.append('?' + ''.join(s))
            elif d == 'I':
                d = dna.popfront()
                if d == 'P':
                    lvl += 1
                    p.append('(')
                elif d == 'C' or d == 'F':
                    if lvl > 0:
                        lvl -= 1
                        p.append(')')
                    else:
                        return p
                elif d == 'I':
                    # Add rna command.
                    rnacmd = dna.popfront(7)
                    print rnacmd
                    if ''.join(rnacmd) not in rnacommands:
                        print 'PTN: Warning: Unknown RNA cmd: ' + ''.join(rnacmd)
                    rna.extend(rnacmd)
    raise NoMoreData

# Extracts a template from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the template and a new position after the
# consumed bases: (template, pos)
# The 'rna' parameter is also modified during the process.
def template(dna, rna):
    t = []
    while dna:
        d = dna.popfront()
        if d == 'C':
            t.append('I')
        elif d == 'F':
            t.append('C')
        elif d == 'P':
            t.append('F')
        if d == 'I':
            d = dna.popfront()
            if d == 'C':
                t.append('P')
            elif d == 'F' or d == 'P':
                l = nat(dna)
                n = nat(dna)
                t.append((l, n))
            elif d == 'I':
                d = dna.popfront()
                if d == 'P':
                    n = nat(dna)
                    t.append(n)
                elif d == 'C' or d == 'F':
                    return t
                elif d == 'I':
                    # Add rna command.
                    rnacmd = dna.popfront(7)
                    print rnacmd
                    if ''.join(rnacmd) not in rnacommands:
                        print 'Warning: Unknown RNA cmd: ' + ''.join(rnacmd)
                    rna.extend(rnacmd)
    raise NoMoreData

# Extracts a natural number from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the number and a new position after the
# consumed bases: (number, pos)
def nat(dna):
    try:
        d = dna.popfront()
        if (d == 'P'):
            return 0
        elif (d == 'I') or (d == 'F'):
            n = nat(dna)
            return 2 * n
        elif (d == 'C'):
            n = nat(dna)
            return 2 * n + 1
        else:
            # Empty -> Exit
            raise NoMoreData
    except IndexError:
        raise NoMoreData
    
    
        
# Extracts a base sequence from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the sequence and a new position after the
# consumed bases: (sequence, pos)
def consts(dna):
    def constsrec(dna):
        if not dna:
            return []
        d = dna.get(0)
        if d == 'C':
            dna.popfront()
            seq = consts(dna)
            seq.append('I')
            return seq
        elif d == 'F':
            dna.popfront()
            seq = constsrec(dna)
            seq.append('C')
            return seq
        elif d == 'P':
            dna.popfront()
            seq = constsrec(dna)
            seq.append('F')
            return seq
        elif d == 'I' and dna.get(1) == 'C':
            dna.popfront(2)
            seq = constsrec(dna)
            seq.append('P')
            return seq
        else:
            return []            
    seq = constsrec(dna)
    seq.reverse()
    return seq
    
# Modifies 'dna' by applying template 't' to matching items in pattern 'pat'.
# The matching starts at position 'i'.
def matchreplace(dna, pat, t):
    e = []
    c = []
    i = 0
    print dna
    print pat
    print t
    for p in pat:
        if p.startswith('!'):
            n = int(p[1:])
            i += n
            if (i > len(dna)):
                # Match failed.
                print 'Matched failed in !'
                return
        elif p.startswith('?'):
            substr = p[1:]
            n = dna.find(substr, i)
            if n >= 0:
                i = n + len(substr)
            else:
                # Match failed.
                print 'Matched failed in ?'
                return
        elif (p == '('):
            c.append(i)
        elif (p == ')'):
            e.append(dna.reference(c.pop(), i))
        else:
            # Base
            print i, dna.get(i), p
            if (dna.get(i) == p):
                i += 1
            else:
                # Match failed.
                print 'Matched failed in Base', p
                return
    print "r: ", dna, t, e
    replace(dna, t, e)
    
def replace(dna, tpl, e):
##    print 'Replace ', e
    r = []
    for t in tpl:
        if isinstance(t, int):
            # |n|
            if (t >= len(e)):
                r.extend(asnat(0))
            else:
                r.extend(asnat(dna.reflen(e[t])))
        elif isinstance(t, tuple):
            # n(l)
            l, n = t
            if (n >= len(e)):
                r.extend(protect(l, []))
            else:
                r.extend(protect(l, dna.getref(e[n])))
        else:
            # Base
            r.append(t)
    print r
    dna.prepend(r)
    
def protect(l, d):
    for ix in xrange(l):
        d = quote(d)
    return d
        
def quote(d):
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
    return nd
    
def asnat(n):
    d = []
    while n > 0:
        if (n % 2) == 0:
            d.append('I')
        else:
            d.append('C')
        n /= 2
    d.append('P')
    return d
    
def execute(dna, rna, progress = False):
    pos = 0
    n = 0
    while True:
        n += 1
        try:
            p = pattern(dna, rna)
            t = template(dna, rna)
            #print p, t
            matchreplace(dna, p, t)
            if progress:
                print 'Iterations: ' + str(n) + '   DNA remaining: ' + str(len(dna)), '   RNA commands: ' + str(len(rna) / 7)
        except NoMoreData:
            print 'DNA remaining: ' + str(len(dna))
            break
    return dna

if __name__ == '__main__':
    prefix = []
    if len(sys.argv) > 3:
        prefixfile = file(sys.argv[3], 'r')
        prefix = DNAList(prefixfile.read())
        prefixfile.close()
    if len(sys.argv) > 2:
        dnafile = file(sys.argv[1], 'r')
        dna = DNAList(prefix + DNAList(dnafile.read()))
        dnafile.close()
        rna = []
        try:
            dna = execute(dna, rna, True)
        except KeyboardInterrupt:
            rnafile = file(sys.argv[2], 'w')
            rnafile.write(''.join(rna))
            rnafile.close()
            sys.exit(1)
        rnafile = file(sys.argv[2], 'w')
        rnafile.write(''.join(rna))
        rnafile.close()
        
    else:
        # Run tests
        print ''
        print 'Test pattern function:'
        print ''
        for dnastr in ['CIIC', 'IIPIPICPIICICIIF']:
            rna = []
            dna = DNAList(dnastr)
            p = pattern(dna, rna)
            print dnastr + ' -> ' + ''.join(p)
        print ''
        print ''
        print 'Test dna execution function:'
        print ''
        for dnastr in ['IIPIPICPIICICIIFICCIFPPIICCFPC', 'IIPIPICPIICICIIFICCIFCCCPPIICCFPC', 'IIPIPIICPIICIICCIICFCFC']:
            dna = DNAList(dnastr)
            rna = []
            dna = execute(dna, rna)
            print dnastr + ' -> ' + ''.join(dna)