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
   Cleaned up a little.

'''

__author__ = 'Austin Garcia'
__version__ = '0.1.0'
if __name__ == '__main__':
    __package__ = 'usefulpy.mathematics'
__all__ = ('vector', 'matrix')

from .. import validation
from .. import formatting
from .mathfuncs import is_constant, mathfunc, cas_expression, safe_str, cas_variable, _comp_derive
import itertools
import functools
import math


class vector(tuple):
    str_mode: int = 0
    scalars: tuple
    dims: int
    magnitude: float

    def __new__(cls, *scalars, dims: int = 0):
        '''__new__ for vector class

        Parameters
        ----------
        dims : int, optional
            Number of dimensions of vector, filling extra space with 0s
            If default number 0 is entered, dimensions are calculated automatically.

        Returns
        -------
        [type]
            [description]

        Raises
        ------
        ValueError
            Raised if dimensions is smaller than length of scalars
        ValueError
            Raised if a function that has not been marked as expressionable by mathfunc_decorator
            is in scalars.
        TypeError
            Raised if an invalid type is encountered.
        '''
        if dims == 0:
            dims = len(scalars)
        else:
            dims = int(dims)
            if dims < len(scalars):
                raise ValueError('Too many scalars for number of dimensions')
            if dims > len(scalars):
                scalars = (*scalars, *itertools.repeat(0, dims-len(scalars)))
        if not validation.are_floats(*scalars):
            type_map = tuple(map(type, scalars))
            assert str not in type_map
            nscalars = []
            fn = []
            var = []
            for n in scalars:
                if is_constant(n):
                    nscalars.append(n)
                    continue
                if callable(n):
                    if type(n) is mathfunc:
                        nscalars.append(n)
                        fn.extend(n.composition.fn)
                        var.extend(n.variables)
                        continue
                    if isinstance(n, cas_expression):
                        nscalars.append(mathfunc(n))
                        fn.extend(n.fn)
                        var.extend(n.var)
                        continue
                    if hasattr(n, 'expressionable') and n.expressionable:
                        nscalars.append(mathfunc(n))
                        fn.extend(n.fn)
                        var.extend(n.info)
                        continue
                    raise ValueError('function is not expressionable')
                if type(n) is cas_variable:
                    nscalars.append(n)
                    var.append(n)
                    continue
                raise TypeError(f'Invalid type, {type(n)}')
            return _mathfunc_vector(tuple(nscalars), set(fn), set(var))
        v = tuple.__new__(cls, scalars)
        v.dims = dims
        v.magnitude = math.hypot(*scalars)
        return v

    def __add__(v1, v2):
        if not isinstance(v2, vector):
            if is_constant(v2) or isinstance(v2, cas_variable, cas_expression):
                return vector(v1[0]+v2, *v1[1:])
            return NotImplemented
        if v1.dims == v2.dims:
            return vector(*(a+b for a, b in zip(v1, v2)))
        if v1.dims < v2.dims:
            end = v2[v1.dims:]
            start = (a+b for a, b in zip(v1, v2))
            return vector(*start, *end)
        end = v1[v2.dims:]
        start = (a+b for a, b in zip(v1, v2))
        return vector(*start, *end)

    __radd__ = __add__

    def __sub__(v1, v2):
        if not isinstance(v2, vector):
            if is_constant(v2) or isinstance(v2, cas_variable, cas_expression):
                return vector(v1[0]-v2, *v1[1:])
            return NotImplemented
        if v1.dims == v2.dims:
            return vector(*(a-b for a, b in zip(v1, v2)))
        if v1.dims < v2.dims:
            end = (-s for s in v2[v1.dims:])
            start = (a+b for a, b in zip(v1, v2))
            return vector(*start, *end)
        end = v1[v2.dims:]
        start = (a-b for a, b in zip(v1, v2))
        return vector(*start, *end)

    def __rsub__(v1, v2):
        if is_constant(v2) or isinstance(v2, cas_variable, cas_expression):
            if isinstance(v2, vector):
                return NotImplemented
            return vector(v2-v1[0], *(-n for n in v1[1:]))
        return NotImplemented

    def __pos__(v):
        return v

    def __neg__(v):
        return vector(*(-n for n in v))

    def __mul__(v, s):
        if isinstance(s, vector):
            return NotImplemented
        try:
            return vector(*(n*s for n in v))
        except Exception:
            return NotImplemented

    def __truediv__(v, s):
        if isinstance(s, vector):
            return NotImplemented
        try:
            return vector(*[n/s for n in v])
        except Exception:
            return NotImplemented

    def __rtruediv__(v, s):
        return NotImplemented

    def __pow__(v, m):
        return NotImplemented

    def __rpow__(v, m):
        return NotImplemented

    def dot(v1, v2):
        if v1.dims < v2.dims:
            v1 = vector(*v1, v2.dims)
        if v2.dims < v1.dims:
            v2 = vector(*v2, v1.dims)
        return sum((a*b for a, b in zip(v1, v2)))

    def is_constant(self):
        return True

    __rmul__ = __mul__

    def __str__(v):
        scalars = map(safe_str, v)
        if v.str_mode == 0:
            tup = ', '.join(scalars)
            return f'vector({tup})'
        mstr = formatting.multline(*scalars)
        h = mstr.getheight()
        w = mstr.getwidth()
        side = formatting.multline(*tuple('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))

    def __repr__(v):
        scalars = map(safe_str, v)
        tup = ', '.join(scalars)
        return f'vector({tup})'

    def differentiate(self, var, k):
        return vector(*map(lambda x: var._math_return(_comp_derive(x, var, k)), self))

    def partial(self, var):
        return self.differentiate(var, 1)


def _get_name(x):
    if is_constant(x):
        return str(x)
    if isinstance(x, cas_variable):
        return x.name
    return x.function


class _mathfunc_vector(vector):
    def __new__(cls, scalars, fn, var):
        v = tuple.__new__(cls, scalars)
        v.dims = len(scalars)
        v.variables = tuple(var)
        v.magnitude = sum(map(lambda x: x**2, scalars))**(1/2)
        var_list_str = ', '.join(map(safe_str, v.variables))
        space = {func.__name__: func for func in fn}
        v.fn = fn
        _function_names = map(_get_name, scalars)
        _func_list_str = ', '.join(_function_names)
        v.function = f'vector({_func_list_str})'
        v.__doc__ = 'Return '+v.function
        _short = eval(f'lambda {var_list_str}: {v.function}', None, space)
        v.shortcut_function = _short
        _get = eval(f'lambda v, {var_list_str}: {v.function}', None, space)
        v.__call__ = _get.__get__(v)
        return v

    def __call__(self, *args):
        if all(map(is_constant, args)):
            return self.shortcut_function(*args)
        d = {var: value for value, var in zip(args, self.variables, strict=True)}
        new_scalars = []
        for n in self:
            if is_constant(n):
                new_scalars.append(n)
            if type(n) is mathfunc:
                new_scalars.append(n(*map(d.__getitem__, n.variables)))
            if type(n) is cas_variable:
                new_scalars.append(d[n])
        return vector(*new_scalars)

    def is_constant(self):
        return False


class matrix:
    repr_mode = 0

    def __new__(cls, *vectors):
        if len(vectors) == 0:
            m = super(matrix, cls).__new__(cls)
            m.out_dim = 0
            m.in_dim = 0
            m.vectors = m._vectors = ()

        vectors = tuple([vector(*v) for v in vectors])
        ivectors = iter(vectors)
        a = max([v.dims for v in vectors])
        b = len(vectors)
        vectors1 = tuple([vector(*v, dims=a) for v in vectors])
        vectors2 = tuple([vector(*v, dims=max(a, b)) for v in vectors])
        function_list = []
        for n in ivectors:
            if type(n) is _mathfunc_vector:
                m = super(matrix, cls).__new__(_mathfunc_matrix)
                vars = list(n.variables)
                fn = list(n.fn)
                m.out_dim = a
                m.in_dim = b
                m.vectors = tuple(vectors1)
                m._vectors = tuple(vectors2)
                function_list.append(n.function)
                for n in ivectors:
                    if type(n) is _mathfunc_vector:
                        vars.extend(n.variables)
                        fn.extend(n.fn)
                        function_list.append(n.function)
                    else:
                        function_list.append(repr(n))
                m.variables = tuple(set(vars))
                m.fn = tuple(set(fn))
                var_list_str = ', '.join(map(safe_str, m.variables))
                space = {func.__name__: func for func in fn}
                _func_list_str = ', '.join(function_list)
                m.function = f'matrix({_func_list_str})'
                m.__doc__ = 'Return '+m.function
                _short = eval(f'lambda {var_list_str}: {m.function}', None, space)
                m.shortcut_function = _short
                _get = eval(f'lambda m, {var_list_str}: {m.function}', None, space)
                m.__call__ = _get.__get__(m)
                return m
            else:
                function_list.append(repr(n))

        m = super(matrix, cls).__new__(cls)
        m.out_dim = a
        m.in_dim = b
        m.vectors = tuple(vectors1)
        m._vectors = tuple(vectors2)
        return m

    def _mul_vector(m, v):
        if m.in_dim <= v.dims:
            nvectors = []
            for s, v1 in zip(m.vectors, v):
                nvectors.append(s*v1)
            return sum(nvectors)
        elif m.in_dim > v.dims:
            nv = vector(*(list(v)), dims=m.in_dim)
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
        return functools.reduce(lambda a, b: a+' '+b, mstrs)

    def __repr__(m):
        if m.repr_mode == 0:
            return 'matrix' + str(m.vectors)
        mstr = m.__mulstr__()
        h = mstr.getheight()
        w = mstr.getwidth()
        side = formatting.multline(*('|'*h))
        mstr = str(side + mstr + side)
        top = '_'+w*' '+'_'
        bottom = '‾' + w*' '+'‾'
        return '\n'.join((top, mstr, bottom))

    __str__ = __repr__

    def __iter__(m):
        return m.vectors.__iter__()

    def __float__(m):
        if len(m.vectors) == 1:
            if len(m.vectors[0]) == 1:
                return m.vectors[0][0]
        return NotImplemented

    def get_column(m, i, zeros=False):
        if zeros:
            column = m._vectors[i]
        else:
            column = m.vectors[i]
        try:
            return matrix(*column)
        except Exception:
            return matrix(column)

    def get_row(m, i, zeros=False):
        if zeros:
            data = [v[i] for v in m._vectors]
        else:
            data = [v[i] for v in m.vectors]
        try:
            return matrix(*data)
        except Exception:
            return matrix(*map(vector, data))

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
            return m[0, True]*m[1, 1, True]-m[0, 1, True]*m[1, 0, True],
        sum = 0
        for n in range(m.in_dim):
            num = float(m[n, 0])
            m_sub = matrix(*m[: n, 1:, True], *m[(n+1):, 1:, True])

            if n & 1:
                sum += num*m_sub.det()
            else:
                sum -= num*m_sub.det()

    def is_constant(self):
        return True

    def differentiate(self, var, k):
        return matrix(*(vector.differentiate(var, k) for vector in self.vectors))

    def partial(self, var):
        return self.differentiate(var, 1)


class _mathfunc_matrix(matrix):

    def __call__(self, *args):
        d = {var: value for value, var in zip(args, self.variables, strict=True)}
        new_vectors = []
        for v in self:
            if is_constant(v):
                new_vectors.append(v)
            if type(v) is _mathfunc_vector:
                new_vectors.append(v(*map(d.__getitem__, v.variables)))
        return matrix(*new_vectors)

    def is_constant(self):
        return False
