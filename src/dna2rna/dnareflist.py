import itertools
from collections import deque

class DNARef(object):
    def __init__(self, start, stop, data=None):
        self.data = data
        self.start = start
        self.stop = stop
        self.len = self.stop-self.start
        self.totlen = 0
        
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
        self.totlen -= num

    def getall(self):
        return self.data[self.start:self.stop]
        
    def __getitem__(self, item):
        try:
            if item.stop :
                return self.data[self.start+item.start:self.start+item.stop]
            else:
                return self.data[self.start+item.start:self.start+self.len]
        except AttributeError:
            return self.data[self.start + item]
        

class DNAList(object):
    def __init__(self):
        self.list = deque()

    def __str__(self):
        s = []
        for r in self.list:
            s.append(str(r))
        return "".join(s)
            
        
    def __len__(self):
        try:
            return self.list[0].totlen
        except IndexError:
            return 0
 
    def getix(self, pos):
        low = 0
        sl = self.list
        high = len(sl) - 1
        ls = len(self)
        while low < high:
           mid = (low + high)/2
           if ls - sl[mid].totlen + sl[mid].len < pos: 
               low = mid + 1
           else:
                high = mid
        return low

    def getall(self):
        tmp = []
        for r in self.list:
            tmp.extend(r.data[r.start:r.stop])
        return tmp        
    
    def flatten(self):
        print "flatten"
        d = self.getall()
        ld = len(d)
        r = DNARef(0, ld, d)
        r.totlen = ld
        self.list.clear()
        self.list.append(r)
    
    def popfront(self, num=1):
        n = 0
        # optimize for common case
        r = self.list[0]
        if num < r.len:
            # avoid function call
            r.start += num
            r.len = r.stop-r.start
            r.totlen -= num
            return
        for r in self.list:
            lr = r.len
            if num < lr:
                # popfront on item is needed
                break
            elif num == lr:
                # exact match, pop this too
                n += 1
                num = 0
                break
            else:
                n+= 1
                num -= lr
        while n:      
            self.list.popleft()
            n -= 1
        if num:
            self.list[0].popfront(num)


    def popfrontret(self, num=1):
        n = 0
        tmp = []
        # optimize for common case
        r = self.list[0]
        if num < r.len:
            tmp = r[0:num]
            # avoid function call
            r.start += num
            r.len = r.stop-r.start
            r.totlen -= num
            return tmp
        for r in self.list:
            lr = r.len
            if num < lr:
                # popfront on item is needed
                break
            elif num == lr:
                # exact match, pop this too
                n += 1
                num = 0
                break
            else:
                n+= 1
                num -= lr
        while n:      
            tmp.extend(self.list.popleft().getall())
            n -= 1
        if num:
            tmp.extend(self.list[0][0:num])
            self.list[0].popfront(num)
        return tmp

    def __getitem__(self, ref):
        try:
            tmp = []
            rstrt = ref.start
            rstp = ref.stop
            te = tmp.extend
            ix = 0
            for r in self.list:
                lr = r.len
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
                        if tmp:                            
                            te(r.data[start:stop])
                            return tmp
                        else:
                            return r.data[start:stop]
                    else:
                        stop = r.stop
                    te(r.data[start:stop])
                ix += lr
            return tmp
        except AttributeError: # not a slice
            r = self.list[self.getix(ref)]
            return r[ref-ix]

    def getreflistiter(self, refstart, refstop):
        ix = 0
        tmpreflist = []
        for r in self.list:
            lr = r.len
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
                    tmpreflist.append(DNARef(start, stop, r.data))
                    return tmpreflist
                else:
                    stop = r.stop
                tmpreflist.append(DNARef(start, stop, r.data))
            if ix + lr >= refstop:
                return tmpreflist
            ix += lr
        raise

    def insertfront(self, reflist):
        totlen = len(self)
        for r in reversed(reflist):
            totlen += len(r)
            r.totlen = totlen
            self.list.appendleft(r)
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
        findix = 0
        findli = 0
        i = startpos
        li = self.getix(startpos)
        ix = len(self)-self.list[li].totlen
        ll = len(self.list)
        while li < ll:
            r = self.list[li]
            lr = r.len
            if ix + lr < i:                
                pass
            else:
                while i - ix < lr:
                    if (r.data[r.start+i-ix] == c):
                        if (subpos == 0):
                            findpos = i 
                            findli = li
                            findix = ix
                        subpos += 1
                        if (subpos == ls):
                            #print "Found", substr, "at:", findpos
                            return findpos
                        else:
                            c = substr[subpos]
                    elif (subpos > 0):
                        # Go back in loop
                        i = findpos
                        if li != findli:
                            li = findli
                            ix = findix
                            r = self.list[li]
                            lr = r.len
                        subpos = 0
                        c = substr[subpos]
                    i += 1
            ix += lr
            li += 1
        print "NOT FOUND!!!!!!!!", substr, startpos
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
