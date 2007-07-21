class DNARef(object):
    def __init__(self, start, stop, data=None):
        self.data = data
        self.start = start
        self.stop = stop
        
    def __len__(self):
        return self.stop-self.start
    
    def __str__(self):
        if self.data:
            return str(self.data[self.start:self.stop])
        else:
            return "(%d, %d)"%(self.start, self.stop)
    
    def popfront(self, num):
        try:
            assert(self.start + num <= self.stop)
            self.start += num
##            print self.start, num
        except:
            print self.start, self.stop, num
            raise
        
    def __getitem__(self, item):
        try:
            if isinstance(item, int):
                assert(self.start+item < self.stop)
                return self.data[self.start + item]
            elif isinstance(item, slice):    
                if not item.stop :
                    item.stop = len(self)
                assert(self.start+item.start < self.stop)
                assert(self.start+item.stop < self.stop)
                return self.data[self.start+item.start:self.start+item.stop]
        except:
##            print self.start, self.stop, item
            raise
        

class DNAList(object):
    def __init__(self):
        self.list = []
        
    def __str__(self):
        s = []
        for r in reversed(self.list):
            s.append(str(r))
        return "".join(s)
            
        
    def __len__(self):
        length = 0
        for r in self.list:
            length += len(r)
        return length
    
    def popfront(self, num=1):
        n = 0
        for r in reversed(self.list):
            length = len(r)
            if num >= length:
                n+= 1
                num -= length
            else:
                break
##        print n, num
        del self.list[len(self.list)-n:]
        if num and self.list:
##            print "pop needed:", self, num
            self.list[-1].popfront(num)

        while True:
            if not self.list:
                return 
            r = self.list[-1]
            if len(r) < num:
                self.list.pop()
            elif len(r) == num:
                self.list.pop()
                return
            else:
                r.popfront(num)
                if len(r) == 0:
                    self.list.pop()
                return
                
    def __getitem__(self, ref):
        if isinstance(ref, int):
            ix = 0
            for r in reversed(self.list):
                if ix + len(r) > ref:
                    return r[ref-ix]
                else:
                    ix += len(r)
            raise IndexError
        elif isinstance(ref, slice):     
            tmp = []
            ix = 0
            for r in reversed(self.list):
                # skip
                if ix + len(r) < ref.start:
##                    print "skipping"
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
                        start = r.start+ref.start-ix
                    else:
                        start = r.start
                    if ix + len(r) >= ref.stop:
                        stop = r.start+ref.stop-ix
                    else:
                        stop = r.stop
                    tmp.extend(r.data[start:stop])
                if ix + len(r) >= ref.stop:
                    return tmp
                ix += len(r)
            return tmp

    def insertfront(self, ref):
        if ref.data:
            self.list.append(ref)
        else:
            tmpreflist = []
            ix = 0
            for r in reversed(self.list):
                # skip
                if ix + len(r) < ref.start:
##                    print "skipping"
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
                        start = r.start+ref.start-ix
                    else:
                        start = r.start
                    if ix + len(r) >= ref.stop:
                        stop = r.start+ref.stop-ix
                    else:
                        stop = r.stop
                    tmp = DNARef(start, stop, r.data)  
                    tmpreflist.append(tmp)
                if ix + len(r) >= ref.stop:
##                    print "OOOOGA", len(tmpreflist), ix, len(r), ref.start, ref.stop
##                    print "1:",len(self)
                    self.list.extend(reversed(tmpreflist))
##                    print "2:",len(self)
                    return
                ix += len(r)
            print "Noooo"
        
    def find(self, substr, i):
        raise
        return -1
    

if __name__=="__main__":
    a = [1,2,3,4,5,6,7,8,9]
    r = DNARef(0, len(a),a)
    dna = DNAList()
    dna.insertfront(r)    
    print dna, dna[3:7], dna[5]
    dna.insertfront(DNARef(2,4,a))
    print dna, dna[3:7], dna[5]
    dna.insertfront(DNARef(0,4,None))
    print dna, dna[3:7], dna[5]
    dna.popfront(5)
    print dna, dna[3:7], dna[5]
    dna.popfront(len(dna))
    print dna, dna[3:7], dna[5]
