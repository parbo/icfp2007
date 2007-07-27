bstr_pos = lambda n: n>0 and bstr_pos(n>>1)+str(n&1) or ''
bd = {'0' : 'C', '1' : 'F'}
def integer(i):
    ibin = [bd[b] for b in bstr_pos(i)]
    ibin.reverse()
    ret = ''.join(ibin)
    print "integer", i, ret, len(ret)
    return ret

if __name__=="__main__":
    pre = "IIPIFFCPICFPPICIIC"
    mid = "IICIPPP"
    post = "IIC"
    import sys
    import os

    pdir = os.getcwd()+os.path.sep+"prefix"
    if not os.path.exists(pdir):
        os.mkdir(pdir)

    for i in range(int(sys.argv[1])):
        f = open(pdir + os.path.sep + "repairguide_%04d.dna"%i, "w")
        f.write(pre)
        num = integer(i)
        f.write("C"*len(num))
        f.write(mid)
        f.write(num)
        f.write(post)
        f.close()


