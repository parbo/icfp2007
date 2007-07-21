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
            ref, ix, pos = self._blockAt(key)
            return ref[key - ix]
        elif isinstance(key, slice):
            # Find start and end blocks.
            startblock, startix, startpos = self._blockAt(key.start)
            endblock, endix, endpos = self._blockAt(key.stop)
            #print key.start, key.stop
            #print startblock, startix, startpos
            #print endblock, endix, endpos
            if (startpos == endpos):
                return startblock[key.start - startix : key.stop - startix]
            else:
                # Merge all dnarefs within the given range.
                newref = endblock[0 : key.stop - endix]
                for ref in self.refs[endpos + 1 : startpos]:
                    newref.merge(ref)
                newref.merge(startblock[key.start - startix : len(startblock)])
                return newref
        raise TypeError
        
    def __str__(self):
        return ''.join([str(ref) for ref in reversed(self.refs)])
        
    # Returns a tuple consisting of the block containing index 'key',
    # this block's start index, and the blocks position in the list: (block, startix, position)
    def _blockAt(self, key):
        # NOTE: The reference list is reversed.
        ix = 0
        position = len(self.refs)
        for ref in reversed(self.refs):
            position -= 1
            if (ix + len(ref)) > key:
                break
            else:
                ix += len(ref)
        return (ref, ix, position)
        
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
        if data:
            if rng:
                self.refs = [blockref(data, rng[0], rng[1])]
            else:
                self.refs = [blockref(data, 0, len(data))]
        else:
            self.refs = refs
        return
        
    def __len__(self):
        return sum([len(ref) for ref in self.refs])
        
    def __getitem__(self, key):
        if isinstance(key, int):
            ref, ix, pos = self._blockAt(key)
            return ref[key - ix]
        elif isinstance(key, slice):
            return self._newref(key.start, key.stop)
        raise TypeError
        
    def __str__(self):
        return ''.join([str(ref) for ref in reversed(self.refs)])
        
    def _newref(self, start, end):
        blocks = []
        startblock, startix, startpos = self._blockAt(start)
        endblock, endix, endpos = self._blockAt(end)
        if (startpos == endpos):
            blocks.append(blockref(startblock.block, startblock.start + start - startix, startblock.start - startix + end))
        else:
            blocks.append(blockref(endblock.block, endblock.start, endblock.end + end - endix))
            blocks.extend(self.refs[endpos+1:startpos])
            blocks.append(blockref(startblock.block, startblock.start + start - startixt, startblock.end))
        return dnaref(refs = blocks)
        
    def merge(self, ref):
        self.refs.extend(ref.refs)
        return
        
    # Returns a tuple consisting of the block containing index 'key',
    # this block's start index, and the blocks position in the list: (block, startix, position)
    def _blockAt(self, key):
        # NOTE: The reference list is reversed.
        ix = 0
        position = len(self.refs)
        for ref in reversed(self.refs):
            position -= 1
            if (ix + len(ref)) > key:
                break
            else:
                ix += len(ref)
        return (ref, ix, position)
            
            
class blockref:
    def __init__(self, block, start, end):
        self.block = block
        self.start = start
        self.end = end
        return
        
    def __len__(self):
        return self.end - self.start
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.block[self.start + key]
        elif isinstance(key, slice):
            pass
        raise TypeError
        
    def __str__(self):
        return ''.join(self.block[self.start:self.end])
        
        
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
    
     # Test 5.
    print ''
    print 'Test 5'
    print ''
    s1 = 'ICCFF'
    s2 = 'FPPPP'
    d = dna(s2)
    d.insertfront(s1)
    r = d[3:7]
    d.insertfront(r)
    print str(r) + s1 + s2
    print d
    for ix in range(len(d)):
        print ix, d[ix]
    print ''