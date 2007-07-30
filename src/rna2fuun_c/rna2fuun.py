# -*- coding: utf-8 -*-

import sys
import Image
import rna2fuun_c
    
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

def splitrna(rna):
    for i in xrange(0, len(rna), 7):
        yield rna[i:i+7] 

def read(filename):
    f = open(filename)
    rna = list(splitrna(f.read()))
    f.close()
    return rna
              
def save(r2f, filename):
    getPILImage(r2f).save(filename, "PNG")
    
def build(r2f, filename):   
    rna = read(filename) 
    for r in rna:
        r2f.buildstep(r)
    save(r2f, filename+".png")

def getPILImage(r2f):
    return Image.frombuffer("RGBA", (600, 600), r2f.getImage(), "raw", "RGBA", 0, 1)


if __name__=="__main__":
    r2f = rna2fuun_c.rna2fuun()
    build(r2f, sys.argv[1])
