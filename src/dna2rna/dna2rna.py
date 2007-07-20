# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
def pattern(dna, pos):
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
            pass
        else:
            # Exit
            pass
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
        pass
        
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
        

if __name__ == '__main__':
    for dnastr in ['CIIC', 'IIPIPICPIICICIIF']:
        dna = list(dnastr)
        p, pos = pattern(dna, 0)
        print dnastr + ' -> ' + ''.join(p)