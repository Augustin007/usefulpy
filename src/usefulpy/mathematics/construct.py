from dataclasses import dataclass
from functools import cache
__package__ = 'usefulpy.mathematics'
from . import nmath as math


def _safe(B):
    if isinstance(B, float):
        return float_(B)
    elif isinstance(B, int):
        return int_(B)
    elif isinstance(B, complex):
        return complex_(B)
    return B
class AbstractConstruct:
    pass

class complex_(complex, AbstractConstruct):
    def __invert__(A, /):
        return complex(A.real, -A.imag)

class int_(int, AbstractConstruct):
    def __invert__(A, /):
        return A

class float_(float, AbstractConstruct):
    def __invert__(A, /):
        return A

@cache
def cdcon(n: int)->type:
    if n == 0:
        return float_
    if n==1:
        return complex_

    class Con(AbstractConstruct):
        A: cdcon(n-1)
        B: cdcon(n-1)

        def __init__(self, *a):
            self.n = n
            if len(a) == 2:
                self.A = cdcon(n-1)(a[0])
                self.B = cdcon(n-1)(a[1])
                return
            cutoff = 2**(n-1)
            self.A = cdcon(n-1)(*a[:cutoff])
            self.B = cdcon(n-1)(*a[cutoff:])

        def __eq__(A, B):
            if isinstance(B, (float, int, complex)) or A.n > B.n:
                return A.A == B and A.B == 0
            if A.n == B.n:
                return A.A == B.A and A.B == B.B
            return NotImplemented

        def __req__(A, B):
            return A == B

        def __add__(A, B):
            if isinstance(B, (float, int, complex) or A.n > B.n):
                return A.__class__(A.A + B, A.B)
            if A.n == B.n:
                return A.__class__(A.A+B.A, A.B+B.B)
            return NotImplemented

        def __radd__(A, B):
            return A+B

        def __sub__(A, B):
            return A + -B

        def __rsub__(A, B):
            return -A+B 

        def __neg__(A):
            return A.__class__(-A.A, -A.B)

        def __invert__(A):
            return A.__class__(~A.A, -A.B)

        def _square_sum(A):
            if A.n == 2:
                return abs(A.A)**2+abs(A.B)**2
            A.A._square_sum() + A.B._square_sum()

        def __abs__(A):
            return math.sqrt(A._square_sum())

        @property
        def real(A):
            return A.A.real

        @property
        def imag(A):
            return A - A.A.real

        v = imag

        def __polar__(q, /):
            r = abs(q)
            phi = q.__phase__()
            n = q.v
            n = n/abs(n)
            return (r, phi, n)

        polar = __polar__

        def __phase__(self, /):
            return math.acos(self.real/abs(self))

        def __ln__(x, /):
            return math.log(abs(x)) + (x.v)/abs(x.v)*math.acos(x.real/abs(x))

        def __exp__(q):
            a = q.real
            v = q.v
            return math.exp(a)*(math.cos(abs(v))+((v/abs(v)*math.sin(abs(v)))))

        def __complex__(self, /):
            if A.B != 0:
                return NotImplemented
            return A.A.__complex__()
 
        def __int__(self, /):
            if A.B != 0:
                return NotImplemented
            return A.A.__int__()

        def __float__(self, /):
            if A.B != 0:
                return NotImplemented
            return A.A.__int__()

        def __bool__(self, /):
            return self != 0

        def __mul__(A, B, /):
            
            if isinstance(B, (float, int, complex)) or A.n > B.n:
                B = _safe(B)
                return A.__class__(A.A*B, A.B*(~B))
            if A.n == B.n:
                return A.__class__(A.A*B.A-(~B.B)*A.B, B.B*A.A + A.B*(~B.A))
            if A.n < B.n:
                return B.__class__(A*B.A, B.B*A) 
            return NotImplemented

        def __rmul__(A, B, /):
            if isinstance(B, (float, int, complex)):
                B = _safe(B)
                return A.__class__(B*A.A, A.B*B)
            return NotImplemented

        def __truediv__(A, B, /):
            if isinstance(B, (int, float)):
                return A.__class__(A.A/B, A.B/B)
            return NotImplemented

        def __rtruediv__(A, B, /):
            if isinstance(B, (int, float)):
                return B*(A**-1)
            return NotImplemented

        def __pow__(A, B, /):
            if B == 0:
                return 1
            if isinstance(B, (int, float, complex, AbstractConstruct)):
                r, p, n = A.__polar__()
                k = B*p
                if isinstance(k, (int, float)):
                    return (r**B) * (math.cos(k)+n*math.sin(k))
                elif isinstance(k, complex):
                    return (r**b) * (cmath.cos(k) + n*math.sin(k))
                return (r**B)*(k.cos()+n*k.sin())
            return NotImplemented

        def __rpow__(A, B, /):
            if isinstance(B, (int, float)):
                return (math.log(B)*A).__exp__()
            if isinstance(B, complex):
                return (cmath.log(B)*A).__exp__()
            if isinstance(B, AbstractConstruct):
                return (B.__ln__()*A).__exp__()
            return NotImplemented

        def __pos__(A):
            return A

        def __hash__(A):
            return hash(A.A) + hash(A.B)

        def __ne__(self, other, /):
            return not self == other

        def __ge__(A, B):
            try:
                return float(self) >= float(other)
            except Exception:
                return NotImplemented

        def __le__(A, B):
            try:
                return float(A) <= float(B)
            except Exception:
                return NotImplemented

        def __lt__(A, B):
            try:
                return float(A) < float(B)
            except Exception:
                return NotImplemented

        def __gt__(A, B, /):
            return float(A) > float(B)

        def __repr__(A):
            return str((A.A, A.B))
    return Con

quaternion = cdcon(2)
tesseract = quaternion(1, 1, 1, 1)

