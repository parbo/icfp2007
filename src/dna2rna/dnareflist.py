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
        for r in reversed(self.list):
            length += len(r)
        return length
    
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
                
    def popfromitem(self, num, item):
        if num == 0:
            return
        n = 0
        ln = len(self)
        print "Len", len(self.list), "item", item, "num", num, "Range", range(len(self.list)-item-1, -1, -1)
        start = len(self.list)-item-1
        for i in xrange(start, -1, -1):
            r =  self.list[i]
            lr = len(r)
            if num == lr:
                # exact match, pop this too
                n += 1
                print "exact match, pop this too", i, i+n
##                for fg in self.list[item-1:item-1+n]:
##                    print fg
                del self.list[i:i+n]
                break
            elif num < lr:
                # popfront on item is needed
                if n:
                    print "pop", i+1, i+n
                    del self.list[i+1:i+1+n]
                print "popfront on item is needed", num
                r.popfront(num)
                break
            else:
                n+= 1
                num -= lr

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

    def insertfrontreflistandpopold(self, reflist, pop):
#         "INSERTFRONTREFLIST"
   #     for r in reflist:  
     #       print len(r)
    #    print len(self.list), len(reflist)
        offs = 0
        for r in reflist:   
            if not r.data:
                r.start+=offs				
                r.stop+=offs
            offs += len(r)	
#            print offs			
            self.insertfront(r)
##        print "KKK",len(reflist)
        self.popfromitem(pop, len(reflist))
#        print "LIST lengt", len(self.list)

    def insertfront(self, ref):
        if ref.data:
        #    print "APPEND", len(ref)
            self.list.append(ref)
        else:
            tmpreflist = []
            ix = 0
#            print "insertfront", len(ref), ref.start, ref.stop
            for r in reversed(self.list):
                # skip
                if ix + len(r) <= ref.start:
#                    print "skippin"
                    pass
                else:
                    start = 0
                    stop = 0
                    if ix <= ref.start:
 #                       print "case1"
                        start = r.start+ref.start-ix
                    else:
  #                      print "case2"
                        start = r.start
                    if ix + len(r) >= ref.stop:
    #                    print "case3"
                        stop = r.start+ref.stop-ix
                    else:
      #                  print "case4"
                        stop = r.stop
                    tmp = DNARef(start, stop, r.data)  
  #                  print "Adding:", tmp[0:10], len(tmp), tmp.start, tmp.stop, ref.start, ref.stop, ix, len(r)
                    tmpreflist.append(tmp)
                if ix + len(r) >= ref.stop:
 #                   print "TMPLIST", len(tmpreflist)
                    self.list.extend(reversed(tmpreflist))
                    return
                ix += len(r)
            print "Noooo"
        
    def find(self, substr, startpos):
        print "find"
        length = len(self)
        subpos = 0
        findpos = 0
        i = startpos
        ix = 0
##        print startpos
        for r in reversed(self.list):
            if ix + len(r) < i:                
                pass
            else:
                while i - ix < len(r):
                    if (r[i-ix] == substr[subpos]):
                        if (subpos == 0):
                            findpos = i 
                        subpos += 1
                        if (subpos == len(substr)):
                            print "FOUND!", findpos, self[findpos:findpos+len(substr)], substr
                            return findpos
                    elif (subpos > 0):
                        i = findpos
                        subpos = 0
                    i += 1
            ix += len(r)
        print "NOT FOUND!!!!!!!!"
        return -1
    

if __name__=="__main__":
    a = [1,2,3,4,4,5,6,7,8,9]
    r = DNARef(0, len(a),a)
    dna = DNAList()
    dna.insertfront(r)    
    print "dna 1:", dna
    print dna.find([4,5,6], 0)
    dna.insertfrontreflistandpopold([DNARef(2,5), DNARef(4,7), DNARef(0,1,['a']), DNARef(0,8), DNARef(4,7)], 0)    
    print "dna 2:", dna
    print dna.find([7,'a',4], 0)
    dna.popfromitem(9, 2)
    print "dna 2.5:", dna
    dna.popfront(7)
    print "dna 3:", dna
    dna.popfront(11)
    print "dna 4:", dna
    print dna.find([4,5,6], 0)
    dna.insertfront(DNARef(2,4,a))
    print dna, dna[3:7], dna[5]
    dna.insertfront(DNARef(0,4,None))
    print dna, dna[3:7], dna[5]
    dna.popfront(len(dna)-2)
    print dna #, dna[3:7], dna[5]
    dna.popfront(len(dna))
    print dna, dna[3:7], dna[5]
