import Image
import sys

def main(filename, bits):
    im = Image.open(filename)
    imd = im.load()
    imout = Image.new(im.mode, im.size)
    imdout = imout.load()
    mask = (1 << bits) - 1
    scale = 256 / mask
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = imd[x,y]
            imdout[x,y] = (scale * (r & mask), scale * (g & mask),scale * (b & mask), a)
    imout.save(filename + ".out.png", "PNG")
            
if __name__=="__main__":
    main(sys.argv[1], int(sys.argv[2]))
