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
            ix = 0
            for ref in reversed(self.refs):
                if (ix + len(ref)) > key:
                    break
                else:
                    ix += len(ref)
            return ref[key - ix]
        elif isinstance(key, slice):
            ix = 0
            for ref in reversed(self.refs):
                if (ix + len(ref)) > key.start:
                    break
                else:
                    ix += len(ref)
            return dnaref(ref.data, (key.start - ix, key.stop - ix))
        raise TypeError
        
    def __str__(self):
        return ''.join([str(ref) for ref in reversed(self.refs)])
        
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
        

class dnaref:
    def __init__(self, data, rng = None):
        self.data = data
        if not rng:
            self.start = 0
            self.end = len(data)
        else:
            self.start, self.end = rng
        return
        
    def __len__(self):
        return self.end - self.start
        
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[self.start + key]
        raise TypeError
        
    def __str__(self):
        return ''.join(self.data[self.start:self.end])
        
        
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