import sys
from rna2fuun.rna2fuun import commands as rnacommands

class NoMoreData(Exception):
    pass

# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
# The 'rna' parameter is also modified during the process.
def pattern(dna, pos, rna):
    p = []
    lvl = 0
    while True:
        dnastr = ''.join(dna[pos:pos+3])
        if dnastr.startswith('C'):
            pos += 1
            p.append('I')
        elif dnastr.startswith('F'):
            pos += 1
            p.append('C')
        elif dnastr.startswith('P'):
            pos += 1
            p.append('F')
        elif dnastr.startswith('IC'):
            pos += 2
            p.append('P')
        elif dnastr.startswith('IP'):
            pos += 2
            n, pos = nat(dna, pos)
            p.append('!' + str(n))
        elif dnastr.startswith('IF'):
            pos += 3 # NOTE: Three bases consumed here.
            s, pos = consts(dna, pos)
            p.append('?' + ''.join(s))
        elif dnastr.startswith('IIP'):
            pos += 3
            lvl += 1
            p.append('(')
        elif dnastr.startswith('IIC') or dnastr.startswith('IIF'):
            pos += 3
            if lvl > 0:
                lvl -= 1
                p.append(')')
            else:
                return (p, pos)
        elif dnastr.startswith('III'):
            # Add rna command.
            rnacmd = dna[pos+3:pos+10]
            if ''.join(rnacmd) not in rnacommands:
                print 'Warning: Unknown RNA cmd: ' + ''.join(rnacmd)
            rna.extend(rnacmd)
            pos += 10
        else:
            # Exit
            raise NoMoreData
    return

# Extracts a template from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the template and a new position after the
# consumed bases: (template, pos)
# The 'rna' parameter is also modified during the process.
def template(dna, pos, rna):
    t = []
    while True:
        dnastr = ''.join(dna[pos:pos+3])
        if dnastr.startswith('C'):
            pos += 1
            t.append('I')
        elif dnastr.startswith('F'):
            pos += 1
            t.append('C')
        elif dnastr.startswith('P'):
            pos += 1
            t.append('F')
        elif dnastr.startswith('IC'):
            pos += 2
            t.append('P')
        elif dnastr.startswith('IF') or dnastr.startswith('IP'):
            pos += 2
            l, pos = nat(dna, pos)
            n, pos = nat(dna, pos)
            t.append((l, n))
        elif dnastr.startswith('IIP'):
            pos += 3
            n, pos = nat(dna, pos)
            t.append(n)
        elif dnastr.startswith('IIC') or dnastr.startswith('IIF'):
            return (t, pos + 3)
        elif dnastr.startswith('III'):
            # Add rna command.
            rnacmd = dna[pos+3:pos+10]
            if ''.join(rnacmd) not in rnacommands:
                print 'Warning: Unknown RNA cmd: ' + ''.join(rnacmd)
            rna.extend(rnacmd)
            pos += 10
        else:
            # Exit
            raise NoMoreData
    return

# Extracts a natural number from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the number and a new position after the
# consumed bases: (number, pos)
def nat(dna, pos):
    dnastr = ''.join(dna[pos:pos+1]) # Produces empty string if 'pos' is out of range.
    if (dnastr == 'P'):
        return (0, pos + 1)
    elif (dnastr == 'I') or (dnastr == 'F'):
        n, pos = nat(dna, pos + 1)
        return (2 * n, pos)
    elif (dnastr == 'C'):
        n, pos = nat(dna, pos + 1)
        return (2 * n + 1, pos)
    else:
        # Empty -> Exit
        raise NoMoreData
        
# Extracts a base sequence from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the sequence and a new position after the
# consumed bases: (sequence, pos)
def consts(dna, pos):
    def constsrec(dna, pos):
        dnastr = ''.join(dna[pos:pos+2]) # Produces empty string if 'pos' is out of range.
        if dnastr.startswith('C'):
            seq, pos = constsrec(dna, pos + 1)
            seq.append('I')
            return (seq, pos)
        elif dnastr.startswith('F'):
            seq, pos = constsrec(dna, pos + 1)
            seq.append('C')
            return (seq, pos)
        elif dnastr.startswith('P'):
            seq, pos = constsrec(dna, pos + 1)
            seq.append('F')
            return (seq, pos)
        elif dnastr.startswith('IC'):
            seq, pos = constsrec(dna, pos + 2)
            seq.append('P')
            return (seq, pos)
        else:
            return ([], pos) # Should 'pos' be incremented?
            
    seq, pos = constsrec(dna, pos)
    seq.reverse()
    return (seq, pos)
    
# Modifies 'dna' by applying template 't' to matching items in pattern 'pat'.
# The matching starts at position 'i'.
def matchreplace(dna, pat, t, i):
    e = []
    c = []
    oldi = i
    for p in pat:
        if p.startswith('!'):
            n = int(p[1:])
            i += n
            if (i > len(dna)):
                # Match failed.
                #print 'Matched failed in !'
                return oldi
        elif p.startswith('?'):
            substr = p[1:]
            dnastr = ''.join(dna)
            ix = dnastr.find(substr, i)
            if ix >= 0:
                i = ix + len(substr)
            else:
                # Match failed.
                #print 'Matched failed in ?'
                return oldi
        elif (p == '('):
            c.append(i)
        elif (p == ')'):
            e.append(dna[c.pop():i])
        else:
            # Base
            if (dna[i] == p):
                i += 1
            else:
                # Match failed.
                #print 'Matched failed in Base'
                return oldi
    return replace(dna, i, t, e)
    
def replace(dna, pos, tpl, e):
    #print 'Replace ', tpl, e
    r = []
    for t in tpl:
        if isinstance(t, int):
            # |n|
            if (t >= len(e)):
                r.extend(asnat(0))
            else:
                r.extend(asnat(len(e[t])))
        elif isinstance(t, tuple):
            # n(l)
            l, n = t
            if (n >= len(e)):
                r.extend(protect(l, []))
            else:
                r.extend(protect(l, e[n]))
        else:
            # Base
            r.append(t)
    try:
        dna[0:pos] = r
    except:
        print pos, dna[pos:pos+100]
        raise
    return 0
    
def protect(l, d):
    for ix in range(l):
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
            p, pos = pattern(dna, pos, rna)
            assert(isinstance(dna, list))
            t, pos = template(dna, pos, rna)
            assert(isinstance(dna, list))
            #print p, t
            pos = matchreplace(dna, p, t, pos)
            if progress:
                print 'Iterations: ' + str(n) + '   DNA remaining: ' + str(len(dna)), '   RNA commands: ' + str(len(rna) / 7)
        except AssertionError:
            print pos
        except NoMoreData:
            break
    return dna

if __name__ == '__main__':
    prefix = []
    if len(sys.argv) > 3:
        prefixfile = file(sys.argv[3], 'r')
        prefix = list(prefixfile.read())
        prefixfile.close()
    if len(sys.argv) > 2:
        dnafile = file(sys.argv[1], 'r')
        dna = prefix + list(dnafile.read())
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
            dna = list(dnastr)
            p, pos = pattern(dna, 0, rna)
            print dnastr + ' -> ' + ''.join(p)
        print ''
        print ''
        print 'Test dna execution function:'
        print ''
        for dnastr in ['IIPIPICPIICICIIFICCIFPPIICCFPC', 'IIPIPICPIICICIIFICCIFCCCPPIICCFPC', 'IIPIPIICPIICIICCIICFCFC']:
            dna = list(dnastr)
            rna = []
            dna = execute(dna, rna)
            print dnastr + ' -> ' + ''.join(dna)