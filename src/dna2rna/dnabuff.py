import time

BUFF_SIZE = 30000000
INIT_OFS  = 5000000

class NoMoreData(Exception):
    pass
    
class dnalist:
    def __init__(self, data):
        self.buff = BUFF_SIZE * ['']
        self.start = INIT_OFS
        self.end = self.start + len(data)
        self.buff[self.start:self.start + len(data)] = data
        self.blocks = []
        self.insert = []
        return
        
    def __len__(self):
        return self.end - self.start
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.buff[self.start + key]
        elif isinstance(key, slice):
            return self.buff[self.start + key.start : self.start + key.stop]
        raise TypeError
        
    def __str__(self):
        if len(self) <= 50:
            return ''.join(self.buff[self.start:self.end])
        else:
            return ''.join(self.buff[self.start:self.start+50]) + '...'
        
    def popfront(self, n = 1):
        if (self.end - self.start) >= n:
            self.start += n
        else:
            self.start = self.end
            raise NoMoreData
        return
        
    def insertfront(self, block):
        #print 'dnalist.insertfront:', block
        self.insert.append(block)
        return
        
    def markblock(self, start, end):
        # Store real indices.
        blockid = len(self.blocks)
        self.blocks.append((self.start + start, self.start + end))
        return blockid
        
    def readblock(self, block):
        start, end = self.blocks[block]
        return self.buff[start:end]
        
    def blocksize(self, block):
        start, end = self.blocks[block]
        return end - start
    
    def _insertblockfront(self, block, blockdata):
        data = None
        if isinstance(block, int):
            data = blockdata[block]
        else:
            data = block
        self.buff[self.start - len(data) : self.start] = data
        self.start -= len(data)
        assert(self.start >= 0)
        return
        
    def _insertblockend(self, block, blockdata):
        data = None
        if isinstance(block, int):
            data = blockdata[block]
        else:
            data = block
        self.buff[self.end : self.end + len(data)] = data
        self.end += len(data)
        assert(self.end < BUFF_SIZE)
        return
        
    def arrange(self):
        #print 'dnalist.arrange:'
        #print '  self.blocks =', self.blocks
        #print '  self.insert =', self.insert
        maxblocksize = len(self)
        maxblockix = -1
        blocksize = 0
        
        # Find largest block (new blocks doesn't count).
        for ix, block in enumerate(self.insert):
            if isinstance(block, int):
                blocksize = self.blocks[block][1] - self.blocks[block][0]                
                if blocksize > maxblocksize:
                    maxblocksize = blocksize
                    maxblockix = ix
                    
        #print 'dnalist.arrange: maxblockix =', maxblockix
           
        # Extract data of referenced blocks.
        blockdata = {}
        for ix, block in enumerate(self.insert):
            if isinstance(block, int) and (ix != maxblockix):
                blockdata[block] = self.buff[self.blocks[block][0]:self.blocks[block][1]]
                
        if (maxblockix != -1):
            # Store DNA
            blockdata[-1] = self.buff[self.start:self.end]
            
        #print 'dnalist.arrange: blockdata =', blockdata
            
        # Largest block in fixed position (may be remaining DNA).
        if (maxblockix == -1):
            for block in self.insert:
                self._insertblockfront(block, blockdata)
        else:
            # Set new start and end positions.
            blockid = self.insert[maxblockix]
            self.start, self.end = self.blocks[blockid]
            
            #print 'dnalist.arrange: self.start =', self.start
            #print 'dnalist.arrange: self.end   =', self.end
            
            # Insert blocks.
            for block in self.insert[maxblockix+1:]:
                self._insertblockfront(block, blockdata)
                
            #print 'dnalist.arrange: dna =', self
            
            for block in reversed(self.insert[:maxblockix]):
                self._insertblockend(block, blockdata)
                
            #print 'dnalist.arrange: dna =', self
                
            # Insert remaining DNA.
            self._insertblockend(-1, blockdata)
            
            #print 'dnalist.arrange: dna =', self
            
        # Reset block lists.
        self.blocks = []
        self.insert = []
        return
        
    def _stepfind(self, substr, startpos, maxtime):
        subpos = 0
        findpos = 0
        i = startpos
        starttime = time.time()
        length = len(self)
        while (i < length):
            if (self[i] == substr[subpos]):
                if (subpos == 0):
                    findpos = i 
                subpos += 1
                if (subpos == len(substr)):
                    return findpos
            elif (subpos > 0):
                i = findpos
                subpos = 0
            i += 1
            if (i % 10000) and (time.time() - starttime > maxtime):
                return None
        return -1
        
    def _strfind(self, substr, startpos):
        s = ''.join(self[startpos:len(self)])
        f = s.find(substr)
        if f >= 0:
            return f + startpos
        else:
            return f
            
    def find(self, substr, startpos = 0):
        f = self._stepfind(substr, startpos, 5.0)
        if f is None:
            return self._strfind(substr, startpos)
        else:
            return f
            
    def buffermargins(self):
        return (self.start, BUFF_SIZE - self.end)
        
if __name__ == '__main__':
    # Test 1.
    print ''
    print 'Test 1'
    print ''
    d = dnalist('IICCCFFFPP')
    print 'd =', d
    print 'd[8] = ', d[8]
    print 'd[3:7] =', d[3:7]
    print 'd.popfront(3)'
    d.popfront(3)
    print 'd =', d
    print "d.insertfront('ICFP')"
    print 'd.arrange()'
    d.insertfront('ICFP')
    d.arrange()
    print 'd =', d
    print ''
    print 'b = d.markblock(2, 4)'
    print 'd.popfront(8)'
    print 'd.insertfront(b)'
    print "d.insertfront('PP')"
    print 'd.arrange()'
    b = d.markblock(2, 4)
    d.popfront(8)
    d.insertfront(b)
    d.insertfront('PP')
    d.arrange()
    print 'd =', d
    
    # Test 2.
    print ''
    print 'Test 2'
    print ''
    d = dnalist('IICCCFFFPP')
    print 'd =', d
    print "d.find('CFF') =", d.find('CFF')
    print "d.find('CFP') =", d.find('CFP')