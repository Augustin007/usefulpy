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
'''

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__ = '0.0.0'

from .. import validation as _validation
from .. import formatting as _formatting
from . import nmath as _nmath
import functools

class vector:
    repr_mode = 'simple'
    def __new__(cls, *scalars, dims = None):
        if dims is None:
            dims = len(scalars)
        for n in scalars:
            if not _validation.is_float(n):
                print(scalars)
                raise TypeError('All basis-vector scalars must be valid numbers')
        scalars = tuple(float(n) for n in scalars)
        v = super(vector, cls).__new__(cls)
        v.scalars = scalars
        v.dims = dims
        v.magnitude = _nmath.hypot(*scalars)
        return v
    
    def __add__(v, v1):
        if not isinstance(v1, vector):
            if _validation.is_float(v1):
                return vector(*([v.scalars[0]+v1]+list(v.scalars[1:])))
            raise TypeError(f'cannot add a vector and a {type(v1).__name__}')
        if v.dims == v1.dims:
            return vector(*[a+b for a, b in zip(v.scalars, v1.scalars)])
        if v.dims < v1.dims:
            end = list(v1.scalars[v.dims:])
            start = [a+b for a, b in zip(v.scalars, v1.scalars)]
            return vector(*(start + end))
        end = list(v.scalars[v1.dims:])
        start = [a+b for a, b in zip(v.scalars, v1.scalars)]
        return vector(*(start+end))

    def _mstr(v):
        return _formatting.multline(*v.scalars)

    def __repr__(v):
        if v.repr_mode == 'simple':
            return 'vector'+str(v.scalars)
        mstr = _formatting.multline(*v.scalars)
        h = mstr.getheight()
        w = mstr.getwidth()
        side = _formatting.multline(*tuple('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))
        
        
    __str__ = __repr__

    __radd__ = __add__

    def __sub__(v, v1):
        if not isinstance(v1, vector):
            if _validation.is_float(v1):
                return vector(*([v.scalars[0]-v1]+list(v.scalars[1:])))
            raise TypeError(f'cannot subtract a {type(v1).__name__} from a vector')
        if v.dims == v1.dims:
            return vector(*[a-b for a, b in zip(v.scalars, v1.scalars)])
        if v.dims < v1.dims:
            end = [-n for n in v1.scalars[v.dims:]]
            start = [a-b for a, b in zip(v.scalars, v1.scalars)]
            return vector(*(start + end))
        end = list(v.scalars[v1.dims:])
        start = [a-b for a, b in zip(v.scalars, v1.scalars)]
        return vector(*(start+end))
    
    def __rsub__(v, v1):
        if _validation.is_float(v1):
            return vector(*([v1-v.scalars[0]]+[-n for n in v.scalars[1:]]))
        raise TypeError(f'cannot subtract a vector from a {type(v1).__name__}')

    def __pos__(v):
        return v
    
    def __neg__(v):
        return vector(*[-n for n in v.scalars])
    
    def __mul__(v, s):
        if _validation.is_float(s):
            return vector(*[n*s for n in v.scalars])
        raise TypeError(f'Vectors can only be multiplied by floats, not {type(s).__name__}')

    __rmul__ = __mul__

    def __div__(v, s):
        if _validation.is_float(s):
            return vector(*[n/s for n in v.scalars])
        raise TypeError(f'Vectors can only be divided by floats, not {type(s).__name__}')

    def __iter__(v):
        return v.scalars.__iter__()

class matrix:
    repr_mode = 'simple'
    def __new__(cls, *vectors):
        nvectors = []
        for n in vectors:
            if isinstance(n, vector): nvectors.append(n); continue
            try: nvectors.append(vector(*n)); continue
            except: pass
            try: nvectors.append(vector(n)); continue
            except: pass
            raise TypeError('Innappropriate argument for matrix')
        a = max([v.dims for v in nvectors])
        b = len(nvectors)
        vectors = []
        for v in nvectors:
            if v.dims != a:
                vectors.append(vector(*(list(v.scalars) + list((a-v.dims)*'0'))))
                continue
            vectors.append(v)
        m = super(matrix, cls).__new__(cls)
        m.out_dim = a
        m.in_dim = b
        m.vectors = tuple(vectors)
        return m
    
    def _mul_vector(m, v):
        if m.in_dim <= v.dims:
            nvectors = []
            for s, v1 in zip(m.vectors, v.scalars):
                nvectors.append(s*v1)
            return sum(nvectors)
        elif m.in_dim > v.dims:
            nv = vector(*(list(v.scalars) + list((m.in_dim-v.dims)*'0')))
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

    def _mstr(m):
        mstrs = tuple([v._mstr() for v in m.vectors])
        return functools.reduce(lambda a, b: a+ ' '+b, mstrs)

    def __repr__(m):
        if m.repr_mode == 'simple':
            return 'matrix' + str(m.vectors)
        mstr = m._mstr()
        h = mstr.getheight()
        w = mstr.getwidth()
        side = _formatting.multline(*tuple('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))

    def __iter__(m):
        return m.vectors.__iter__()

def _organize(*row_info):
    boxln = max(map(len, map(str, _validation.flatten(row_info))))
    a = [(' '.join(map(lambda n: str(n).ljust(boxln), row))) for row in row_info]
    return tuple(a)

if __name__ == '__main__': #For testing reasons
    vector.repr_mode = ''
    matrix.repr_mode = ''
