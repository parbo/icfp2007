# -*- coding: utf-8 -*-

import Image
import ImageColor
import functools

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

bucket = []
position = (0, 0)
mark = (0, 0)
dir = E

def c2p(c, alpha):
    return c + tuple(alpha)

def empty():
    return Image.new(mode, size, c2p(black, transparent))

bitmaps = [empty()]

def splitrna(rna):
    for i in xrange(len(rna), 7):
        yield rna[i:i+7] 
    
def addColor(c):
    bucket.insert(c, 0)
    
def emptyBucket():
    bucket = []
    
def getComponentIter(component):
    for i in bucket:
        yield i[component]
    
def average(component, default):
    if bucket:
        if component < 3:
            return sum([c[component] for c in bucket if isinstance(c, tuple)])/len(bucket)
        else:
            return sum([c for c in bucket if isinstance(c, int)])/len(bucket)
    else:
        return default

def currentPixel():
    rc = average(bucket, 0, 0)
    gc = average(bucket, 1, 0)
    bc = average(bucket, 2, 0)
    ac = average(bucket, 3, 255)
    return (rc*ac/255, gc*ac/255, bc*ac/255, ac)

def move(pos, d):
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
    return (d - 1) % 4

def turnCounterClockwise(d):
    return (d + 1) % 4

def getPixel(p):
    return bitmaps[0].getPixel(p)

def setPixel(p):
    bitmaps[0].putPixel(p, currentPixel())

def setPixelVal(p, val):
    bitmaps[0].putPixel(p, val)

def line(start, stop):
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
        setPixelVal(x/d, y/d, cp)
        x = x + deltax
        y = y + deltay
    setPixelVal(x1, y1, cp)
    
def fill(pos, initial):
    if getPixel(pos) == initial:
        setPixel(pos)
    x, y = pos
    if x > 0:
        fill((x - 1, y ), initial)
    if x < 599:
        fill((x + 1, y ), initial)
    if y > 0:
        fill((x , y - 1), initial)
    if y < 599:
        fill((x , y + 1), initial)

def tryfill():
    newp = currentPixel()
    oldp = getPixel(position)
    if newp != oldp:
        fill(position, oldp)
        
def addBitmap(b):
    if len(bitmaps) < 10:
        bitmaps.insert(b, 0)
        
def compose():
    if len(bitmaps) > 2:
        for y in xrange(600):
            for x in xrange(600):
                r0, g0, b0, a0 = bitmaps[0].getPixel((x,y))
                r1, g1, b1, a1 = bitmaps[1].getPixel((x,y))
                bitmaps[1].putPixel((r0 + (r1 * (255 - a0) / 255),
                                     g0 + (g1 * (255 - a0) / 255),
                                     b0 + (b1 * (255 - a0) / 255),
                                     a0 + (a1 * (255 - a0) / 255)))
        bitmaps.pop(0)
        
def clip():
    if len(bitmaps) > 2:
        for y in xrange(600):
            for x in xrange(600):
                r0, g0, b0, a0 = bitmaps[0].getPixel((x,y))
                r1, g1, b1, a1 = bitmaps[1].getPixel((x,y))
                bitmaps[1].putPixel((r1 * a0 / 255,
                                     g1 * a0 / 255,
                                     b1 * a0 / 255,
                                     a1 * a0 / 255))
        
def build(filename):
    f = open(filename)
    rna = splitrna(f.read())
    f.close()
    
    doMove = lambda: position = move(position, dir)
    doTurnCCW = lambda: dir = turnCounterClockwise(dir)
    doTurnCW = lambda: dir = turnClockwise(dir)
    doMark = lambda: mark = position
    
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
        'PFFICCP' : functools.partial(line, position, mark),
        'PIIPIIP' : tryfill,
        'PCCPFFP' : functools.partial(addBitmap, empty()),
        'PFFPCCP' : compose,
        'PFFICCF' : clip}
    
    for r in rna:
        try:
            d[r]()
        except KeyError:
            pass
            
    Image.save(filename+".png", "PNG")

if __name__=="__main__":
    import sys
    build(sys.argv[1])