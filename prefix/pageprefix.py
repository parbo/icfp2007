import sys

def pageprefix(page):
    bitlist = []
    while (page > 0):
        if (page % 2 == 0):
            bitlist.append('C')
        else:
            bitlist.append('F')
        page /= 2
    pagetag = ''.join(bitlist)
    return 'IIPIFFCPICFPPICIIC' + len(pagetag) * 'C' + 'IICIPPP' + pagetag + 'IIC'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        page = int(sys.argv[1])
        outfile = file('repairguide_' + str(page) + '.dna', 'w')
        p = pageprefix(page)
        print p
        outfile.write(p)
        outfile.close()