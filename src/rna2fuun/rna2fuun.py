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

def build(filename):
    f = open(filename)
    rna = f.read()
    f.close()
    
    for r in rna:
182 case r is of the form
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