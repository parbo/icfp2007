# -*- coding: utf-8 -*-

import sys
import Image
import ImageColor
import functools

debug = False

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

    
E, S, W, N = 0, 1, 2, 3

dstr = {E:"East", S:"South", W:"West", N:"North"}
def d2str(d):
    return dstr[d]
    

bucket = []
position = (0, 0)
mark = (0, 0)
dir = E

def c2p(c, alpha):
    a = (alpha,)
    return c + a

def empty():
    return Image.new(mode, size, c2p(black, transparent))

bitmaps = [empty()]

def splitrna(rna):
    for i in xrange(0, len(rna), 7):
        yield rna[i:i+7] 
    
def addColor(c):
    if debug: 
        print "Adding colour:", c
    bucket.insert(0, c)
    
def emptyBucket():
    if debug: 
        print "Emptying bucket"
    bucket = []
    
def getComponentIter(component):
    for i in bucket:
        yield i[component]
    
def averageColor(default):
    rc = 0
    gc = 0
    bc = 0
    colbucket = [c for c in bucket if isinstance(c, tuple)]
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

def averageAlpha(default):
    abucket = [c for c in bucket if isinstance(c, int)]
    if abucket:
        return sum(abucket)/len(abucket)
    else:
        return default
    
def currentPixel():
    rc, gc, bc = averageColor(0)
    ac = averageAlpha(255)
    return (rc*ac/255, gc*ac/255, bc*ac/255, ac)

def move(pos, d):
    if debug: 
        print "Move: ", pos, d2str(d)
    x, y = pos
    if d == N:
        return (x , (y - 1) % 600)
    elif d == E:
        return ((x + 1) % 600, y )
    elif d == S:
        return (x , (y + 1) % 600)
    elif d == W:
        return ((x - 1) % 600, y )
    else:
        raise "Unknown direction"

def turnCounterClockwise(d):
    if debug: 
        print "Turn CCW: ", d2str(d)
    return (d - 1) % 4

def turnClockwise(d):
    if debug: 
        print "Turn CW: ", d2str(d)
    return (d + 1) % 4

def getPixel(p):
    return bitmaps[0].getpixel(p)

def setPixel(p):
    bitmaps[0].putpixel(p, currentPixel())

def setPixelVal(p, val):
    bitmaps[0].putpixel(p, val)

def line(start, stop):
    if debug: 
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
    cp = currentPixel() 
    for i in xrange(d):
        setPixelVal((x/d, y/d), cp)
        x = x + deltax
        y = y + deltay
    setPixelVal((x1, y1), cp)
    

def fillScanline(pos, oldp, newp):
    if getPixel(pos) != oldp:
        return   
    
##    if debug: 
##        print "Fill scanline: ", pos, oldp, newp
        
    x, y = pos
    w, h = size
    
    # draw current scanline from start position to the top
    y1 = y
    while y1 < h and getPixel((x, y1)) == oldp:
        setPixelVal((x, y1), newp)
        y1 += 1
       
    # draw current scanline from start position to the bottom
    y1 = y - 1
    while y1 >= 0 and getPixel((x, y1)) == oldp:
        setPixelVal((x, y1), newp)
        y1 -= 1
    
    # test for new scanlines to the left
    y1 = y
    while y1 < h and getPixel((x, y1)) == newp:
        if x > 0 and getPixel((x - 1, y1)) == oldp:
            fillScanline((x - 1, y1), oldp, newp)
        y1 += 1
    y1 = y - 1
    while y1 >= 0 and getPixel((x, y1)) == newp:
        if x > 0 and getPixel((x - 1, y1)) == oldp:
            fillScanline((x - 1, y1), oldp, newp)
        y1 -= 1
    
    # test for new scanlines to the right 
    y1 = y
    while y1 < h and getPixel((x, y1)) == newp:
        if x < w - 1 and getPixel((x + 1, y1)) == oldp:
            fillScanline((x + 1, y1), oldp, newp)
        y1 += 1
    y1 = y - 1
    while y1 >= 0 and getPixel((x, y1)) == newp:
        if x < w - 1 and getPixel((x + 1, y1)) == oldp:
            fillScanline((x + 1, y1), oldp, newp)
        y1 -= 1

    
def tryfill():
    newp = currentPixel()
    oldp = getPixel(position)
    if debug: 
        print "Fill: ", position, oldp, newp
    if newp != oldp:
        fillScanline(position, oldp, newp)
        
def addBitmap(b):
    if debug: 
        print "Add bitmap"
    if len(bitmaps) < 10:
        bitmaps.insert(0, b)
        
def compose():
    if debug: 
        print "Compose"
    if len(bitmaps) > 2:
        bm0 = bitmaps[0].load()
        bm1 = bitmaps[1].load()
        for y in xrange(600):
            for x in xrange(600):
                r0, g0, b0, a0 = bm0[x,y]
                r1, g1, b1, a1 = bm1[x,y]
                bm1[x, y] = (r0 + (r1 * (255 - a0) / 255),
                            g0 + (g1 * (255 - a0) / 255),
                            b0 + (b1 * (255 - a0) / 255),
                            a0 + (a1 * (255 - a0) / 255))
        bitmaps.pop(0)
        
def clip():
    if debug: 
        print "Clip"
    if len(bitmaps) > 2:
        bm0 = bitmaps[0].load()
        bm1 = bitmaps[1].load()
        for y in xrange(600):
            for x in xrange(600):
                r0, g0, b0, a0 = bm0[x,y]
                r1, g1, b1, a1 = bm1[x,y]
                bm1[x, y] = (r1 * a0 / 255,
                            g1 * a0 / 255,
                            b1 * a0 / 255,
                            a1 * a0 / 255)

def doMove():
    global position
    position = move(position, dir)
    
def doTurnCCW():
    global dir
    dir = turnCounterClockwise(dir)
    
def doTurnCW():
    global dir
    dir = turnClockwise(dir)
    
def doMark():
    if debug: 
        print "Mark:", position
    mark = position
        
def doLine():
    line(position, mark)
    
def build(filename):
    f = open(filename)
    rna = splitrna(f.read())
    f.close()
    
    sys.setrecursionlimit(600*600)
    
    d = {
        'PIPIIIC' : functools.partial(addColor, black),
        'PIPIIIP' : functools.partial(addColor, red),
        'PIPIICC' : functools.partial(addColor, green),
        'PIPIICF' : functools.partial(addColor, yellow),
        'PIPIICP' : functools.partial(addColor, blue),
        'PIPIIFC' : functools.partial(addColor, magenta),
        'PIPIIFF' : functools.partial(addColor, cyan),
        'PIPIIPC' : functools.partial(addColor, white),
        'PIPIIPF' : functools.partial(addColor, transparent),
        'PIPIIPP' : functools.partial(addColor, opaque),
        'PIIPICP' : emptyBucket,
        'PIIIIIP' : doMove,
        'PCCCCCP' : doTurnCCW,
        'PFFFFFP' : doTurnCW,
        'PCCIFFP' : doMark,
        'PFFICCP' : doLine,
        'PIIPIIP' : tryfill,
        'PCCPFFP' : functools.partial(addBitmap, empty()),
        'PFFPCCP' : compose,
        'PFFICCF' : clip}
    
    for r in rna:
        try:
            d[r]()
        except KeyError:
            if debug:
                print "Unkown instruction:", r
            pass
            
    bitmaps[0].save(filename+".png", "PNG")

if __name__=="__main__":
    #debug = True
    build(sys.argv[1])