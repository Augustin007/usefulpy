'''
File: algebraicsolvers.py
Version: pr 5 (1.1.1)
Author: Austin Garcia

Algebraic expressions/algebraic simplification

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  pr 1 (0.0.0)
   creates expression class
   a lot of work has been done on the divexpression class
  pr 2 (0.0.0)
   bugfixes for the divexpression class
  pr 3 (0.0.0)
   addexpression class. a lot of work has been done.
  pr 4 (0.0.0)
   Worked a lot on clearing dozens of little bugs that would crop up
   when adding or dividing objects of two different classes. Also when working
   between the two current expression classes.  AGH!
  pr 5 (0.0.0)
   Warnings, for the sake of sanity! Oh, bug fixes as well, of course.
  pr 6 (0.0.0)
   To prevent infinite recursion and yet still support adding and subtracting
   variables: the 'frozen'  is added to the statement.

'''

##UNFINISHED: finish for Usefulpy 1.3
##PREREQUISITE1.3: 1.1.1

__author__ = 'Austin Garcia'
__version__ = 'pr 6 (1.1.1)'

try:
    from nmath import *
    from basenum import *
    from quaternion import *
    from PrimeComposite import *
except:
    from usefulpy.mathematics.nmath import *
    from usefulpy.mathematics.basenum import *
    from usefulpy.mathematics.quaternion import *
    from usefulpy.mathematics.PrimeComposite import *
from usefulpy.formatting import multline
from usefulpy import validation as _validation

class FrozenError(Exception):
    def __init__(self, source = ''):
        if scource: self.message = "'"+str(scource)+"' is frozen and cannot be updated"
        else: self.message = ''

    def __str__(self):
        return self.message

class irrational(object):
    '''represents irrational number for expression'''
    
    conversions = {'pi': π, 'π': π, 'τ': τ, 'tau': τ, 'e': e}
    def __init__(self, value):
        if value == 'pi': value = 'π'
        if value == 'tau': value = 'τ'
        self.name = None
        if type(value) == str: value = _validation.tryfloat(value)
        if type(value) == str:
            self.name, self.value = value
            irrational.conversions[name]
        elif type(value) in (float, int, num, basenum): self.value = value
        else: raise ValueError

    def __float__(self): return float(self.value)

    def __int__(self): return int(self.value)

    def __abs__(self): return abs(float(self.value))

    def __lt__(self, other): return float(self)<float(other)

    def __gt__(self, other): return float(self)>float(other)

    def __le__(self, other): return float(self)<=float(other)

    def __ge__(self, other): return float(self)>=float(other)

    def __eq__(self, other): return float(self)==float(other)

    def __ne__(self, other): return float(self)!=float(other)

    def __str__(self): return str(self.value)

hasbeenwarned1 = False
def WarnOnce1():
    global hasbeenwarned1
    if not hasbeenwarned1:
        warnings.warn(NotImplementedError('var class is in progress: expect errors and bugs'))
        hasbeenwarned1 = True
class var(object):
    '''represents a variable'''
    names ={}
    def __init__(self, name, value = None):
        WarnOnce1()
        if type(name) != str: raise TypeError
        if len(name) != 1: raise ValueError
        if value != None:
            if _validation.is_float(value):
                value = _validation.tryint(float(value))
                if type(value) == float: value = expression(value)
            else: raise FloatingPointError
        self.name = name
        self.solved = value != None
        self.value = value
        if not self.solved:
            if self.name in self.names:
                if self.names[self.name] == None: return
                self.solved = True
                self.value = self.names[self.name]
            else:
                self.names[self.name] = self.value
        if self.solved:
            if self.name in self.names:
                if self.names[self.name] == None:
                    self.names[self.name] = self.value
                elif self.names[self.name] == self.value: pass
                else: raise ArithmeticError
            else: self.names[self.name] = self.value

    def assign(self, value):
        WarnOnce1()
        if self.solved: raise AttributeError
        if value != None:
            if is_float(value):
                value = _validation.tryint(float(value))
                if type(value) == float: value = expression(value)
            else: raise FloatingPointError
        self.value = value
        self.solved = True

    def __float__(self):
        WarnOnce1()
        return float(self.value)

    def __int__(self):
        WarnOnce1()
        return int(self.value)

    def __abs__(self):
        WarnOnce1()
        return abs(float(self.value))

    def __str__(self):
        WarnOnce1()
        return str(self.name)

    def __lt__(self, other):
        WarnOnce1()
        return float(self)<float(other)

    def __gt__(self, other):
        WarnOnce1()
        return float(self)>float(other)

    def __le__(self, other):
        WarnOnce1()
        return float(self)<=float(other)

    def __ge__(self, other):
        WarnOnce1()
        return float(self)>=float(other)

    def __eq__(self, other):
        WarnOnce1()
        try: return float(self)==float(other)
        except: return self.name == other.name

    def __ne__(self, other):
        WarnOnce1()
        try: return float(self)!=float(other)
        except: return False

    def __repr__(self):
        WarnOnce1()
        return str(self)

    def Value(self):
        WarnOnce1()
        if not self.solved:
            if self.name in self.names:
                if self.names[self.name] == None: return
                self.solved = True
                self.value = self.names[self.name]
            else:
                self.names[self.name] = self.value
        return self.value

