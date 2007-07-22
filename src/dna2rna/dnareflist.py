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
##        try:
##            assert(self.start + num <= self.stop)
            self.start += num
##        except:
##            print self.start, self.stop, num
##            raise
        
    def __getitem__(self, item):
##        try:
            if isinstance(item, int):
##                assert(self.start+item < self.stop)
                return self.data[self.start + item]
            elif isinstance(item, slice):    
                if not item.stop :
                    item.stop = len(self)
##                assert(self.start+item.start < self.stop)
##                assert(self.start+item.stop < self.stop)
                return self.data[self.start+item.start:self.start+item.stop]
##        except:
##            print self.start, self.stop, item
##            raise
        

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
            length = 0
            for r in reversed(self.list):
                length += len(r)
            self.lencache = length
        return self.lencache
    
    def flatten(self):
##        print "Flatten!"
        ls = len(self)
        d = self[0:ls]
        r = DNARef(0, ls, d)
        self.list = []
        self.insertfront(r)
    
    def popfront(self, num=1):
        n = 0
        ln = len(self)
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
        ln = len(self)
        
        length = 0
##        print "POPFROMITEM", len(self.list), num, item
        start = len(self.list)-item-1
##        for i, r in enumerate(self.list[0:start+1]):
##            print "lennnnn", i,  len(r)
##            length += len(r)
##        print "LENGTH AFTER ITEM",  length
        
##        print "Len", len(self.list), "item", item, "num", num, "Range", range(start, -1, -1)
        cumlen = 0
        for i in xrange(start, -1, -1):
            r =  self.list[i]
            lr = len(r)
            cumlen += lr
            if num == lr:
                # exact match, pop this too
##                print "exact match, pop this too", i, item, n, num, cumlen
##                for fg in self.list[item-1:item-1+n]:
##                    print fg
##                print "popping", range(i, start+1)#, [str(x) for x in self.list[i: start+1]]
##                print len(self.list)
                del self.list[i:start+1]
##                print len(self.list)
                break
            elif num < lr:
                # popfront on item is needed
                if n:
##                    print "pop", i+1, start+1
##                    print len(self.list)
                    del self.list[i+1:start+1]
##                    print len(self.list)
##                print "popfront on item is needed", num
                r.popfront(num)
                break
            else:
##                print "pop this!", i
                n+= 1
                num -= lr
        self.lencache = None

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
##            raise
            return tmp

    def insertfrontreflistandpopold(self, reflist, pop):
#         "INSERTFRONTREFLIST"
   #     for r in reflist:  
     #       print len(r)
    #    print len(self.list), len(reflist)
        offs = 0
        oldlen = len(self.list)
        for r in reflist:   
            if not r.data:
                r.start+=offs				
                r.stop+=offs
            offs += len(r)	
#            print offs			
            self.insertfront(r)
##            print self
        self.popfromitem(pop, len(self.list)-oldlen)
        self.lencache = None
        if len(self.list) > 1000:
            self.flatten()
##        print "LIST length", len(self.list), oldlen, pop

    def insertfront(self, ref):
        if ref.data:
        #    print "APPEND", len(ref)
            self.list.append(ref)
            self.lencache = None
        else:
            tmpreflist = []
            ix = 0
##            print "insertfront", len(ref), ref.start, ref.stop
            for r in reversed(self.list):
                # skip
##                print "look", ix, len(r), len(r.data), r.start, r.stop#, r
                if ix + len(r) <= ref.start:
##                    print "skippin", len(r), ix
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
##                        print "case1"
                        start = r.start+ref.start-ix
                    else:
##                        print "case2"
                        start = r.start
                    if ix + len(r) >= ref.stop:
##                        print "case3"
                        stop = r.start+ref.stop-ix
                    else:
##                        print "case4"
                        stop = r.stop
                    tmp = DNARef(start, stop, r.data)  
##                    try:
##                        assert(start != stop)
##                        assert(0 <= start < len(r.data))
##                        assert(0 < stop <= len(r.data))
##                    except AssertionError:
##                        print "Error", start, stop, len(r.data)
##                        raise
##                    print "Adding:", r.data[start:min(start+10, stop)], len(tmp), tmp.start, tmp.stop, ref.start, ref.stop, ix, len(r)
                    tmpreflist.append(tmp)
                if ix + len(r) >= ref.stop:
 #                   print "TMPLIST", len(tmpreflist)
                    self.list.extend(reversed(tmpreflist))
                    self.lencache = None
                    return
                ix += len(r)
            print "Noooo"
        
    def find(self, substr, startpos):
        print "find"
        ls = len(substr)
        if ls == 0:
            return
        length = len(self)
        subpos = 0
        c = substr[subpos]
        findpos = 0
        i = startpos
        ix = 0
##        print startpos
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
                            print "FOUND!", findpos, self[findpos:findpos+len(substr)], substr
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
