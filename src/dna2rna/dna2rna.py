# Extracts a pattern from the list 'dna', starting at position 'pos'.
# Returns tuple containing the pattern and a new position after the
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

if __name__ == '__main__':
    dnastr = 'CIIC'
    dna = list(dnastr)
    p, pos = pattern(dna, 0)
    print dnastr + ' -> ' + ''.join(p)