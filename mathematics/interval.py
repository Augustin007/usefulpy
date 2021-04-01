class interval:
    start:float
    stop:float
    _check:type(lambda:None)
    _repstr:str
    mode = int
    def __new__(cls, start, stop, mode = 'open'):
        if mode not in ('open', 'close', 'left', 'right'):
            raise ValueError('Invalid Mode')
        self = super(interval, cls).__new__(cls)
        self.start = start
        self.stop = stop
        if mode == 'open':
            self._check = (lambda x: (x>start) and (x<stop))
            self._repstr = '('+str(start)+', '+str(stop)+')'
            self.mode = 0
            return self
        if mode == 'close':
            self._check = (lambda x: (x>=start) and (x<=stop))
            self._repstr = '['+str(start)+', '+str(stop)+']'
            self.mode = 1
            return self
        if mode =='left':
            self._check = (lambda x: (x>=start) and (x<stop))
            self._repstr = '['+str(start)+', '+str(stop)+')'
            self.mode = 2
            return self
        if mode == 'right':
            self._check = (lambda x: (x>start) and (x<=stop))
            self._repstr = '('+str(start)+', '+str(stop)+']'
            self.mode = 3
            return self
    
    def __contains__(self, x):
        return self._check(x)
    
    def __repr__(self):
        return f'interval[{self._repstr}]'
    
    def __str__(self):
        return self._repstr
    
    def __eq__(self, other):
        return self._repstr == other._repstr
    
    def __hash__(self):
        return hash(self.start,self.stop, self.mode)