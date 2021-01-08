'''
File: validation.py
Version: 1.1.2
Author: Austin Garcia

This program contains many useful functions for validation of input and output.

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   validation.py contains various useful modules for validation of input and
   output
  Version 1.1.2:
   An updated description and various bug fixes. Cleaner looking code with more
   comments. Addition of several different biases, now imports random.

'''
__version__ = '1.1.2'
import datetime
from collections import namedtuple, deque

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
    if is_integer(s): return int(float(s))
    return s

#Necessary for 'fromrepr', essentially a dictionary with a single item.
class _keyob(object):
    '''Support for fromrepr'''
    def __init__(self, arg:str):
        self.k = arg[:arg.index(':')]
        self.y = arg[arg.index(':')+1:]

def fromrepr(s:str):
    '''not perfect, but it is supposed to be the inverse of repr(x)=s'''
    #If the s is a number
    if is_float(s):
        if '.' not in s: return int(s)
        return float(s)

    #Boolean and Nonetype values
    if s == 'True': return True
    if s == 'None': return
    if s == 'False': return False

    #if it is a string
    if (s[0] in ('"', "'")) and (s[-1] == x[0]):
        s = s[1:-1]

        #I originally used a for loop, but I switched it for a while loop.
        #escape characters have an added // in the repr
        count = 0
        while count < len(s):
            if s[count] == '\\' and s[count+1] != '\\':
                s = s[:count]+s[count+1:]
            else: count +=1
        return s

    #iterables
    if s[0] == '[' and s[-1] == ']':
        return makelist(s)
    if s[0] == '(' and s[-1] == ')':
        return tuple(makelist(s))
    if s[0] == '{' and s[-1] == '}':
        nlist = makelist(s)
        #this hopefully accounts for dictionaries correctly, and doesn't leave
        if _keyob in map(type, nlist):
            ndict = {}
            for ob in nlist: ndict[ob.k] = ob.y
            return ndict
        return set(nlist)
    if ':' in s: return _keyob(s)

    #If all else fail.
    return s

def makelist(*s):
    '''Makes a list out of nearly any input of any type'''
    if len(s) == 0: return []
    if len(s) > 1: return list(s)
    s = s[0]
    if type(s) is list: return s
    if type(s) in (tuple, set): return list(s)
    if type(s) is str:
        inverses = str.maketrans('({[]})',')}][{(')
        if (s[0] in ('(', '[', '{')) and (s[0] == s[-1].translate(inverses)):
            #the list
            runlist = []
            
            # is it nested an interator
            in_iter = False
            #what started the iterator, and the iterator within an iterator, etc
            neststarters = deque()
            # I am using a deque object because they are
            # more efficient
            #
            #depth level
            level = 0 

            #is it within a string?
            instr = False
            #was the string started with a '"' or a "'"?
            strstart = ''
            #is the escapecharacter being used?
            eschar = False

            #What is the current object of the list.
            runobject = ''
            for x in s[1:-1]:
                if not instr and not in_iter:
                    if x in ('(', '[', '{'):
                        in_iter = True
                        level += 1
                        runobject += x
                        neststarters.append(x)
                    elif x in ('"', "'"):
                        instr = True
                        runobject += x
                        strstart = x
                    elif x in (','):
                        runlist.append(fromrepr(runobject))
                        runobject = ''
                    elif x == ' ':
                        pass
                    else:
                        runobject += x
                elif instr:
                    runobject += x
                    if x == strstart and not eschar:
                        instr = False
                    if x == '\\': eschar = True
                    else: eschar = False
                elif in_iter:
                    runobject += x
                    if x in ('"', "'"):
                        instr = True
                        strstart = x
                    elif x in ('(', '[', '{'):
                        in_iter = True
                        level += 1
                        neststarters.append(x)
                    elif x == neststarters[-1]:
                        neststarters.popleft()
                        level -= 1
                        if level == 0:
                            in_iter = False
            if runobject: runlist.append(fromrepr(runobject))
            return runlist
        else: return s.split()
    try: return [x for x in s]
    except: return [s]

def is_intlist(s):
    '''Check if a list is composed solely of integers'''
    try:
        Numbers = list(map(float, makelist(s)))
        Valid = list(map(is_integer, Numbers))
        return not (False in Valid)
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
    try: Numbers = list(map(float, NumbersStr.split())); return True
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
    '''
    This part is a big mess despite its simple job. there can be multiple
    prompts at once. and numinputs is the number of inputs... this will overide
    number of prompts if specified. validquery is the function that returns True
    when the input is valid, the returnclass is the function or type that
    the final input is put through. ninput is the type of input required for
    the arguments and the various input prompts...
    like I said... big mess
    '''
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
    while not validquery(*inp): print(Chastisement); inp = getinp(numinputs, *Prompt, inputtype = ninput)
    if ending != None: print(ending)
    return returnclass(*inp)

def isbool(s):
    '''Check if s is a boolean value'''
    return type(s) == bool

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

tryfloat = lambda s:trytype(float, s)

trynumber = lambda s: tryint(tryfloat(s))

from random import randint as rint, random as rnum

def lowbias(low, high):
    '''return a random integer from low to high, lower numbers have higher
weights'''
    return rint(low, rint(low, rint(low, high)))

def highbias(low, high):
    '''return a random integer from low to high, higher numbers have higher
weights'''
    return rint(rint(rint(low, high), high), high)

def centerbias(low, high):
    '''return a random integer from low to high, center numbers have higher
weights'''
    return rint(rint(low, high//2), rint(high//2, high))

def outerbias(low, high):
    '''return a random number from low to high, outermost numbers have
higher weights'''
    return choice((highbias, lowbias))(low, high)

def rbool():
    '''return a random boolean value'''
    return choice((True, False))

def truebias(chance = 75):
    '''return a random boolean value, biased to True,or a chance% to return
True'''
    return rint(1, 100) <= chance

def falsebias(chance = 75):
    '''return a random boolean value, biased to False, or a chance% to return
False'''
    return rint(1, 100) >= chance
