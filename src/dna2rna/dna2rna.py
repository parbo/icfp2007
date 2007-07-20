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
            pos += 2
            s, pos = consts(dna, pos)
            p.append('?' + s)
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
# Returns a tuple containing the pattern and a new position after the
# consumed bases: (pattern, pos)
def nat(dna, pos):
    dnastr = dna[pos]
    if (dnastr == 'P'):
        pos += 1
        return (0, pos)
    elif (dnastr == 'I') or (dnastr == 'F'):
        pos += 1
        n, pos = nat(dna, pos)
        return (2 * n, pos)
    elif (dnastr == 'C'):
        pos += 1
        n, pos = nat(dna, pos)
        return (2 * n + 1, pos)
    else:
        # Empty -> Exit
        pass
        

if __name__ == '__main__':
    for dnastr in ['CIIC', 'IIPIPICPIICICIIF']:
        dna = list(dnastr)
        p, pos = pattern(dna, 0)
        print dnastr + ' -> ' + ''.join(p)