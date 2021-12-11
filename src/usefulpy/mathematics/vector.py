'''
vector

DESCRIPTION
a simple linear algebra calculator

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   A simple linear algebra calculator
 0.1
  Version 0.1.0:
   
'''

__author__ = 'Augustin Garcia'
__version__ = '0.0.0'

from .. import validation as _validation
from .. import formatting as _formatting
from . import nmath as _nmath
import functools
import math

class vector:
    repr_mode:int = 0
    scalars:tuple[float]
    dims:int
    magnitude:float
    def __new__(cls, *scalars, dims = None):
        v = super(vector, cls).__new__(cls)
        scalars = tuple(map(float, scalars))
        if dims is None: 
            dims = len(scalars)
        else:
            dims = int(dims)
            if dims < len(scalars):
                raise ValueError('Too many scalars for number of dimensions')
            if dims > len(scalars):
                scalars = tuple(list(scalars)+[0]*(dims-len(scalars)))
        v.scalars = scalars
        v.dims = dims
        v.magnitude = math.hypot(*scalars)
        return v
    
    def __add__(v1, v2):
        if not isinstance(v2, vector):
            if _validation.is_float(v2):
                return vector(*([v1.scalars[0]+float(v2)]+list(v1.scalars[1:])))
            return NotImplemented
        if v1.dims == v2.dims:
            return vector(*[a+b for a, b in zip(v1.scalars, v2.scalars)])
        if v1.dims < v2.dims:
            end = list(v2.scalars[v1.dims:])
            start = [a+b for a, b in zip(v1.scalars, v2.scalars)]
            return vector(*(start + end))
        end = list(v1.scalars[v2.dims:])
        start = [a+b for a, b in zip(v1.scalars, v2.scalars)]
        return vector(*(start+end))
    
    __radd__ = __add__

    def __mulstr__(v):
        return _formatting.multline(*v.scalars)
    
    def __repr__(v):
        if v.repr_mode == 0:
            return 'vector'+str(v.scalars)
        mstr = _formatting.multline(*v.scalars)
        h = mstr.getheight()
        w = mstr.getwidth()
        side = _formatting.multline(*tuple('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))
        
    def __sub__(v1, v2):
        if not isinstance(v2, vector):
            if _validation.is_float(v2):
                return vector(*([v1.scalars[0]-v2]+list(v1.scalars[1:])))
            raise TypeError(f'cannot subtract a {type(v2).__name__} from a vector')
        if v1.dims == v2.dims:
            return vector(*[a-b for a, b in zip(v1.scalars, v2.scalars)])
        if v1.dims < v2.dims:
            end = [-n for n in v2.scalars[v1.dims:]]
            start = [a-b for a, b in zip(v1.scalars, v2.scalars)]
            return vector(*(start + end))
        end = list(v1.scalars[v2.dims:])
        start = [a-b for a, b in zip(v1.scalars, v2.scalars)]
        return vector(*(start+end))
    
    def __rsub__(v1, v2):
        if _validation.is_float(v2):
            return vector(*([v2-v1.scalars[0]]+[-n for n in v1.scalars[1:]]))
        return NotImplemented
    
    __str__ = __repr__

    def __pos__(v):
        return v
    
    def __neg__(v):
        return vector(*[-n for n in v.scalars])
    
    def __mul__(v, s):
        s = float(s)
        try: return vector(*[n*s for n in v.scalars])
        except: return NotImplemented
    __rmul__ = __mul__
    def __div__(v, s):
        s = float(s)
        try: return vector(*[n/s for n in v.scalars])
        except: return NotImplemented
    
    def __rdiv__(v, s): return NotImplemented

    def __pow__(v, m): return NotImplemented

    def __rpow__(v, m): return NotImplemented
    
    def __iter__(v):
        return v.scalars.__iter__()
    
    def dot(v1, v2):
        if v1.dims < v2.dims:
            v1 = vector(*v1.scalars, v2.dims)
        if v2.dims < v1.dims:
            v2 = vector(*v2.scalars, v1.dims)
        return sum(map(lambda a, b: a*b, zip(v1, v2)))
    
    def __getitem__(v, i): 
        return v.scalars[i]


class matrix:
    repr_mode = 0
    def __new__(cls, *vectors):
        if len(vectors) == 0:
            m = super(matrix, cls).__new__(cls)
            m.out_dim = 0
            m.in_dim = 0
            m.vectors = m._vectors = ()
        vectors = tuple([v if type(v) is vector else vector(*v) for v in vectors])
        a = max([v.dims for v in vectors])
        b = len(vectors)
        vectors1 = tuple([vector(*v.scalars, dims = a) for v in vectors])
        vectors2 = tuple([vector(*v.scalars, dims = max(a, b)) for v in vectors])
        m = super(matrix, cls).__new__(cls)
        m.out_dim = a
        m.in_dim = b
        m.vectors = tuple(vectors1)
        m._vectors = tuple(vectors2)
        return m
    
    def _mul_vector(m, v):
        if m.in_dim <= v.dims:
            nvectors = []
            for s, v1 in zip(m.vectors, v.scalars):
                nvectors.append(s*v1)
            return sum(nvectors)
        elif m.in_dim > v.dims:
            nv = vector(*(list(v.scalars)), dims = m.in_dim)
            return m*nv
        

    def _mul_matrix(m, m1):
        nv = []
        for v in m1.vectors:
            nv.append(m*v)
        return matrix(*nv)
        

    def __mul__(m, m1):
        if isinstance(m1, vector):
            return m._mul_vector(m1)
        if isinstance(m1, matrix):
            return m._mul_matrix(m1)
        return NotImplemented
    
    def __mulstr__(m):
        mstrs = tuple([v.__mulstr__() for v in m.vectors])
        return functools.reduce(lambda a, b: a+ ' '+b, mstrs)

    def __repr__(m):
        if m.repr_mode == 0:
            return 'matrix' + str(m.vectors)
        mstr = m.__mulstr__()
        h = mstr.getheight()
        w = mstr.getwidth()
        side = _formatting.multline(*('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))

    def __iter__(m):
        return m.vectors.__iter__()
    
    def __float__(m):
        if len(m.vectors) == 1:
            if len(m.vectors[0].scalars) == 1:
                return m.vectors[0].scalars[0]
        return NotImplemented
    
    def get_column(m, i, zeros = False):
        if zeros: l = m._vectors[i]
        else: l = m.vectors[i]
        try: return matrix(*l)
        except: return matrix(l)
    
    def get_row(m, i, zeros = False):
        if zeros: data = [v[i] for v in m._vectors]
        else: data = [v[i] for v in m.vectors]
        try: return matrix(*data)
        except: return matrix(*map(vector, data))

    def __getitem__(m, i):
        if type(i) is tuple:
            if len(i) == 2: 
                return m.get_row(i[1]).get_column(i[0])
            if len(i) == 3:
                return m.get_row(i[1], i[2]).get_column(i[0], i[2])
            raise IndexError("Invalid Index")
        if type(i) in (slice, int): 
            return m.get_column(i)


    def det(m):
        if m.in_dim > m.out_dim:
            return 0
        if m.in_dim == 2: 
            return m[0,True]*m[1, 1,True]-m[0, 1,True]*m[1, 0,True], 
        sum = 0
        for n in range(m.in_dim):
            num = float(m[n, 0])
            m_sub = matrix(*m[:n, 1:, True], *m[(n+1):, 1:, True])
            print(m_sub)
            if n&1: sum += num*m_sub.det()
            else: sum -=  num*m_sub.det()
        