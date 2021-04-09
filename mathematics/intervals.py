def _nbin(num, length):
    binnum = bin(num)[2:]
    if len(binnum) >= length: return binnum[-length:]
    return (length - len(binnum))*'0'+binnum
class interval:
    start:float
    stop:float
    _check:type(lambda:None)
    _repstr:str
    mode: int
    finished: False
    def __new__(cls, start:float, stop:float, mode = 'open'):
        if type(mode) is str and mode not in ('open', 'left', 'right', 'close'):
            raise ValueError('Invalid Mode')
        elif type(mode) is int and mode not in range(0, 4):
            raise ValueError('Invalid Mode')
        elif type(mode) in (int, str): pass
        else:
            raise TypeError('Invalid Mode')
        self = super(interval, cls).__new__(cls)
        self.start = float(start)
        self.stop = float(stop)
        if mode in ('open', 0):
            self._check = (lambda x: (x>start) and (x<stop))
            self._repstr = '('+str(self.start)+', '+str(self.stop)+')'
            self.mode = 0
            return self
        if mode in ('right', 1):
            self._check = (lambda x: (x>start) and (x<=stop))
            self._repstr = '('+str(self.start)+', '+str(self.stop)+']'
            self.mode = 1
            return self
        if mode in ('left',2):
            self._check = (lambda x: (x>=start) and (x<stop))
            self._repstr = '['+str(self.start)+', '+str(self.stop)+')'
            self.mode = 2
            return self
        if mode in ('close', 3):
            self._check = (lambda x: (x>=start) and (x<=stop))
            self._repstr = '['+str(self.start)+', '+str(self.stop)+']'
            self.mode = 3
            return self
        raise Exception('Internal Error Occured: This code shouldn\'t be possible to access')

    def __contains__(self, x):
        return self._check(x)
    
    def __repr__(self):
        return f'Interval[\'{self._repstr}\']'
    
    def __str__(self):
        return self._repstr
    
    def __eq__(self, other):
        return self._repstr == other._repstr
    
    def __hash__(self):
        return hash(self.start,self.stop, self.mode)

    def __or__(self, other):
        if type(other) is interval:
            if other.start in self:
                if other.stop in self: return self
                return interval(self.start, other.stop, int(_nbin(self.mode, 2)[0]+_nbin(other.mode, 2)[-1], base = 2))
            if other.stop in self:
                return interval(other.start, self.stop, int(_nbin(other.mode, 2)[0]+_nbin(self.mode, 2)[-1], base = 2))
            if self.start in other: return other
            if self.stop in other:
                return interval(self.start, other.stop, int(_nbin(self.mode, 2)[0]+_nbin(other.mode, 2)[-1], base = 2))
            return unified_interval(self, other)
        if type(other) is unified_interval:
            for inter in unified:pass
        return NotImplemented

    def __ror__(self, other):
        if type(other) is interval:
            if other.start in self:
                if other.stop in self: return self
                return interval(self.start, other.stop, int(_nbin(self.mode, 2)[0]+_nbin(other.mode, 2)[-1], base = 2))
            if other.stop in self:
                return interval(other.start, self.stop, int(_nbin(other.mode, 2)[0]+_nbin(self.mode, 2)[-1], base = 2))
            if self.start in other: return other
            if self.stop in other:
                return interval(self.start, other.stop, int(_nbin(self.mode, 2)[0]+_nbin(other.mode, 2)[-1], base = 2))
            return unified_interval(self, other)
        if type(other) is unified_interval:
            pass
            
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __rxor__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __rand__(self, other):
        return NotImplemented

    def __lt__(self, other):
        if self.start != other.start:
            return self.start < other.start
        return self.stop<other.stop

    def __gt__(self, other):
        if self.start != other.start:
            return self.start > other.start
        return self.stop>other.stop

class unified_interval:
    intervals: tuple[interval]
    def __new__(cls, *intervals):
        self = super(unified_interval, cls).__new__(cls)
        self.intervals = sorted(intervals)
        return self

    def __contains__(self, x):
        for inter in self.intervals:
            if x in inter: return True
        return False

    def __repr__(self):
        repstr = 'U'.join(map(str, self.intervals))
        return f'Interval(\'{repstr}\')'

    def __str__(self):
        return 'U'.join(map(str, self.intervals))

    def __iter__(): pass
