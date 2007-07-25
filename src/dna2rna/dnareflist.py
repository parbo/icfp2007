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
            if item.stop :
                return self.data[self.start+item.start:self.start+item.stop]
            else:
                return self.data[self.start+item.start:self.start+self.len]
        

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
            self.lencache = sum(map(lambda x: x.len, self.list))
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
        self.list = [r]
        self.lencache = None
    
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
        if n > 0:
            del self.list[len(self.list)-n:]
            self.lencache = None
        if num:
            self.list[-1].popfront(num)
            if self.lencache:
                self.lencache -= num

                
    def popfrontret(self, num=1):
        n = 0
        tmp = []
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
        if n > 0:
            for b in [a for a in reversed(self.list[len(self.list)-n:])]:
                tmp.extend(b[0:])
            del self.list[len(self.list)-n:]
            self.lencache = None
        if num:
            tmp.extend(self.list[-1][0:num])
            self.list[-1].popfront(num)
            if self.lencache:
                self.lencache -= num
        return tmp

    def __getitem__(self, ref):
        try:
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
        except AttributeError: # not a slice
            ix = 0
            for r in reversed(self.list):
                lr = len(r)
                if ix + lr > ref:
                    return r[ref-ix]
                else:
                    ix += lr
            raise IndexError

    def getreflistiter(self, refstart, refstop):
        ix = 0
        tmpreflist = []
        for r in reversed(self.list):
            lr = len(r)
            # skip
            if ix + lr <= refstart:
                pass
            else:
                start = 0
                stop = 0
                if ix <= refstart:
                    start = r.start+refstart-ix
                else:
                    start = r.start
                if ix + lr >= refstop:
                    stop = r.start+refstop-ix
                else:
                    stop = r.stop
                tmpreflist.append(DNARef(start, stop, r.data))
            if ix + lr >= refstop:
                return tmpreflist
            ix += lr

    def insertfront(self, reflist):
        self.list.extend(reversed(reflist))
        self.lencache = None
        if len(self.list) > 200:
            self.flatten()
        
    def find(self, substr, startpos):
#        print "find:", substr, startpos
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
