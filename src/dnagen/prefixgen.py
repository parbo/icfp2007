ACTBEGIN = "IIPIFFCPICCFPICICFFFIIPIFFCPICCFPICICFFFIICIICIICIPPP"
ACTEND   = "IPPCPIIC"

PUSHBEGIN = "IIPIFFCPICCFPICICFPCICICIICIICIIPPP"
PUSHEND   = "IIC"

genes = {
    "AAA_geneTablePageNr" : (0x000510, 0x000018),
    "M-class-planet"      : (0x2ccd88, 0x03c7f0),
    "__array_index"       : (0x0c4589, 0x000018),
    "__array_value"       : (0x0c45a1, 0x000018)
}


bstr_pos = lambda n: n>0 and bstr_pos(n>>1)+str(n&1) or ''
bd = {'0' : 'C', '1' : 'F'}
def integer(i, fill=0):
    ibin = [bd[b] for b in bstr_pos(i)]
    ibin.reverse()
    if fill:
        ibin.extend((fill-len(ibin))*['C'])
    ibin.extend(['I', 'C'])
    return ''.join(ibin)    

def boolean(b):
    if b:
        return "CP"
    else:
        return "P"
    
def push(d):
    if isinstance(d, int) and not isinstance(d, bool):
        return PUSHBEGIN + integer(d, 24) + PUSHEND
    elif isinstance(d, bool):
        return PUSHBEGIN + boolean(d) + PUSHEND
        
        
def activate(offset, len):
    return ACTBEGIN + integer(offset) + integer(len) + ACTEND
    

def activatename(name):
    offset, len = genes[name]
    return activate(offset, len)    

if __name__=="__main__":
    print activate(1234, 500)
    print push(42)
    print push(True)
    print push(False)
    print activatename("M-class-planet")
    
    