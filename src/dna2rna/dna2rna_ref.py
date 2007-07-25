import sys
#from rna2fuun.rna2fuun import commands as rnacommands
#import array
import dnareflist
import os
import time

class NoMoreData(Exception):
    pass

# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
# The 'rna' parameter is also modified during the process.
def pattern(dna, rna):
    p = []
    lvl = 0
    pa = p.append
    dp = dna.popfront
    dpr = dna.popfrontret
    ra = rna.append
    btmp = []
    while True:
        dnastr = dna[0:3]
        try:
            d = dnastr[0]
            if d == 'C':    # C
                dp()
                btmp.append('I')
            elif d == 'F':  # F
                dp()
                btmp.append('C')
            elif d == 'P':  # P
                dp()
                btmp.append('F')
            elif d == 'I':
                d = dnastr[1]
                if d == 'C':    # IC
                    dp(2)
                    btmp.append('P')
                elif d == 'P':  # IP
                    dp(2)
                    n = nat(dna)
                    if btmp:
                        pa(btmp)
                        btmp = []
                    pa('!%d'%n)
                elif d == 'F':  # IF
                    dp(3) # NOTE: Three bases consumed here.
                    if btmp:
                        pa(btmp)
                        btmp = []
                    pa('?%s'%(''.join(consts(dna)),))
                elif d == 'I':
                    d = dnastr[2]
                    if d == 'P':    # IIP
                        dp(3)
                        lvl += 1
                        if btmp:
                            pa(btmp)
                            btmp = []
                        pa('(')
                    elif d == 'C' or d == 'F': # IIC, IIF
                        dp(3)      
                        if btmp:
                            pa(btmp)
                            btmp = []
                        if lvl == 0:
                            return p
                        else:
                            lvl -= 1
                            pa(')')
                    elif d == 'I':  # III
                        # Add rna command.
                        # Add rna command.
                        rnacmd = dpr(10)[3:]
                        ra(rnacmd)
        except IndexError:
            raise NoMoreData
    return


# Extracts a template from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the template and a new position after the
# consumed bases: (template, pos)
# The 'rna' parameter is also modified during the process.
def template(dna, rna):
    t = []
    ta = t.append
    dp = dna.popfront
    dpr = dna.popfrontret
    ra = rna.append
    btmp = []
    while True:
        dnastr = dna[0:3]
        try:
            d = dnastr[0]
            if d == 'C':
                dp()
                btmp.append('I')
            elif d == 'F':
                dp()
                btmp.append('C')
            elif d == 'P':
                dp()
                btmp.append('F')
            elif d == 'I':
                d = dnastr[1]
                if d == 'C':
                    dp(2)
                    btmp.append('P')
                elif d == 'F' or d == 'P':
                    dp(2)
                    l = nat(dna)
                    n = nat(dna)
                    if btmp:
                        ta(btmp)
                        btmp = []
                    ta((l, n))
                elif d == 'I':
                    d = dnastr[2]
                    if d == 'P':
                        dp(3)
                        n = nat(dna)
                        if btmp:
                            ta(btmp)
                            btmp = []
                        ta(n)
                    elif d == 'C' or d == 'F':
                        dp(3)      
                        if btmp:
                            ta(btmp)
                            btmp = []
                        return t
                    elif d == 'I':
                        # Add rna command.
                        # Add rna command.
                        rnacmd = dpr(10)[3:]
                        ra(rnacmd)
        except IndexError:
            # Exit
            raise NoMoreData
    return


# Extracts a natural number from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the number and a new position after the
# consumed bases: (number, pos)
def nat(dna):
    ret = 0
    p = 0
    while True:
        try:
            d = dna.popfrontret(1)[0]
            if (d == 'P'):
                return ret
            elif d == 'I' or d == 'F':
                p += 1
            elif d == 'C':
                ret += 1 << p
                p += 1
        except IndexError:
            raise NoMoreData
    
    
        
# Extracts a base sequence from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the sequence and a new position after the
# consumed bases: (sequence, pos)
def consts(dna):
    seq = []
    dp = dna.popfront
    while True:
        dnastr = dna[0:2]
        d = dnastr[0]
        if d == 'C':
            dp()
            seq.append('I')
        elif d == 'F':
            dp()
            seq.append('C')
        elif d == 'P':
            dp()
            seq.append('F')
        elif d == 'I':
            d = dnastr[1]
            if d == 'C':
                dp(2)
                seq.append('P')
            else:
                return seq
    
# Modifies 'dna' by applying template 't' to matching items in pattern 'pat'.
# The matching starts at position 'i'.
def matchreplace(dna, pat, t):
    e = []
    c = []
    i = 0
    ld = len(dna)
#    print "pattern", ''.join(pat)
#    print
#    print "template", t
#    print
#    print dna[0:10]
    for p in pat:
        pp = p[0]
        if pp == '!':
            n = int(p[1:])
            i += n
            if (i > ld):
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
#            print e[-1]
#            print "e[%d]:"%(len(e)-1,), dna[e[-1].start: min(e[-1].start+10, e[-1].stop)]
        else:
            # Base
            lp = len(p)
            if (dna[i:i+lp] == p):
                i += lp
            else:
                # Match failed.
                return
    replace(dna, t, e, i)
#    print dna[0:10], len(dna)
    
def replace(dna, tpl, e, i):
    r = []
    tmp = []
    le = len(e)
    dr = dnareflist.DNARef
    dgri = dna.getreflistiter
    ra = r.append
    re = r.extend
    for t in tpl:
        if isinstance(t, int):
            # |n|
            if (t >= le):
                tmp.extend(asnat(0))
            else:
                a = e[t]
                tmp.extend(asnat(a.stop-a.start))
        elif isinstance(t, tuple):
            # n(l)
            l, n = t
            if (n >= le):
                pass
            else:
                a = e[n]
                if l == 0:
                    if tmp:
                        ra(dr(0, len(tmp), tmp))
                    tmp = []
                    re(dgri(a.start, a.stop))
                else:
                    tmp.extend(protect(l, dna[a.start:a.stop]))
        else:
            # Base
            tmp.extend(t)

    if tmp:
        ra(dr(0, len(tmp), tmp))
        
#    for rr in r:
#        print "ref:", rr.start, rr.stop, len(rr)
    dna.popfront(i)
    dna.insertfront(r)    
#    for rr in dna.list:
#        print "after:", rr.start, rr.stop, len(rr)
#    print dna[0:10], len(dna)
    
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
    
    now = time.time() 
   
    while True:
        n += 1
        try:
            p = pattern(dna, rna)
            t = template(dna, rna)
            matchreplace(dna, p, t)
#            if n == 5000:
#                break
            if progress and ((n % 1000) == 0 or n == 1):
                print 'Iterations: ' + str(n) + '   DNA remaining: ' + str(len(dna)), '   RNA commands: ' + str(len(rna)), "List size:", len(dna.list)
#            if (n % 50000) == 0:
#                print "Saving RNA..."
#                rnafile = file(rnadir+os.path.sep+"tmp_%08d.rna"%n, 'w')
#                for r in rna:
#                    rnafile.write(''.join(r))
#                rnafile.close()

        except NoMoreData:
            print 'DNA remaining: ' + str(len(dna))
            break
    print "execute finished in:", time.time()-now, "seconds"

def main():
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
        dna.insertfront([dnareflist.DNARef(0, len(dnastr), list(dnastr))])
        dnafile.close()
        rna = []
        try:
            execute(dna, rna, True)
        except KeyboardInterrupt:
            print "Interrupted!"
            pass
        print "Saving RNA file of length:", len(rna)
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

if __name__ == '__main__':
    main()
