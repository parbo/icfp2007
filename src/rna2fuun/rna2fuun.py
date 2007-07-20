# -*- coding: utf-8 -*-

import sys
import Image
import ImageColor
import functools

    
sys.setrecursionlimit(600*600)

mode = 'RGBA'
size = (600, 600)
black = (0 , 0 , 0)
red = (255, 0 , 0)
green = (0 , 255, 0)
yellow = (255, 255, 0)
blue = (0 , 0 , 255)
magenta = (255, 0 , 255)
cyan = (0, 255, 255)
white = (255, 255, 255)
transparent = 0
opaque = 255

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

E, S, W, N = 0, 1, 2, 3

dstr = {E:"East", S:"South", W:"West", N:"North"}
def d2str(d):
    return dstr[d]

def c2p(c, alpha):
    a = (alpha,)
    return c + a

def splitrna(rna):
    for i in xrange(0, len(rna), 7):
        yield rna[i:i+7] 

def read(filename):
    f = open(filename)
    rna = splitrna(f.read())
    f.close()
    return rna

class rna2fuun(object):

    def __init__(self):
        self.debug = False
        self.reset()

    def reset(self):
        self.bucket = []
        self.position = (0, 0)
        self.mark = (0, 0)
        self.dir = E
        self.bitmaps = []
        self.addBitmap()
    
    def addColor(self, c):
        if self.debug: 
            print "Adding colour:", c
        self.bucket.insert(0, c)
    
    def emptyBucket(self):
        if self.debug: 
            print "Emptying bucket"
        self.bucket = []
    
    def averageColor(self, default):
        rc = 0
        gc = 0
        bc = 0
        colbucket = [c for c in self.bucket if isinstance(c, tuple)]
        if colbucket:
            for c in colbucket:
                r, g, b = c
                rc += r 
                gc += g 
                bc += b
            lencb = len(colbucket)
            return (rc/lencb, gc/lencb, bc/lencb)
        else:
            return (default, default, default)

    def averageAlpha(self, default):
        abucket = [c for c in self.bucket if isinstance(c, int)]
        if abucket:
            return sum(abucket)/len(abucket)
        else:
            return default
    
    def currentPixel(self):
        rc, gc, bc = self.averageColor(0)
        ac = self.averageAlpha(255)
        return (rc*ac/255, gc*ac/255, bc*ac/255, ac)

    def move(self):
        if self.debug: 
            print "Move: ", self.position, d2str(self.dir)
        x, y = self.position
        if self.dir == N:
            self.position = (x , (y - 1) % 600)
        elif self.dir == E:
            self.position = ((x + 1) % 600, y )
        elif self.dir == S:
            self.position = (x , (y + 1) % 600)
        elif self.dir == W:
            self.position = ((x - 1) % 600, y )
        else:
            raise "Unknown direction"

    def turnCounterClockwise(self):
        if self.debug: 
            print "Turn CCW: ", d2str(self.dir)
        self.dir = (self.dir - 1) % 4

    def turnClockwise(self):
        if self.debug: 
            print "Turn CW: ", d2str(self.dir)
        self.dir = (self.dir + 1) % 4

    def getPixel(self, p):
        return self.bitmaps[0][1][p]

    def setPixel(self, p):
        self.bitmaps[0][1][p] = self.currentPixel()

    def setPixelVal(self, p, val):
        self.bitmaps[0][1][p] = val

    def line(self, start, stop):
        if self.debug: 
            print "Line:", start, stop
        x0, y0 = start
        x1, y1 = stop
        deltax = x1 - x0
        deltay = y1 - y0
        d = max(abs(deltax), abs(deltay))
        
        if (deltax * deltay) >= 0:
            c = 1 
        else:
            c = 0
            
        x = x0 * d + (d - c)/2 
        y = y0 * d + (d - c)/2
        cp = self.currentPixel() 
        for i in xrange(d):
            self.setPixelVal((x/d, y/d), cp)
            x = x + deltax
            y = y + deltay
        self.setPixelVal((x1, y1), cp)
    
    def fillScanline(self, pos, oldp, newp):
        if getPixel(pos) != oldp:
            return   
        
    ##    if self.debug: 
    ##        print "Fill scanline: ", pos, oldp, newp
            
        x, y = pos
        w, h = size
        
        # draw current scanline from start position to the top
        y1 = y
        while y1 < h and self.getPixel((x, y1)) == oldp:
            self.setPixelVal((x, y1), newp)
            y1 += 1
           
        # draw current scanline from start position to the bottom
        y1 = y - 1
        while y1 >= 0 and self.getPixel((x, y1)) == oldp:
            self.setPixelVal((x, y1), newp)
            y1 -= 1
        
        # test for new scanlines to the left
        y1 = y
        while y1 < h and self.getPixel((x, y1)) == newp:
            if x > 0 and self.getPixel((x - 1, y1)) == oldp:
                self.fillScanline((x - 1, y1), oldp, newp)
            y1 += 1
        y1 = y - 1
        while y1 >= 0 and self.getPixel((x, y1)) == newp:
            if x > 0 and self.getPixel((x - 1, y1)) == oldp:
                self.fillScanline((x - 1, y1), oldp, newp)
            y1 -= 1
        
        # test for new scanlines to the right 
        y1 = y
        while y1 < h and self.getPixel((x, y1)) == newp:
            if x < w - 1 and self.getPixel((x + 1, y1)) == oldp:
                self.fillScanline((x + 1, y1), oldp, newp)
            y1 += 1
        y1 = y - 1
        while y1 >= 0 and self.getPixel((x, y1)) == newp:
            if x < w - 1 and self.getPixel((x + 1, y1)) == oldp:
                self.fillScanline((x + 1, y1), oldp, newp)
            y1 -= 1
    
    def tryfill(self):
        newp = self.currentPixel()
        oldp = self.getPixel(position)
        if self.debug: 
            print "Fill: ", self.position, oldp, newp
        if newp != oldp:
            self.fillScanline(self.position, oldp, newp)
        
    def addBitmap(self):
        if self.debug: 
            print "Add bitmap"
        if len(self.bitmaps) < 10:
            b = Image.new(mode, size, c2p(black, transparent))
            self.bitmaps.insert(0, (b, b.load()))
        
    def compose(self):
        if self.debug: 
            print "Compose"
        if len(self.bitmaps) > 2:
            bm0 = self.bitmaps[0][1]
            bm1 = self.bitmaps[1][1]
            for y in xrange(600):
                for x in xrange(600):
                    r0, g0, b0, a0 = bm0[x,y]
                    r1, g1, b1, a1 = bm1[x,y]
                    bm1[x, y] = (r0 + (r1 * (255 - a0) / 255),
                                g0 + (g1 * (255 - a0) / 255),
                                b0 + (b1 * (255 - a0) / 255),
                                a0 + (a1 * (255 - a0) / 255))
            self.bitmaps.pop(0)
        
    def clip():
        if self.debug: 
            print "Clip"
        if len(self.bitmaps) > 2:
            bm0 = self.bitmaps[0][1]
            bm1 = self.bitmaps[1][1]
            for y in xrange(600):
                for x in xrange(600):
                    r0, g0, b0, a0 = bm0[x,y]
                    r1, g1, b1, a1 = bm1[x,y]
                    bm1[x, y] = (r1 * a0 / 255,
                                g1 * a0 / 255,
                                b1 * a0 / 255,
                                a1 * a0 / 255)

    def doMark(self):
        if self.debug: 
            print "Mark:", self.position
        self.mark = self.position
            
    def doLine(self):
        self.line(self.position, self.mark)

    def buildgenerator(self, rna):
        d = {
            'PIPIIIC' : functools.partial(self.addColor, black),
            'PIPIIIP' : functools.partial(self.addColor, red),
            'PIPIICC' : functools.partial(self.addColor, green),
            'PIPIICF' : functools.partial(self.addColor, yellow),
            'PIPIICP' : functools.partial(self.addColor, blue),
            'PIPIIFC' : functools.partial(self.addColor, magenta),
            'PIPIIFF' : functools.partial(self.addColor, cyan),
            'PIPIIPC' : functools.partial(self.addColor, white),
            'PIPIIPF' : functools.partial(self.addColor, transparent),
            'PIPIIPP' : functools.partial(self.addColor, opaque),
            'PIIPICP' : self.emptyBucket,
            'PIIIIIP' : self.move,
            'PCCCCCP' : self.turnCounterClockwise,
            'PFFFFFP' : self.turnClockwise,
            'PCCIFFP' : self.doMark,
            'PFFICCP' : self.doLine,
            'PIIPIIP' : self.tryfill,
            'PCCPFFP' : self.addBitmap,
            'PFFPCCP' : self.compose,
            'PFFICCF' : self.clip}
        
        for r in rna:
            try:
                d[r]()
                yield commands[r]
            except KeyError:
                if debug:
                    print "Unkown instruction:", r
                pass
                
    def save(self, filename):
        self.bitmaps[0][0].save(filename, "PNG")
    
    def build(self, filename):   
        rna = read(filename) 
        g = self.buildgenerator(rna)
        for x in g:
            pass   
        self.save(filename+".png")

if __name__=="__main__":
    #debug = True
    r2f = rna2fuun()
    r2f.build(sys.argv[1])