hasbeenwarned2 = False
def WarnOnce2():
    global hasbeenwarned2
    if not hasbeenwarned2:
        warnings.warn(NotImplementedError('Expression class is in progress: Expect errors and bugs'))
        hasbeenwarned2 = True

class Expression:

    def is_negative(num):
        WarnOnce2()
        if type(num) == int:
            return 0>num
        if type(num) == quaternion:
            return 0>num.a

    def getTypes():
        WarnOnce2()
        Types = (int, irrational, quaternion, var)
        return Types+Expression.ExpressionTypes

    def acceptType(number):
        WarnOnce2()
        #Possible return types are int, an Expression subtype, var,
        #irrational, and quaternion
        if type(number) == var:
            if number.solved: number = number.value
        if type(number) in Expression.ExpressionTypes:
            if number.__solved__(): return Expression.acceptType(number.value)
        if _validation.is_integer(number): return int(number)
        if _validation.is_float(number):
            new, times = round(float(number), 13), 1
            while not _validation.is_integer(new): times *= 10; new *= 10
            return Expression.divExpression(int(new), times)
        if type(number) == fraction: return Expression.divExpression(number.as_integer_ratio()[0], '/', number.as_integer_ratio()[1])
        if type(number) == complex: return quaternion(first)
        return number
        
    class divExpression(object):
        classname = 'divExpression'
        symbol = '/'
        def __init__(self, numer, denom = 1, /, frozen = False):
            Types = Expression.getTypes()
            ExpressionTypes = Expression.ExpressionTypes
            numer = Expression.acceptType(numer)
            denom = Expression.acceptType(denom)
            if type(numer) not in Types: raise TypeError
            if type(denom) not in Types: raise TypeError
            self.solved = False
            self.value = None
            self.numer = numer
            self.denom = denom
            self.Types = Types
            self.ExpressionTypes = ExpressionTypes
            self.frozen = bool(frozen)
            if not self.frozen: self.simplify()

        def frozen_check(self):
            if self.frozen: raise FrozenError(self)

        def simplify(self):
            WarnOnce2()
            self.frozen_check()
            if self.denom == self.numer: self.numer, self.denom = 1, 1
            if self.__solved__(): return
            if type(self.denom) is quaternion:
                self.numer = Expression.acceptType(self.numer*self.denom.converse())
                self.denom = Expression.acceptType(self.denom*self.denom.converse())
                ngcd = findgcd(self.denom, self.numer)
                self.numer, self.denom = self.numer//ngcd, self.denom//ngcd
                return
            if type(self.denom) is int is type(self.numer):
                ngcd = gcd(self.denom, self.numer)
                self.numer, self.denom = self.numer//ngcd, self.denom//ngcd
                return
            if type(self.denom) is self.__class__ is type(self.numer):
                nlcm = lcm(self.numer.denom, self.denom.denom)
                self.numer = Expression.acceptType(self.numer*nlcm)
                self.denom = Expression.acceptType(self.denom*nlcm)
                return
            if type(self.denom) is self.__class__:
                nlcm = self.denom.denom
                self.numer = Expression.acceptType(self.numer*nlcm)
                self.denom = Expression.acceptType(self.denom*nlcm)
                return
            if type(self.numer) is self.__class__:
                nlcm = self.numer.denom
                self.numer = Expression.acceptType(self.numer*nlcm)
                self.denom = Expression.acceptType(self.denom*nlcm)
                return
            if type(self.denom) in self.ExpressionTypes:
                #NOT IMPLEMENTED
                # Maybe something like
                #if type(self.numer) in (int, quaternion, var, irrational):
                #   return
                #self.numer.is_divisible_by(self.denom):
                #   self.set(self.numer/self.denom)
                return
            if type(self.denom) in (irrational, var):
                #Not quite worked out
                return

        def __gcd__(self):#IMPLIMENT LATER
            WarnOnce2()
            pass

        def gcd(self, other): #IMPLIMENT LATER
            WarnOnce2()
            pass

        def rgcd(other, self):
            WarnOnce2()
            pass

        def set(self, to):
            WarnOnce2()
            if type(to) is self.__class__:
                self.numer = to.numer
                self.denom = to.denom
                self.solved = to.solved
                self.value = to.value
                return
            self.solved = True
            self.value = to

        def __repr__(self):
            WarnOnce2()
            if self.__solved__():
                return repr(self.value)
            return str(self)

        def __str__(self):
            WarnOnce2()
            if self.frozen: return 'DivExpression('+str(self.numer)+'/'+str(self.denom)+')'
            self.simplify()
            def center(multistring, linelen):
                newlist = []
                for line in multistring.split('\n'):
                    newlist.append(line.center(linelen))
                return '\n'.join(newlist)
            if self.__solved__(): return str(self.value)
            top = str(self.numer)
            bottom = str(self.denom)
            toplen = max(list(map(len, top.split('\n'))))
            bottomlen = max(list(map(len, bottom.split('\n'))))
            linelen = max(toplen, bottomlen)+2
            top = center(top, linelen)
            bottom = center(bottom, linelen)
            return top + '\n' + ('–'*linelen) + '\n' + bottom

        def reciprocal(self):
            WarnOnce2()
            self.frozen_check()
            return self.__class__(self.denom, self.numer)

        def __mul__(self, other):
            WarnOnce2()
            self.frozen_check()
            other = Expression.acceptType(other)
            if self.solved: return other*self.value
            if type(other) in self.ExpressionTypes:
                return self.__class__(other*self.numer, self.denom)
            return self.__class__(self.numer*other, self.denom)

        def __add__(self, other):
            WarnOnce2()
            self.frozen_check()
            if self.frozen: raise FrozenError
            if self.solved: return self.value+other
            other = Expression.acceptType(other)
            if type(other) in (int, quaternion) and type(self.numer) == int: other = self.__class__(other)
            if type(other) not in self.Types: raise TypeError
            if type(other) is self.__class__: return self.__class__(((self.numer * other.denom) + (other.numer * self.denom)), (self.denom*other.denom))
            answer = Expression.addExpression(self, other)
            if answer.solved(): return answer.value
            return answer

        def __radd__(other, self):
            WarnOnce2()
            self.frozen_check()
            return other+self

        def __sub__(self, other):
            WarnOnce2()
            self.frozen_check()
            return self + (other*-1)

        def __rsub__(other, self):
            WarnOnce2()
            self.frozen_check()
            return (other*-1)+self

        def __truediv__(self, other):
            WarnOnce2()
            self.frozen_check()
            return self*(self.__class__(other).reciprocal())

        def __solved__(self):
            WarnOnce2()
            self.frozen_check()
            if self.solved: return self.solved
            if self.denom == 1: self.set(self.numer)
            return self.solved

    class addExpression(object):
        classname = 'addExpression'
        symbol = '+'
        def __init__(self, *terms):
            WarnOnce2()
            if len(terms) == 0: raise TypeError
            self.Types = Expression.getTypes()
            self.ExpressionTypes = Expression.ExpressionTypes
            termlist = list(map(Expression.acceptType, terms))
            for term in termlist:
                if type(term) not in self.Types: raise TypeError
            self.terms = termlist
            self.solved = False
            self.value = None
            self.simplify()

        def simplify(self):
            WarnOnce2()
            ncount = 0
            terms = self.terms.copy()
            newterms = []
            while terms:
                current = terms.pop(ncount)
                tcount = 0
                while tcount < len(terms):
                    try:
                        current += terms[tcount]
                        terms.pop(tcount)
                    except:
                        try:
                            current = terms[tcount] + current
                            terms.pop(tcount)
                        except:
                            tcount += 1
                newterms.append(current)
            terms = newterms
            if len(terms) == 1:
                self.solved = True
                self.value = terms[0]
            self.terms = terms

        def __gcd__(self):
            WarnOnce2()
            return findgcd(*self.terms)

        def __str__(self):
            WarnOnce2()
            if self.__solved__(): return str(self.value)
            return ' + '.join(list(map(str, self.terms)))

        def __repr__(self):
            WarnOnce2()
            if self.__solved__(): return str(self.value)
            return str(self.terms) #Also temporary

        def __solved__(self):
            WarnOnce2()
            if self.solved: return self.solved
            if len(self.terms) == 1:
                self.solved = True
                self.value = self.terms[0]
            return self.solved

        def __add__(self, other):
            WarnOnce2()
            other = Expression.acceptType(other)
            if self.solved: return self.__class__(self.value, other)
            if type(other) == self.__class__:
                return self.__class__(*(self.terms + other.terms))
            else:
                nterms = self.terms.copy()
                nterms.append(other)
                return self.__class__(*nterms)

    class mulExpression(object):
        classname = 'mulExpression'
        symbol = '*'
        def __init__(self, *terms):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class expExpression(object):
        classname = 'expExpression'
        symbol = '^'
        def __init__ (self, base, power = 1):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class rootExpression(object):
        classname = 'rootExpression'
        symbol = 'rt'
        def __init__(self, base, root = 1):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class logExpression(object):
        classname = 'logExpression'
        symbol = 'log'
        def __init__(self, number, base = 10):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class cosExpression(object):
        classname = 'cosExpression'
        symbol = 'cos'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class sinExpression(object):
        classname = 'sinExpression'
        symbol = 'sin'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__)  + 'has not been implemented yet')

    class tanExpression(object):
        classname = 'tanExpression'
        symbol = 'tan'
        def __init__(self, angle):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    class lnExpression(object):
        classname = 'lnExpression'
        symbol = 'ln'
        def __init__(self, number):
            raise NotImplementedError(repr(self.__class__) + 'has not been implemented yet')

    ExpressionTypes = (divExpression, addExpression)
    varTypes = (var, irrational)

#eof
