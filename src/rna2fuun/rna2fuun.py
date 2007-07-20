# -*- coding: utf-8 -*-

import Image
import ImageColor

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
    bitmaps[0].setPixel(p, currentPixel())

def setPixelVal(p, val):
    bitmaps[0].setPixel(p, val)

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

def build(filename):
    f = open(filename)
    rna = splitrna(f.read())
    f.close()
    

    
    for r in rna:
        if r == 
case r is of the form
183 ‘PIPIIIC’ ) addColor (black rgb)
184 ‘PIPIIIP’ ) addColor (red rgb)
185 ‘PIPIICC’ ) addColor (green rgb)
186 ‘PIPIICF’ ) addColor (yellow rgb)
187 ‘PIPIICP’ ) addColor (blue rgb)
188 ‘PIPIIFC’ ) addColor (magenta rgb)
189 ‘PIPIIFF’ ) addColor (cyan rgb)
190 ‘PIPIIPC’ ) addColor (white rgb)
191 ‘PIPIIPF’ ) addColor (transparent a)
192 ‘PIPIIPP’ ) addColor (opaque a)
193 ‘PIIPICP’ ) bucket   #
194 ‘PIIIIIP’ ) position   move (position, dir)
195 ‘PCCCCCP’ ) dir   turnCounterClockwise (dir)
196 ‘PFFFFFP’ ) dir   turnClockwise (dir)
197 ‘PCCIFFP’ ) mark   position
198 ‘PFFICCP’ ) line (position, mark)
199 ‘PIIPIIP’ ) tryfill ()
200 ‘PCCPFFP’ ) addBitmap (transparentBitmap)
201 ‘PFFPCCP’ ) compose ()
202 ‘PFFICCF’ ) clip ()
203 anything else ) do nothing
204 end case
205 end foreach
206 draw bitmaps[0] all alpha values are set to 255!
207 exit
Figure 19: Building a Fuun from RNA
resulting image is determined by the RGB values of bitmaps[0]. The transparency values of
bitmaps[0] are ignored and all set to opaque (255) for drawing.
The known RNA commands can be sorted into four groups: commands that affect the
bucket, commands that change the focus, commands that draw, and commands that affect
the sequence of bitmaps. Each of the command groups is discussed in detail below.
4.3 Bucket commands
For each of the eight predefined colors and the two predefined transparency values, there
is an RNA command that prepends the Color to the bucket, using the procedure addColor in
Figure 20. The instruction ‘PIIPICP’ empties the bucket.
The bucket encodes information about a pixel, i.e., a current color and transparency
value. The function currentPixel, also in Figure 20, can be used to determine this value of
type Pixel.
14    pass


if __name__=="__main__":
    import sys
    build(sys.argv[1])