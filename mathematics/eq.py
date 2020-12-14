'''
File: eq.py
Version: 2.1.5
Author: Austin Garcia

This program stores the 'eq' class. It takes a string of an expression of a
function and returns an 'eq' object, which can be called with a number which
replaces the variable with a number.

Note: I originally created this for a specific sceneario in a graphing program
I created that used this to make a turtle graph an input equation. While I am
sure that there are other practical uses for this, some areas are only develope
as necessary within the original program, though I have attempted to broaden its
abilities.

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1
   eq is stored as a function with a list as a non-positional argument that
   defaults to the data, this equation is returned from a function 'make_eq'
  Version 1.1.2
   some bug fixes and whatnot.
 1.2
  Version 1.2.1
   Things moved around, a few new functions added
2
 2.1
  2.1.1
   Swiched to using a class for eq. Everything has been moved around. More
   efficient and elegant code
  2.1.2
   added 'prepare' and 'create' to avoid small bugs. added 'translations',
   'constants', and 'mathfuncs' for same reason 
  2.1.3
   eq class is now callable, a small bugfix or two.
   added to the usefulpy module
  2.1.4
   Really, really small bugfixes, and thus small improvements in quality.
  2.1.5
   Hopefully fixed a couple elusive bugs...
   Improvement with 'create' and involving function.
   
   Functions are addable.

'''

__version__ = '2.1.5'

try: from nmath import *
except: from usefulpy.mathematics.nmath import *

from usefulpy import formatting
import copy

translations = {'cos':'\\cos ', 'sin':'\\sin ', 'tan':'\\tan ',
                'arccos':'\\arccos ', 'arcsin':'\\arcsin ',
                'sqrt': '\\sqrt ', 'cbrt':'\\cbrt ', 'rt': '\\rt ',  'arctan':'\\arctan ',
                'log':'\\log ', 'ln':'\\ln ', 'π':'\x0epi ', 'τ':'\x0etau ',
                'e':'\x0ee ', 'Φ': '\x0ephi ', 'φ':'\x0elphi ', 'ρ': '\x0erho ',
                'σ': '\x0esigma ', 'ς': '\x0elsigma ', 'κ': '\x0ekappa ',
                'ψ': '\x0epsi ', '**':'^', '\\sq\\rt':'\\sqrt', '\\cb\\rt':'\\cbrt'}
constants = {'\x0epi': π, '\x0etau': τ, '\x0ee': e, '\x0ephi': Φ, '\x0elphi': φ,
             '\x0erho': ρ, '\x0esigma': σ, '\x0elsigma': ς, '\x0ekappa': κ,
             '\x0epsi': ψ}
mathfuncs = {'\\cos': (cos, (1,)), '\\sin': (sin, (1,)), '\\tan': (tan, (1,)),
             '\\arccos': (acos, (1,)), '\\arcsin': (asin, (1,)),
             '\\arctan' : (atan, (1,)), '\\log': (log, (1, (2,))),
             '\\ln': (ln, (1,)), '\\sqrt': (sqrt, (1,)), '\\cbrt':(cbrt, (1,)),
             '\\rt':(rt, (-2, 1))}
parenthesis = '()'
digits = '0.123456789'
operations = '^+-*/'
implied = 'im*'

fns = {}

def create(text):
    text = text.replace(' ', '')
    while '--' in text: text = text.replace('--', '+')
    while '++' in text: text = text.replace('++', '+')
    while '+-' in text: text = text.replace('+-', '-')
    while '-+' in text: text = text.replace('-+', '-')
    text = text.replace('**', '^')
    var = None
    if text[1] == '(' and text[3:5] == ')=':
        var = text[2]
        fnnm = text[0]
        text = text[5:]
    text = formatting.translate(text, translations)
    ntext = ''
    fn = False
    for x in text:
        if fn:
            if x == ' ': fn = False
            if x in digits: ntext += ' ' + x
            else: ntext += x
        else:
            if x in ('\\', '\x0e'):
                ntext += x
                fn = True
            elif x not in digits: ntext += ' '+x+' '
            else: ntext+= x
    if text.startswith('-'): text+='0 '
    text = (ntext+' ').replace('  ', ' ')
    neq = eq(text, var)
    try: fns[fnnm] = neq
    return neq

