import sys
#from rna2fuun.rna2fuun import commands as rnacommands
#import array
import dnareflist
import os

class NoMoreData(Exception):
    pass

# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
# The 'rna' parameter is also modified during the process.
def pattern(dna, rna):
    p = []
    lvl = 0
    while True:
        dnastr = ''.join(dna[0:3])
        if dnastr.startswith('C'):
            dna.popfront()            
            p.append('I')
        elif dnastr.startswith('F'):
            dna.popfront()
            p.append('C')
        elif dnastr.startswith('P'):
            dna.popfront()
            p.append('F')
        elif dnastr.startswith('IC'):
            dna.popfront(2)
            p.append('P')
        elif dnastr.startswith('IP'):
            dna.popfront(2)
            n = nat(dna)
            p.append('!' + str(n))
        elif dnastr.startswith('IF'):
            dna.popfront(3) # NOTE: Three bases consumed here.
            s = consts(dna)
            p.append('?' + ''.join(s))
        elif dnastr.startswith('IIP'):
            dna.popfront(3)
            lvl += 1
            p.append('(')
        elif dnastr.startswith('IIC') or dnastr.startswith('IIF'):
            dna.popfront(3)
            if lvl > 0:
                lvl -= 1
                p.append(')')
            else:
                return p
        elif dnastr.startswith('III'):
            # Add rna command.
            rnacmd = dna[3:10]
            dna.popfront(10)
            rna.append(rnacmd)
        else:
            # Exit
            print "N more data!" #, len(dna), dna[0:3]
            raise NoMoreData
    return


# Extracts a template from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the template and a new position after the
# consumed bases: (template, pos)
# The 'rna' parameter is also modified during the process.
def template(dna, rna):
    t = []
    while True:
        dnastr = ''.join(dna[0:3])
        if dnastr.startswith('C'):
            dna.popfront()
            t.append('I')
        elif dnastr.startswith('F'):
            dna.popfront()
            t.append('C')
        elif dnastr.startswith('P'):
            dna.popfront()
            t.append('F')
        elif dnastr.startswith('IC'):
            dna.popfront(2)
            t.append('P')
        elif dnastr.startswith('IF') or dnastr.startswith('IP'):
            dna.popfront(2)
            l = nat(dna)
            n = nat(dna)
            t.append((l, n))
        elif dnastr.startswith('IIP'):
            dna.popfront(3)
            n = nat(dna)
            t.append(n)
        elif dnastr.startswith('IIC') or dnastr.startswith('IIF'):
            dna.popfront(3)      
            return t
        elif dnastr.startswith('III'):
            # Add rna command.
            # Add rna command.
            rnacmd = dna[3:10]
            dna.popfront(10)
            rna.append(rnacmd)
        else:
            # Exit
            raise NoMoreData
    return


# Extracts a natural number from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the number and a new position after the
# consumed bases: (number, pos)
def nat(dna):
    dnastr = ''.join(dna[0:1])
    dna.popfront()
    if (dnastr == 'P'):
        return 0
    elif (dnastr == 'I') or (dnastr == 'F'):
        n = nat(dna)
        return 2 * n
    elif (dnastr == 'C'):
        n = nat(dna)
        return 2 * n + 1
    else:
        # Empty -> Exit
        raise NoMoreData
    
    
        
# Extracts a base sequence from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the sequence and a new position after the
# consumed bases: (sequence, pos)
def consts(dna):
    def constsrec(dna):
        dnastr = ''.join(dna[0:2])
        if dnastr.startswith('C'):
            dna.popfront()
            seq = constsrec(dna)
            seq.append('I')
            return seq
        elif dnastr.startswith('F'):
            dna.popfront()
            seq = constsrec(dna)
            seq.append('C')
            return seq
        elif dnastr.startswith('P'):
            dna.popfront()
            seq = constsrec(dna)
            seq.append('F')
            return seq
        elif dnastr.startswith('IC'):
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
    for p in pat:
        pp = p[0]
        if pp == '!':
            n = int(p[1:])
            i += n
            if (i > len(dna)):
                # Match failed.
                return
        elif pp == '?':
            substr = p[1:]
            n = dna.find(substr, i)
            if n >= 0:
                i = n + len(substr)
            else:
                # Match failed.
                return
        elif pp == '(':
            c.append(i)
        elif pp == ')':
            e.append(slice(c.pop(),i))
        else:
            # Base
            if (dna[i] == pp):
                i += 1
            else:
                # Match failed.
                return
    replace(dna, t, e, i)
    
