import sys

commands = {
    'PIPIIIC' : "addColor, black",
    'PIPIIIP' : "addColor, red",
    'PIPIICC' : "addColor, green",
    'PIPIICF' : "addColor, yellow",
    'PIPIICP' : "addColor, blue",
    'PIPIIFC' : "addColor, magenta",
    'PIPIIFF' : "addColor, cyan",
    'PIPIIPC' : "addColor, white",
    'PIPIIPF' : "addColor, transparent",
    'PIPIIPP' : "addColor, opaque",
    'PIIPICP' : "emptyBucket",
    'PIIIIIP' : "move",
    'PCCCCCP' : "turnCCW",
    'PFFFFFP' : "turnCW",
    'PCCIFFP' : "mark",
    'PFFICCP' : "line",
    'PIIPIIP' : "tryfill",
    'PCCPFFP' : "addBitmap",
    'PFFPCCP' : "compose",
    'PFFICCF' : "clip"}


def preprocess(rna):
    ix = 0
    prerna = []
    move = 0
    while (ix < len(rna)):
        cmd = rna[ix:ix+7]
        ix += 7
        if cmd in commands:
            if (cmd == 'PIIIIIP'):
                # Move
                move += 1
            else:
                if (move > 0):
                    prerna.append('move ' + str(move))
                    move = 0
                prerna.append(cmd)
    return '\n'.join(prerna)
    

if __name__ == '__main__':
    if (len(sys.argv) > 2):
        infile = file(sys.argv[1], 'r')
        outfile = file(sys.argv[2], 'w')
        outfile.write(preprocess(infile.read()))
        infile.close()
        outfile.close()
        