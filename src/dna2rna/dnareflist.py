class DNARef(object):
    def __init__(self, start, stop, data=None):
        self.data = data
        self.start = start
        self.stop = stop
        self.len = self.stop-self.start
        
    def __len__(self):
        return self.len
    
    def __str__(self):
        if self.data:
            return str(self.data[self.start:self.stop])
        else:
            return "(%d, %d)"%(self.start, self.stop)
    
    def popfront(self, num):
        self.start += num
        self.len = self.stop-self.start
        
    def __getitem__(self, item):
        if isinstance(item, int):
            return self.data[self.start + item]
        elif isinstance(item, slice):    
            if not item.stop :
                item.stop = len(self)
            return self.data[self.start+item.start:self.start+item.stop]
        

class DNAList(object):
    def __init__(self):
        self.list = []

    def __str__(self):
        s = []
        for r in reversed(self.list):
            s.append(str(r))
        return "".join(s)
            
        
    def __len__(self):
        if not self.lencache:
            self.lencache = sum(map(len, self.list))
        return self.lencache

    def getall(self):
        tmp = []
        for r in reversed(self.list):
            tmp.extend(r.data[r.start:r.stop])
        return tmp        
    
    def flatten(self):
        print "flatten"
        d = self.getall()
        r = DNARef(0, len(d), d)
        self.list = []
        self.insertfront(r)
    
    def popfront(self, num=1):
        n = 0
        for r in reversed(self.list):
            lr = len(r)
            if num == lr:
                # exact match, pop this too
                n += 1
                num = 0
                break
            elif num < lr:
                # popfront on item is needed
                break
            else:
                n+= 1
                num -= lr
        if n != 0:
            del self.list[len(self.list)-n:]
        if num:
            self.list[-1].popfront(num)
        self.lencache = None
                
    def popfromitem(self, num, item):
        if num == 0:
            return
        n = 0
        start = len(self.list)-item-1
        for i in xrange(start, -1, -1):
            r =  self.list[i]
            lr = len(r)
            if num == lr:
                # exact match, pop this too
                del self.list[i:start+1]
                break
            elif num < lr:
                # popfront on item is needed
                if n:
                    del self.list[i+1:start+1]
                r.popfront(num)
                break
            else:
                n+= 1
                num -= lr
        self.lencache = None

    def __getitem__(self, ref):
        if isinstance(ref, int):
            ix = 0
            for r in reversed(self.list):
                lr = len(r)
                if ix + lr > ref:
                    return r[ref-ix]
                else:
                    ix += lr
            raise IndexError
        elif isinstance(ref, slice):     
            tmp = []
            ix = 0
            rstrt = ref.start
            rstp = ref.stop
            for r in reversed(self.list):
                lr = len(r)
                # skip
                if ix + lr < rstrt:
                    if ix + lr >= rstp:
                        return tmp
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= rstrt:
                        start = r.start+rstrt-ix
                    else:
                        start = r.start
                    if ix + lr >= rstp:
                        stop = r.start+rstp-ix
                    else:
                        stop = r.stop
                    if ix + lr >= rstp:
                        if tmp:                            
                            tmp.extend(r.data[start:stop])
                            return tmp
                        else:
                            return r.data[start:stop]
                    tmp.extend(r.data[start:stop])
                ix += lr
            return tmp

    def insertfrontreflistandpopold(self, reflist, pop):
        offs = 0
        oldlen = len(self.list)
        for r in reflist:   
            if not r.data:
                r.start+=offs				
                r.stop+=offs
            offs += len(r)	
            self.insertfront(r)
        ls = len(self.list)
        self.popfromitem(pop, ls-oldlen)
        self.lencache = None
        if ls > 1000:
            self.flatten()

    def insertfront(self, ref):
        if ref.data:
            self.list.append(ref)
            self.lencache = None
        else:
            tmpreflist = []
            ix = 0
            for r in reversed(self.list):
                lr = len(r)
                # skip
                if ix + lr <= ref.start:
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
                        start = r.start+ref.start-ix
                    else:
                        start = r.start
                    if ix + lr >= ref.stop:
                        stop = r.start+ref.stop-ix
                    else:
                        stop = r.stop
                    tmp = DNARef(start, stop, r.data)  
                    tmpreflist.append(tmp)
                if ix + lr >= ref.stop:
                    self.list.extend(reversed(tmpreflist))
                    self.lencache = None
                    return
                ix += lr
            print "Noooo"
        
    def find(self, substr, startpos):
        ls = len(substr)
        if ls == 0:
            return
        subpos = 0
        c = substr[subpos]
        findpos = 0
        i = startpos
        ix = 0
        for r in reversed(self.list):
            lr = len(r)
            if ix + lr < i:                
                pass
            else:
                while i - ix < lr:
                    if (r.data[r.start+i-ix] == c):
                        if (subpos == 0):
                            findpos = i 
                        subpos += 1
                        if (subpos == ls):
##                            print "Found", substr, "at:", findpos
                            return findpos
                        else:
                            c = substr[subpos]
                    elif (subpos > 0):
                        i = findpos
                        subpos = 0
                        c = substr[subpos]
                    i += 1
            ix += lr
        print "NOT FOUND!!!!!!!!"
        return -1
    

if __name__=="__main__":
    a = range(10)
    r = DNARef(0, len(a),a)
    dna = DNAList()
    dna.insertfront(r)    
    print "dna 1:", dna
    print
    for i in "qwertyuiopasdfghjkl":
        r = DNARef(0, 1,[i])
        dna.insertfront(r)
    print "dna 2:", dna
    print
    dna.insertfrontreflistandpopold([DNARef(2,5), DNARef(4,7), DNARef(0,1,['a']), DNARef(0,8), DNARef(4,7)], 18)    
    print "dna 3:", dna