class eq(object):
    def __init__(self, text, var = None):
        ''' creates a function from text that can be solved for a single
variable while slower compared to a regular function, it has the ability to
create this from *input* which is what makes it useful'''
        parameter = None
        if type(text) == self.__class__:
            self = copy.deepcopy(text)
        if '"' in text:
            index = text.index('"')
            text = text[:index]
            del index
        if '{' in text:
            index = text.index('{')
            text, parameter = text[:index], text[index:]
            del index
        self.text = text+' '
        self.ParameterText = parameter
        self.parameter = self.makeParameter()
        self.var = var
        self.neq = self.makeEq()
        self.solved = False
        self.value = None
        if self.var is None:
            self.value = self.solve(0)
            self.solved = True

    def makeParameter(self): return NotImplemented #Working on it

    def __eq__(self, other):
        if type(other) != self.__class__: return False
        return self.neq == other.neq

    def makeEq(self):
        text = self.text
        if text.count('(') != text.count(')'):
            raise SyntaxError('Parenthesis nesting error occured')
        nlist = []
        runstr = ''
        depth = 0
        var = self.var
        inner = False
        fn = False
        na = 'na' #To avoid errors regarding '-' placed first
        prevtype = na #To avoid 'implied multiplication' leading to errors
        num = 'num' #support for prevtype
        oper = 'oper'#support for prevtype
        va = 'var' #support for prevtype
        f = 'fn'#support for prevtype
        c = 'special'#support for prevtype
        p = '()'
        nprev = None
        for char in text:
            l = runstr
            if depth == 0:
                if char == ')':
                    raise SyntaxError('Parenthesis nesting error occured')
                elif char == '(':
                    depth += 1
                    if runstr != '':
                        if runtr == '-':
                            nlist.append(-1)
                            prevtype = num
                        else:
                            nlist.append(runstr)
                            if validation.is_float(runstr): curtype = num
                            elif runstr in operations: curtype = oper
                            elif runstr.startswith('\\'): curtype = f
                            elif runstr.startswith('\x0e'): curtype = c
                            else:
                                if var == None:
                                    if runstr.startswith('-'):
                                        var = runstr[1:]
                                    else:
                                        var = runstr
                                    curtype = va
                                elif runstr == var: curtype = va
                                else: raise SyntaxError(runstr + ' seems to be an invalid character')
                            prevtype = curtype
                    if prevtype in (va, num, c, p):
                        nlist.append
                    nlist.append(runstr)
                    runstr = '('
                elif char == ' ':
                    if runstr != '':
                        if validation.is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var: curtype = va
                            else: raise SyntaxError(runstr + ' seems to be an invalid character')
                        if prevtype in (va, num, c, p):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        if runstr == '-' and prevtype == na: pass
                        elif runstr == '-' and prevtype == oper: pass
                        else: nlist.append(validation.trynumber(runstr)); runstr = ''
                        prevtype = curtype
                        if fn: fn = False
                elif char == '\\' or char == '\x0e':
                    fn = True
                    if runstr != '':
                        if validation.is_float(runstr): curtype = num
                        elif runstr in operations: curtype = oper
                        elif runstr.startswith('\\'): curtype = f
                        elif runstr.startswith('\x0e'): curtype = c
                        else:
                            if var == None:
                                if runstr.startswith('-'):
                                    var = runstr[1:]
                                else:
                                    var = runstr
                                curtype = va
                            elif runstr == var: curtype = va
                            else: raise SyntaxError(runstr + ' seems to be an invalid character')
                        if prevtype in (va, num, c):
                            if curtype == oper: pass
                            else: nlist.append(implied)
                        prevtype = curtype
                    nlist.append(validation.trynumber(runstr))
                    runstr = char
                elif fn:
                    runstr += char
                elif char in operations:
                    runstr = char
                else:
                    if runstr == '':
                        runstr += char
                    elif validation.is_float(runstr) or runstr == '-' or runstr == '.' or runstr == '-.':
                        if validation.is_float(char) or char == '.':
                            runstr += char
                        elif runstr == '-':
                            runstr += char
                        else:
                            nlist.append(validation.trynumber(runstr))
                            nlist.append(implied)
                            runstr = char
                    elif validation.is_float(char):
                        nlist.append(validation.trynumber(runstr))
                        nlist.append(implied)
                        runstr = char
                    else: runstr += char
            else:
                runstr += char
                if char == ')': depth -= 1
                elif char == '(': depth += 1
                if depth == 0:
                    ceq = eq(runstr[1:-1])
                    if ceq.solved: ceq = ceq.value
                    elif var == None: var = ceq.var
                    else:
                        if ceq.var != var: raise SyntaxError(ceq.var + ' seems to be an invalid character')
                    nlist.append(ceq)
                    prevtype = p
                    runstr = ''
            nprev = l
        self.var = var
        if nlist[0] == '+': nlist = nlist[1:]
        nlist = formatting.scour(nlist)
        if len(nlist) == 1 and (type(nlist[0]) is self.__class__): nlist = nlist[0]
        return nlist

    def __repr__(self):
        if self.solved:
            return '('+str(self.value)+')'
        reprtranslate = {'[':'(', ']':')', ',':'', "'":'', '\\':'', ' im* ':''}
        return formatting.translate(str(self.neq), reprtranslate)

    def solve(self, value):
        if self.solved: return self.value
        Nlist = self.neq.copy()
        def s(Nlist):
            count = 0
            for x in Nlist.copy():
                if self.var != None:
                    if x == self.var:
                        Nlist[count] = value
                    if x == ('-'+self.var):
                        Nlist[count] = 0-value
                if type(x) == str:
                    if x in constants:
                        Nlist[count] = constants[x]
                count += 1
            return Nlist
        def p(Nlist):
            count = 0
            for x in Nlist.copy():
                if type(x) is self.__class__:
                    Nlist[count] = x.solve(value)
                count +=1
            return Nlist
        def e(Nlist):
            while '^' in Nlist:
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    try:
                        if prev1 == '^':
                            Nlist[count-3:count] = [prev2**x]
                            break
                    except: pass
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def imp(Nlist):
            while (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == implied:
                        if validation.is_float(prev2) and validation.is_float(x):
                            Nlist[count-3:count] = [prev2*x]
                            break
                        else: pass
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def f(Nlist):
            #see mathfuncs
            def done(Nlist):
                for x in Nlist:
                    if (type(x) is str) and (x.startswith('\\')):
                        return False
            while not done(Nlist):
                index = 0
                for x in Nlist.copy():
                    if (type(x) is str) and (x.startswith('\\')):
                        if Nlist[index+1] == '^':
                            Nlist.pop(index+1)
                            power = Nlist.pop(index+1)
                        else: power = 1
                        funcdata = mathfuncs[x]
                        fx = funcdata[0]
                        pardata = funcdata[1]
                        args = []
                        
                        for datum in pardata:
                            args.append(Nlist[index+datum])
                        nvalue = fx(*args)
                        pardata = list(pardata)
                        pardata.append(0)
                        spacer = (min(pardata), max(pardata))
                        Nlist[index+spacer[0]:1+index+spacer[1]] = [nvalue**power]
                    index +=1
                else: break
            return Nlist
        
        def m(Nlist):
            while ('*' in Nlist) or ('/' in Nlist) or (implied in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '*' or prev1 == implied:
                        Nlist[count-3:count] = [prev2*x]
                        break
                    elif prev1 == '/':
                        Nlist[count-3:count] = [prev2/x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def a(Nlist):
            while ('+' in Nlist) or ('-' in Nlist):
                prev1 = ''
                prev2 = ''
                count = 1
                for x in Nlist.copy():
                    if prev1 == '+':
                        Nlist[count-3:count] = [prev2+x]
                        break
                    elif prev1 == '-':
                        Nlist[count-3:count] = [prev2-x]
                        break
                    prev2 = prev1
                    prev1 = x
                    count +=1
                else: break
            return Nlist
        def b(Nlist):
            while len(Nlist) != 1:
                prev = ''
                count = 0
                for x in Nlist.copy():
                    if validation.is_float(x) and validation.is_float(prev):
                        if x < 0:
                            Nlist[count-1:count+1] = [prev+x]
                            break
                        else:
                            Nlist[count-1:count+1] = [prev*x]
                            break
                    elif prev == '-' and validation.is_float(x):
                        Nlist[count-1, count] = [-x]
                    count += 1
                    prev = x
                else: break
            return Nlist
        OOP = 'spifemab'
        oop = {'s': s, 'p':p, 'f':f, 'i': imp, 'e':e, 'm': m, 'a':a, 'b':b}
        for op in OOP:
            Nlist = oop[op](Nlist)
        if len(Nlist)==1:
            return validation.trynumber(Nlist[0])
        else:
            raise ValueError(Nlist)
    def __call__(self, num):
        return self.solve(num)

    def __str__(self):
        return repr(self)

    def __add__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self)[1:-1])+' + '+(repr(other)[1:-1]))

    def __radd__(self, other):
        return self+other

    def __mul__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+(repr(other)))

    def __rmul__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+(repr(self)))

    def __sub__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+'-'+(repr(other)))

    def __truediv__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(self))+'/'+(repr(other)))

    def __rsub__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+'-'+(repr(self)))

    def __rtruediv__(self, other):
        if type(other) is not self.__class__: other = create(str(other))
        return create((repr(other))+'/'+(repr(self)))

#eof