def replace(dna, tpl, e, i):
    r = []
    tmp = []
    for t in tpl:
        if isinstance(t, int):
            # |n|
            if (t >= len(e)):
                tmp.extend(asnat(0))
            else:
                tmp.extend(asnat(e[t].stop-e[t].start))
        elif isinstance(t, tuple):
            # n(l)
            l, n = t
            if (n >= len(e)):
                pass
            else:
                if l == 0:
                    r.append(dnareflist.DNARef(0, len(tmp), tmp))
                    tmp = []
                    a = e[n]
                    r.append(dnareflist.DNARef(a.start, a.stop))
                else:
                    tmp.extend(protect(l, dna[e[n].start:e[n].stop]))
        else:
            # Base
            tmp.append(t)

    if tmp:
        r.append(dnareflist.DNARef(0, len(tmp), tmp))
        
    r.reverse()
    dna.insertfrontreflistandpopold(r, i)    
    
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
    
    rnadir = os.getcwd()+os.path.sep+"rna"
    if not os.path.exists(rnadir):
        os.mkdir(rnadir)
    
    while True:
        n += 1
        try:
            p = pattern(dna, rna)
            t = template(dna, rna)
            matchreplace(dna, p, t)
            if progress: #and (n % 100) == 0:
                print 'Iterations: ' + str(n) + '   DNA remaining: ' + str(len(dna)), '   RNA commands: ' + str(len(rna)), "List size:", len(dna.list)
            if (n % 50000) == 0:
                print "Saving RNA..."
                rnafile = file(rnadir+os.path.sep+"tmp_%08d.rna"%n, 'w')
                for r in rna:
                    rnafile.write(''.join(r))
                rnafile.close()

        except NoMoreData:
            print 'DNA remaining: ' + str(len(dna))
            break

if __name__ == '__main__':
    import psyco
    psyco.full()
    
    prefix = ""
    if len(sys.argv) > 3:
        prefixfile = file(sys.argv[3], 'r')
        prefix = prefixfile.read()
        prefixfile.close()
    if len(sys.argv) > 2:
        dnafile = file(sys.argv[1], 'r')
        dnastr = prefix + dnafile.read()
        dna = dnareflist.DNAList()
        dna.insertfront(dnareflist.DNARef(0, len(dnastr), list(dnastr)))
        dnafile.close()
        rna = []
        try:
            execute(dna, rna, True)
        except KeyboardInterrupt:
            rnafile = file(sys.argv[2], 'w')
            for r in rna:
                rnafile.write(''.join(r))
            rnafile.close()
            sys.exit(1)
        rnafile = file(sys.argv[2], 'w')
        for r in rna:
            rnafile.write(''.join(r))
        rnafile.close()
        
    else:
        # Run tests
        print ''
        print 'Test pattern function:'
        print ''
        for dnastr in ['CIIC', 'IIPIPICPIICICIIF']:
            rna = []
            dna = dnareflist.DNAList()
            dna.insertfront(dnareflist.DNARef(0, len(dnastr), dnastr))
            p = []
            try:
                p = pattern(dna, rna)
            except NoMoreData:
                print 'DNA remaining: ' + str(len(dna))
                pass
            print dnastr + ' -> ' + ''.join(p)
        print ''
        print ''
        print 'Test dna execution function:'
        print ''
        for dnastr in ['IIPIPICPIICICIIFICCIFPPIICCFPC', 'IIPIPICPIICICIIFICCIFCCCPPIICCFPC', 'IIPIPIICPIICIICCIICFCFC']:
            dna = dnareflist.DNAList()
            dna.insertfront(dnareflist.DNARef(0, len(dnastr), dnastr))
            rna = []
            execute(dna, rna)
            print dnastr + ' -> ' + ''.join(dna)
