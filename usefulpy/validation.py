'''
validation

This program contains many useful functions for validation of input and output.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   validation.py contains various useful modules for validation of input and
   output
  Version 0.0.1:
   An updated description and various bug fixes. Cleaner looking code with more
   comments. Addition of several different biases, now imports random.
 0.1
  Version 0.1.0
    ——Friday, the fifteenth day of the firstmonth Janurary, 2021——
   Code is shorter by about fifty lines, and yet its functionality have
   increased... Simplicity is better! Who knew?
  Version 0.1.1
   Small bugfixes
'''

__author__ = 'Augustin Garcia'
__version__ = '0.1.1'

import sys
import datetime

_chastise = '''
Your input was invalid.
Please try again
'''

#for easier reference of the function type.
function = type(lambda: None)

def is_function(s):
    '''Check whether variable s is a function'''
    return type(s) is function

def is_integer(s):
    '''Check if an object is an integer can be turned into an integer without
losing any value'''
    try: return int(float(s)) == float(s)
    except: return False

def are_integers(*a):
    '''Return True if is_integer is True for all objects in a'''
    return all(map(is_integer, a))

def intinput(Prompt = '', beginning = '', ending = None, \
             Chastisement = _chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into an integer.'''
    intstr = input(beginning + Prompt)
    while not is_integer(intstr): print(Chastisement); intstr = input(Prompt)
    if ending != None: print(ending)
    return int(intstr)

def tryint(s):
    '''Try to turn an object into an integer'''
    if type(s) is int: return s
    if is_integer(s):
        try: return int(s)
        except: return int(float(s))
    return s

def fromrepr(s:str):
    '''Supposed to be the inverse of repr(x)=s'''
    try: return eval(s)
    except: return s

def makelist(*s):
    '''Makes a list out of nearly any input of any type'''
    if len(s) == 0: return []
    if len(s) > 1: return [makelist(n) for n in s]
    s = s[0]
    if type(s) is list: return s
    if type(s) in (tuple, set): return list(s)
    if type(s) is str:
        try: return makelist(eval(s))
        except: return s.split()
    try: return [x for x in s]
    except: return [s]

def is_intlist(s):
    '''Check if a list is composed solely of integers'''
    try:
        Valid = list(map(is_integer, s))
        return all(Valid)
    except: return False

def intlistinput(Prompt = '', beginning = '', ending = None, \
                 Chastisement = _chastise):
    '''Continue to repeat an input prompt until the input can be converted
into a list of integers'''
    numsstr = input(beginning + Prompt)
    while not is_intlist(numsstr): print(Chastisement); numsstr = input(Prompt)
    if ending != None: print(ending)
    return list(map(int, numsstr))

def is_float(s):
    '''Check if an object can be turned into a float'''
    try: return float(s)==float(s)
    except: return False

def are_floats(*a):
    '''Return True if is_integer is True for all objects in a'''
    return all(map(is_float, a))

def floatinput(Prompt = '', beginning = '', ending = None, \
               Chastisement = _chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a float.'''
    floatstr = input(beginning + Prompt)
    while not is_float(floatstr): print(Chastisement); floatstr = input(Prompt)
    if ending != None: print(ending)
    return float(floatstr)

def is_floatlist(s):
    '''Check if a list is composed solely of numbers'''
    try: list(map(float, s.split())); return True
    except: return False

def floatlistinput(Prompt = '', beginning = '', ending = None, \
                   Chastisement = _chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a list of floats.'''
    numsstr = input(beginning + Prompt)
    while not is_floatlist(numsstr): print(Chastisement); numsstr = input(Prompt)
    if ending != None: print(ending)
    return list(map(float, numsstr))

    
def _getinp(numinputs, *Prompts, inputtype = None):
    '''Get a number of inputs in a certain type based on prompts'''
    #support for valid inputs
    if not type(numinputs) == int: raise ValueError
    if inputtype == None: inputtype = input
    if len(Prompts) == 0: Prompts = ('',)
    if len(Prompts)>numinputs: raise ValueError
    inp = []
    for num in range(numinputs):
        try: inp.append(inputtype(Prompts[num]))
        except: inp.append(inputtype(Prompts[-1]))
    return inp

def validinput(validquery, *Prompt, returnclass = str, numinputs = None, \
               beginning = '', ending = None, Chastisement = _chastise, \
               ninput = None):
    '''Continue to repeat an input prompt until the prompt is validated by
validquery'''
    '''This part is a big mess despite its simple job. there can be multiple
prompts at once. and numinputs is the number of inputs... this will overide
number of prompts if specified. validquery is the function that returns True
when the input is valid, the returnclass is the function or type that
the final input is put through. ninput is the type of input required for
the arguments and the various input prompts...
like I said... big mess'''
    #Making sure there is a prompt (and thus, an input taken)
    if len(Prompt) == 0: Prompt = ('',)
    #if numinputs is not specified
    if numinputs == None: numinputs = len(Prompt)
    if len(Prompt) > numinputs: raise ValueError()
    #To make the first prompt different
    firstPrompt = list(Prompt).copy()
    firstPrompt[0] = beginning + firstPrompt[0]
    #gets the various inputs at once with _getinp
    inp = _getinp(numinputs, *firstPrompt, inputtype = ninput)
    while not validquery(*inp): print(Chastisement); inp = _getinp(numinputs, *Prompt, inputtype = ninput)
    if ending != None: print(ending)
    return returnclass(*inp)

def isbool(s):
    '''Check if s is a boolean value'''
    n = type(s)
    return s in ('True', 'False') if n is str else n is _bool

_bool = bool

def bool(x):
    '''bool(c) -> bool'''
    return _bool({'True':True, 'False':False}.get(x))

def boolinput(Prompt):
    '''Continue to repeat an input prompt until the input is 'True' or 'False'.'''
    return _bool(validinput(isbool, Prompt))

def fromdatainput(data, prompt = ''):
    '''Continue to repeat an input prompt until the input is a value from the
list 'data'.'''
    datum = input(prompt)
    while datum not in data: datum = input(prompt)
    return datum

def multicheck(data, checks, threshhold = 1):
    '''Check checks on data, threshold is the number of checks that need
to return a True value'''
    try: data = iter(data)
    except: data = iter((data,))
    try: checks = iter(checks)
    except: checks = iter((checks,))
    count = 0
    for n in data:
        for c in checks:
            try:
                if c(n): count += 1
                if count >= threshhold: return True
            except: pass
    return False

def multi_in(data1, data2, threshhold = 1):
    '''Check if any item in data1 is in data2. Threshold is the number of
matches there has to be'''
    try: data1 = iter(data1)
    except: data1 = iter((data1,))
    try: data2 = iter(data2)
    except: data2 = iter((data2,))
    count = 0
    for n in data1:
        if n in data2: count += 1
        if count >= threshhold: return True
    return False 
    

def YesOrNo(Response):
    '''Check if a text is an affirmative or a negative'''
    affirmatives, negatives = ('ye', 'do', 'course', 'would', 'sure'), ('no', 'n\'t', 'na', 'stop')
    response, Response = Response.lower(), None
    if response in ('true', 't', 'y') : return True
    if response in ('false', 'n', 'f'): return False
    for n in affirmatives:
        if n in response: Response = True; break
    for n in negatives:
        if n in response: Response = False; break
    if 'why' in response:
        if Response == False: Response = True
        else: Response = False
    return Response

def getYesOrNo(Prompt = '', beginning = '', ending = None, \
               Chastisement = _chastise):
    '''Continue to repeat an input prompt until the prompt can be converted
into a boolean value, this includes variations of Yes and No.'''
    response = input(beginning + Prompt)
    while YesOrNo(response) is None: print(Chastisement); response = input(Prompt)
    if ending != None: print(ending)
    return YesOrNo(response)

del _chastise

def is_numeric(s):
    '''Return True if s supports all arithmetic operations.'''
    try:
        s += 1
        s -= 1.0
        s *= 2
        s /= 2.0
        s **= 2
        s **= (1/2)
        return True
    except: return False

def validdate(year, month, day):
    '''Check if a year, month, day combo is valid'''
    try: datetime.date(year, month, day); return True
    except: return False

def validquery(ntype, *s):
    '''Check if s can be converted into a type ntype'''
    try:
        if type(*s) == ntype: return True
    except:pass
    try: ntype(*s); return True
    except: return False

def trytype(ntype, *s):
    '''Try to convert data s into a type ntype'''
    if len(s) == 1:
        s = s[0]
        if type(s) == ntype: return s
        if validquery(ntype, s): return ntype(s)
        return s
    if validquery(ntype, *s): return ntype(*s)
    return s

def is_iterable(n):
    '''Check if n is iterable'''
    try:
        for l in n: l
        return True
    except: return False

def merge_dicts(a, b, exclude = True, fill_val = None):
    ndict = {}
    for key in a:
        if key in b: ndict[key] = (a[key],b[key])
    if exclude: return ndict
    for key in b:
        ndict[key] = (a.get(key, fill_val),b.get(key, fill_val))
    return ndict

def flatten(iterable):
    '''Flatten an iterable into a single dimension'''
    assert is_iterable(iterable)
    itertype = type(iterable)
    new_iterable = []
    for n in iterable:
        if is_iterable(n):
            new_iterable.extend(list(flatten(n)))
            continue
        new_iterable.append(n)
    return itertype(new_iterable)

def tryfloat(s):
    '''Convert s to a float if is_float(s)'''
    s = tryeval(s)
    try: return float(s)
    except: return s

def tryeval(s):
    '''Tries to evaluate a string if it is a string. returns input if it cannot
be evaluated'''
    if type(s) is str:
        try: return eval(s)
        except: return s
    return s

def valideval(s):
    '''Returns True if a string can be evaluated'''
    if type(s) is str:
        try:
            eval(s)
            return True
        except: return False
    return False

class _empty:
    def write(self, *args, **kwargs): pass
    def read(self, *args, **kwargs): pass

def validexec(s):
    '''Return True if it can be executed. Note: will trigger the code.'''
    if type(s) is str:
        try:
            out = sys.stdout
            in_ = sys.stdin
            sys.stdout = _empty()
            sys.stdin = _empty()
            exec(s)
            sys.stdout = out
            sys.stdin = in_
            return True
        except: return False
    return False

def is_complex(s):
    '''Return True if s can be interpreted as a complex number'''
    s = tryeval(s)
    try:
        complex(s)
        return True
    except: return False

def trycomplex(s):
    '''Tries to convert s into a complex number'''
    s = tryeval(s)
    try: return complex(s)
    except: return s

def trynumber(s):
    '''Convert it into the simplest of an int, float, or complex'''
    s = tryeval(s)
    if type(s) in (int, float, complex): return tryint(s)
    if is_integer(s):
        try: return int(s)
        except: return int(float(s))
    if is_float(s): return float(s)
    if is_complex(s): return complex(s)
    return s

#eof
