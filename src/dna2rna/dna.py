from array import array

class dna:
    def __init__(self, data):
        self.datablocks = [array('c', data)]
        self.refs = [dnaref(self.datablocks[0])]
        return
        
    def __len__(self):
        return sum([len(ref) for ref in self.refs])
        
    def __getitem__(self, key):
        if isinstance(key, int):
            ref, ix = self._blockAt(key)
            return ref[key - ix]
        elif isinstance(key, slice):
            # Find start and end blocks.
            startblock, startix = self._blockAt(key.start)
            endblock, endix = self._blockAt(key.stop)
            if startblock is endblock:
                if startblock.data:
                    return dnaref(startblock.data, (key.start - startix, key.stop - endix))
                else:
                    #return dnaref(refs = startblock.refs)
                    pass
            else:
                pass
        raise TypeError
        
    def __str__(self):
        return ''.join([str(ref) for ref in reversed(self.refs)])
        
    # Returns a tuple consisting of the block containing index 'key' and this block's start index: (block, start)
    def _blockAt(self, key):
        # NOTE: The reference list is reversed.
        ix = 0
        for ref in reversed(self.refs):
            if (ix + len(ref)) > key:
                break
            else:
                ix += len(ref)
        return (ref, ix)
        
    def popfront(self, n):
        return
        
    def insertfront(self, data):
        # NOTE: The reference list is reversed.
        if isinstance(data, dnaref):
            self.refs.append(data)
        else:
            block = array('c', data)
            self.datablocks.append(block)
            self.refs.append(dnaref(block))
        return
        
    def simplify(self):
        datablock = array('c', self.__str__())
        self.datablocks = [datablock]
        self.refs = [dnaref(datablock)]
        return
        

class dnaref:
    def __init__(self, data = None, rng = None, refs = None):
        self.data = data
        self.refs = refs
        self.start = None
        self.end = None
        if data:
            # Reference to single data block.
            if not rng:
                self.start = 0
                self.end = len(data)
            else:
                self.start, self.end = rng
        else:
            # Reference to list of references.
            pass
        return
        
    def __len__(self):
        if self.data:
            return self.end - self.start
        else:
            return sum([len(ref) for ref in self.refs])
        
    def __getitem__(self, key):
        if isinstance(key, int):
            if self.data:
                return self.data[self.start + key]
            else:
                pass
        raise TypeError
        
    def __str__(self):
        if self.data:
            return ''.join(self.data[self.start:self.end])
        else:
            return ''.join([str(ref) for ref in reversed(self.refs)])
        
        
if __name__ == '__main__':
    # Test 1.
    print ''
    print 'Test 1'
    print ''
    s = 'ICCFFFPPPP'
    d = dna(s)
    print s
    print d
    for ix in range(len(d)):
        print ix, d[ix]
    print ''
        
    # Test 2.
    print ''
    print 'Test 2'
    print ''
    s1 = 'ICCFF'
    s2 = 'FPPPP'
    d = dna(s2)
    d.insertfront(s1)
    print s1 + s2
    print d
    for ix in range(len(d)):
        print ix, d[ix]
    print ''
    
    # Test 3.
    print ''
    print 'Test 3'
    print ''
    s1 = 'ICCFF'
    s2 = 'FPPPP'
    d = dna(s2)
    d.insertfront(s1)
    r = d[1:4]
    d.insertfront(r)
    print str(r) + s1 + s2
    print d
    for ix in range(len(d)):
        print ix, d[ix]
    print ''
    
    # Test 4.
    print ''
    print 'Test 4'
    print ''
    s1 = 'ICCFF'
    s2 = 'FPPPP'
    d = dna(s2)
    d.insertfront(s1)
    r = d[1:4]
    d.insertfront(r)
    d.simplify()
    print str(r) + s1 + s2
    print d
    for ix in range(len(d)):
        print ix, d[ix]
    print ''