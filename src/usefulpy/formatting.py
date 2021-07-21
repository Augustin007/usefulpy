'''
formatting

Several useful functions for formatting output.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   formatting.py contains a small amount of functions for formatting.
  Version 0.0.1
   An updated description, some bug fixes
 0.1
  Version 0.1.0:
   Addition of 'color', 'composenumber', 'syllable', 'write' and 'unformat'
  Version 0.1.1:
   Some small bug fixes
   Raises warnings at unfinished sections
  Version 0.1.2
   More bug fixes
  Version 0.2.3
   A couple new stuff, mostly dealing with the long s
  Version 0.2.4
   Bugfixes, deactivated section of multline... will be reimplemented soon.
'''

__version__ = '0.2.4'
__author__ = 'Augustin Garcia'

from . import validation as _validation

vowels = 'aeiou'
endingpuncuation = '.?!'
phrasepuncuation = ',–—()"\';:'
inwordpunctuation = '-_'

# The letters are in an inconsistant and incorrect order to prevent the attempt
# to translate 'Upsilon' for example, returning Uψlon, though adding 'lσ'='ς'
# Uψlon = 'Υ', 'uψlon'='υ', 'Eψlon' ='Ε', 'eψlon' ='ε' may be advisable in a
# gui environment that translates the letters as they are typed.
#
# This is the way I did it.
# 
# replacements = formatting.greek_letters
# replacements['lσ']='ς'
# replacements['Uψlon']='Υ'
# replacements['Eψlon']='Ε'
# replacements['eψlon']='ε'
# replacements['uψlon']='υ'
#


greek_letters = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ',
                 'epsilon': 'ε', 'zeta': 'ζ', 'theta': 'θ', 'iota': 'ι',
                 'kappa': 'κ', 'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ',
                 'omicron': 'ο', 'pi': 'π', 'rho': 'ρ', 'lsigma':'ς',
                 'sigma':'σ', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ',
                 'chi': 'χ', 'omega': 'ω', 'Alpha': 'Α', 'Beta': 'Β',
                 'Gamma': 'Γ', 'Delta': 'Δ', 'Epsilon': 'Ε', 'Zeta': 'Ζ',
                 'Eta': 'Η', 'Theta': 'Θ', 'Iota': 'Ι', 'Kappa': 'Κ',
                 'Lambda': 'Λ', 'Mu': 'Μ', 'Nu': 'Ν', 'Xi': 'Ξ', 'Omicron': 'Ο',
                 'Pi': 'Π', 'Rho': 'Ρ', 'Sigma': 'Σ', 'Tau': 'Τ',
                 'Upsilon': 'Υ', 'Phi': 'Φ', 'Chi': 'Χ', 'Psi': 'Ψ', 'eta': 'η',
                 'Omega': 'Ω', 'psi': 'ψ'}

#Temporary, eventually will add all the other characters and superscript
subscript = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')

def cap(string):
    '''capitalize first letter'''
    return string[0].upper()+string[1:]

def a_an(nextword):
    '''use a or an as an article for nextword'''
    for vowel in vowels:
        if nextword.startswith(vowel) and vowel != 'u': return 'an'
    return 'a'

def punctuate(n, witha = '.'):
    '''adds a punctuation, strips of old punctuation'''
    if witha not in endingpuncuation: raise ValueError(f'{witha} not in {endingpuncuation}')
    n.rstrip(endingpuncuation)
    n += witha
    return n

def multisplit(string, *by, whitespacetoo = False):
    '''split by various keys'''
    if not by: 
        if whitespacetoo:
            return string.split()
        return [string]
    if whitespacetoo:
        run = string.split()
    else:
        splitter = by[0]
        by = by[1:]
        run = string.split(splitter)
    for splitter in by:
        nrun = []
        for n in run:
            nrun.extend(n.split(splitter))
        run = nrun
    return scour(run)

def translate(string, translater):
    '''Translate all items in translator'''
    for old, new in translater.items(): string=string.replace(old, new)
    return string

def scour(obj, of= ''):
    '''remove all instances of 'of' from 'obj' '''
    if type(obj) is str:
        if type(of) is str: return obj.replace(of, '')
        for key in of: obj=obj.replace(key, '')
        return obj
    if type(obj) is list:
        if type(of) is str:
            count = 0
            for c in obj.copy():
                if c == of: obj.pop(count)
                else: count += 1
            return obj
        count = 0
        for c in obj.copy():
            if c in of: obj.pop(count)
            else: count += 1
        return obj

long_s = 'ſ'

def Fix_stolong(text):
    '''replace certain instances of s with long s according to older spelling rules'''
    if text == '': return ''
    if 's' not in text: return text
    textm1 = ' '+text[:-1]
    textp1 = text[1:]+' '
    ntext = ''
    for prevchar, char, nextchar in zip(textm1, text, textp1):
        if char == 's':
            if prevchar in ('sſf'):
                ntext+=char
            elif nextchar in '?!,–—()";:kfb_ ':
                ntext += char
            else:
                ntext += long_s
            continue
        ntext += char
    return ntext

def Fix_longtos(text):
    '''Replace long s with s'''
    return text.replace('ſ', 's')

_numbers={
        'zero': 0,
        'one':1,
        'two':2,
        'three':3,
        'four':4,
        'five':5,
        'six':6,
        'seven':7,
        'eight':8,
        'nine':9,
        'eleven':11,
        'twelve':12,
        'thirteen':13,
        'fourteen':14,
        'fifteen':15,
        'sixteen':16,
        'seventeen':17,
        'eighteen':18,
        'nineteen':19,
        'ten':10,
        'twenty':20,
        'thirty':30,
        'forty':40,
        'fifty':50,
        'sixty':60,
        'seventy':70,
        'eighty':80,
        'ninety':90
        }
_furtherplaces = {
        'thousand': 1000,
        'million': 1000000,
        'billion': 1000000000,
        'trillion': 1000000000000,
        'quatrillion': 1000000000000000,
        'quitillion': 1000000000000000000,
        'hexillion': 1000000000000000000000,
        'septillion': 1000000000000000000000000,
        'octillion': 1000000000000000000000000000
        }
def unformat(text: str, /, query = 1):
    '''Remove all capitals from text, strip it of extra spaces, translate
written-out greek-letters or numbers. Et cetera'''
    numbers = _numbers
    hundred = 'hundred'
    dozen = 'dozen'
    furtherplaces=_furtherplaces
    text = text.lower()
    punct = endingpuncuation+phrasepuncuation
    listtext = text.split()
    loop = text.split()
    index = 0
    for word in loop:
        if word[-1] in punct:
            listtext[index] = word[:-1]
            listtext.insert(index+1, word[-1])
            word=listtext[index]
            add=2
        else: add = 1
        listtext[index] = _validation.trynumber(word)
        if word in numbers: listtext[index] = numbers[word]
        if word in greek_letters: listtext[index] = greek_letters[word]
        index += add
    runtext = []
    is_prevnum = False
    prevnum = 0
    runcount = 0
    is_postpoint = False
    hundredsgroup = 0
    postpointruncount = ''
    for word in listtext:
        if _validation.is_integer(word) or _validation.is_float(word):
            if is_postpoint:
                postpointruncount += str(word)
            elif is_prevnum:
                if len(str(prevnum)) <= len(str(word)):
                    runcount += hundredsgroup
                    runcount = _validation.trynumber(str(runcount) + str(word))
                else:
                    hundredsgroup += word
            else:
                is_prevnum = True
                hundredsgroup = word
            prevnum = word
        elif word == hundred:
            hundredfactor = 100
            if is_postpoint:
                postpointruncount += str(100)
            elif is_prevnum and hundredsgroup:
                hundredsgroup *= hundredfactor
            else:
                is_prevnum = True
                hundredsgroup = hundredfactor
            prevnum = hundredfactor
        elif word in furtherplaces:
            multfactor = furtherplaces[word]
            if is_postpoint:
                nn = float(postpointruncount)*multfactor
                if _validation.is_integer(nn):
                    is_postpoint = False
                    postpointruncount = ''
                    runcount= nn
                else:
                    postpointruncount = str(nn)
                postpointruncount += str(multfactor)
            elif is_prevnum and hundredsgroup:
                runcount += (hundredsgroup*multfactor)
            else:
                is_prevnum = True
                runcount = multfactor
            hundredsgroup = 0
            prevnum = multfactor
        elif (word in ('point', '.')) and is_prevnum:
            is_postpoint = True
            postpointruncount = str(runcount + hundredsgroup)+'.'
            runcount = 0
            hundredsgroup = 0
        else:
            is_dozen = word == dozen
            if is_prevnum:
                if is_postpoint:
                    if is_dozen:
                        postpointruncount = str(float(postpointruncount)*12)
                    runtext.append(postpointruncount)
                    postpointruncount = ''
                    is_postpoint = False
                else:
                    if is_dozen:
                        runcount = (runcount + hundredsgroup)*12
                        hundredsgroup = 0
                    runtext.append(str(_validation.trynumber(runcount + hundredsgroup)))
                    runcount = 0
                    hundredsgroup = 0
                is_prevnum = False
                prevnum = 0
                if not is_dozen:
                    runtext.append(word)
            elif is_dozen:
                runtext.append('12')
            else: runtext.append(word)
    if is_prevnum:
        if is_postpoint:
            runtext.append(postpointruncount)
            postpointruncount = ''
        else:
            runtext.append(str(_validation.trynumber(runcount + hundredsgroup)))
            runcount = 0
            hundredsgroup = 0
        is_prevnum = False
        prevnum = 0
    if query: return ' '.join(runtext)
    else: return runtext

def write(text):
    '''Adds comas to numbers.'''
    if ' ' in text: return ' '.join(map(write, text.split()))
    if '.' not in text: num = _validation.tryint(text)
    else: num = _validation.tryfloat(text)
    if type(num) is int:
        numstr = str(num)
        nicenum = ''
        for count, letter in enumerate(numstr):
            nicenum += letter
            if (len(numstr)-(count+1))%3 == 0 and (len(numstr)-(count+1)) != 0:
                nicenum += ','
        return nicenum
    if type(num) is float:
        intpart = text[:text.index('.')]
        floatpart =  text[text.index('.'):]
        return write(intpart) + floatpart
    return text
_Digit = {
    '0': '',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine'
    }
_tensPlace = {
    '1': 'ten',
    '2': 'twenty',
    '3': 'thirty',
    '4': 'forty',
    '5': 'fifty',
    '6': 'sixty',
    '7': 'seventy',
    '8': 'eighty',
    '9': 'ninety'
    }
_OddOnes = {
    '11': 'eleven',
    '12': 'twelve',
    '13': 'thirteen',
    '14': 'fourteen',
    '15': 'fifteen',
    '16': 'sixteen',
    '17': 'seventeen',
    '18': 'eighteen',
    '19': 'nineteen'
    }
_LargeGroups = {
    '1': 'thousand',
    '2': 'million',
    '3': 'billion',
    '4': 'trillion',
    '5': 'quatrillion',
    '6': 'quitillion',
    '7': 'hexillion',
    '8': 'septillion',
    '9': 'octillion',
    }
def _TensGroup(num):
    '''support for compose number'''
    if str(num) in _OddOnes: return _OddOnes[str(num)]
    else:
        if str(num)[0] == '0': return _Digit[(str(num)[1])]
        if str(num)[1] == '0': return _tensPlace[(str(num)[0])]
        return _tensPlace[(str(num)[0])] + ' ' + _Digit[(str(num)[1])]
def _HundredsGroup(num):
    '''support for compose number'''
    num = str(int(num))
    if int(num) == 0: return ''
    elif len(str(num)) == 1: return _Digit[str(num)]
    elif len(str(num)) == 2: return _TensGroup(num)
    elif len(str(num)) == 3:
        if str(num)[1:] == '00': return _Digit[(str(num)[0])] + ' hundred'
        return _Digit[(str(num)[0])] + ' hundred ' + _TensGroup((str(num)[1:]))
    

def ComposeNumber(integer:int):
    '''
Converts a number into a string, fails if number is bigger than
999999999999999999999999999999 (nine hundred ninety nine octillion nine hundred ninety nine septillion nine hundred ninety nine hexillion nine hundred ninety nine quitillion nine hundred ninety nine quatrillion nine hundred ninety nine trillion nine hundred ninety nine billion nine hundred ninety nine million nine hundred ninety nine thousand nine hundred ninety nine)

>>> ComposeNumber(100)
'one hundred\''''
    LargeGroups=_LargeGroups
    HundredsGroup=_HundredsGroup
    strint = str(integer)
    Places = len(strint)
    
    if integer == 0: return 'zero'
    elif Places <= 3: return HundredsGroup(strint)
    
    Group = (Places-1)//3
    extra = Places - (Group*3)
    Number = HundredsGroup(strint[:extra])
    strint = strint[extra:]
    PrevZero = False
    
    for x in range (1, Group + 1):
        #Looping through groups of 3 in the strint
        group = Group + 1 - x
        #number of groups
        if str(group) in LargeGroups:
            if not PrevZero: #Prevents extra words, like thousand in one million thousand
                Number += ' ' + LargeGroups[str(group)]
            Number += ' ' + HundredsGroup(strint[:3])
            if HundredsGroup(strint[:3]) == '':
                PrevZero = True
            else:
                PrevZero = False
            strint = strint[3:]
        else: raise ValueError('Number is bigger that 999999999999999999999999999999')
    return ' '.join(Number.split()) #Gets rid of any extra spaces
_alphabet = {
    'a': 'V',
    'b': 'C',
    'c': 'C',
    'd': 'C',
    'e': 'V',
    'f': 'C',
    'g': 'C',
    'h': 'C',
    'i': 'V',
    'j': 'C',
    'k': 'C',
    'l': 'C',
    'm': 'C',
    'n': 'C',
    'o': 'V',
    'p': 'C',
    'q': 'C',
    'r': 'C',
    's': 'C',
    't': 'C',
    'u': 'V',
    'v': 'C',
    'w': 'C',
    'x': 'C',
    'y': 'Y',
    'z': 'C'
    }
_special = {
    'hundred': 2,
    'ambiguities': 5,
    'ambiguity':5,
    'interest': 2,
    'interested': 3,
    'interests': 2,
    'interesting': 3,
    'nineteen': 2,
    'ninety': 2,
    'nineteens': 2,
    'hundreds':2,
    'nineties': 2
    }
def Syllables(word:str):
    """ Count syllables in word/phrase"""
    alphabet=_alphabet
    special=_special
    
    word = str(word).lower().strip() #makes it more uniform

    try: word = ComposeNumber(int(float(word)))
    except: pass
    if ' ' in word: #If sentence is input, counts syllables for each word in sentence, one at a time.
        words = word.split()
        SyllCount = 0
        for word in words:
            SyllCount += Syllables(word)
        return SyllCount
    
    if word in special: #Some words are wierd.
        return special[word]
    
    Base = "" #Consonants and Vowels
    SyllCount = 1 #Count of syllables
    endings = ["VCCV", "VCV", "VCCCV", "VCCCCV", 'VCY', 'VCCY', 'VCCCY', 'VCCCCY', 'VYV']#Posible reasons to split syllables, Y is sometimes a consonant and sometimes a vowel.
    
    for letter in word:
        #Goes through letters in word, checking if they are
        #consonants or vowels (or a y), counting syllables along the way.
        if letter in alphabet:
        
            Base += alphabet[letter] #Consonant or vowel?
            for ending in endings: #Split into syllables?
                if Base.endswith(ending):
                    Base = "V"
                    SyllCount +=1
                    break
                    
        elif letter == "-": #Compound word stuff, so it counts each word.
            Base = ""
            SyllCount +=1
            
    if not (word[-2:] in ['le', 'he', 'ie', 'ae', 'ee', 'oe', 'ue'] or word[-3:] in ['ses', 'les', 'ies', 'aes', 'oes', 'ues', 'ees', 'eed','aed', 'ied', 'oed', 'ued']): # endings that do make sound even though the word ends in e, es, or ed
        for ending in ['es', 'ed', 'e']: #Usually don't constitute as a syllable
            if word.endswith(ending):
                SyllCount -= 1
                break
    
    if SyllCount == 0:
        SyllCount += 1
    elif word.endswith('lion') or word.endswith('lions'):
        #words that end like this usually divide the li and on, without any
        #consonant.
        SyllCount += 1
    
    return SyllCount


## TODO: colors can be improved severely.
class colors:
	'''Colors class:reset all colors with colors.reset; two subclasses:
fg for foreground and bg for background; use as colors.subclass.colorname. 
i.e. colors.fg.red or colors.bg.green also, the generic bold, disable, 
underline, reverse, strike through, and invisible work with the main class
i.e. colors.bold'''
	reset='\033[0m'
	bold='\033[01m'
	disable='\033[02m'
	underline='\033[04m'
	reverse='\033[07m'
	strikethrough='\033[09m'
	invisible='\033[08m'
	class fg: 
		black='\033[30m'
		red='\033[31m'
		green='\033[32m'
		orange='\033[33m'
		blue='\033[34m'
		purple='\033[35m'
		cyan='\033[36m'
		lightgrey='\033[37m'
		darkgrey='\033[90m'
		lightred='\033[91m'
		lightgreen='\033[92m'
		yellow='\033[93m'
		lightblue='\033[94m'
		pink='\033[95m'
		lightcyan='\033[96m'
	class bg: 
		black='\033[40m'
		red='\033[41m'
		green='\033[42m'    
		orange='\033[43m'
		blue='\033[44m'
		purple='\033[45m'
		cyan='\033[46m'
		lightgrey='\033[47m'

def justify(string, length):
    '''justify a string according to a given length'''
    strings = string.split(' ')
    strlnth = sum([len(s) for s in strings])
    if strlnth+len(strings)-1 >= length:
        return ' '.join(strings)
    required_spaces = length-strlnth
    a, b = divmod(required_spaces, len(strings)-1)
    join = ' '*a
    gap = len(strings)/(b+1)
    current_gap = gap
    runstr = ''
    end = len(strings) -1
    print(gap)
    for c, n in enumerate(strings):
        runstr += n
        if c == end:
            break
        runstr += join
        if c+1 == round(current_gap):
            runstr += ' '
            current_gap += gap
    return runstr    

_allignments = {'center': str.center, 'left': str.ljust, 'right':str.rjust, 'justify': justify}

##TODO: Finish multline object
class multline(object):
    '''multi line string character stuff... in progress'''
    def __init__(self, *strings, format_ = 'center'):
        if len(strings) == 0:
            strings = tuple(strings[0].split('\n'))
        if format_ in _allignments:
            format_=_allignments[format_]
        self.height = len(strings)
        self.width = max([len(str(x)) for x in strings])
        self.strings = tuple([format_(str(x), self.width) for x in strings])

    def __repr__(self):
        return '\n'.join(map(repr, self.strings))

    def __str__(self):
        return '\n'.join(self.strings)

    def getwidth(self):
        return self.width

    def getheight(self):
        return self.height

    def getrow(self, line=0):
        if type(line) is int:
            return multline(self.strings[line])
        elif type(line) is slice:
            lines = self.strings[line]
            return multline(*lines)
        raise TypeError('index must be an integer or slice')

    def getcolumn(self, line=0):
        return multline(*[x[line] for x in self.strings])

    def __getitem__(self, get):
        ##print(get)
        unpack = lambda value, default: value if type(value) is tuple else (value, default)
        if type(get) is tuple:
            if len(get) == 2:
                return self.getcolumn(get[0]).getrow(get[1])
            raise ValueError
        if type(get) is slice:
            if tuple in map(type, (get.start, get.stop, get.step)):
                start1, start2 = unpack(get.start, None)
                stop1, stop2 = unpack(get.stop, None)
                step1, step2 = unpack(get.step, get.step)
                return self.getcolumn(slice(start1, stop1, step1)).getrow(slice(start2, stop2, step2))
        return self.getcolumn(get)
        
    def extend(self, other, center = None):
        if self.__class__ != other.__class__:
            return NotImplemented
        height1 = self.height
        height2 = other.height
        if center == None:
            new = []
            maxheight = max(height1, height2)
            if height1>=height2:
                offset2 = (height1-height2)//2
                offset1 = 0
            else:
                offset1 = (height1-height2)//2
                offset2 = 0
            firsts = self.strings
            seconds = other.strings
            for num in range(maxheight):
                try:
                    if num-offset1<0: raise Exception
                    first = firsts[num-offset1]
                except: first = ' '*self.width
                try:
                    if num-offset2<0: raise Exception
                    second = seconds[num-offset2]
                except: second = ' '*other.width
                new.append(first+second)
            return multline(*new)
        return NotImplemented
        '''
        if __name__ !='__main__': return NotImplemented
        ##print(height1)
        ##print(height2)
        if center not in range(height1): raise ValueError
        def halves(num):
            odd = lambda n: (n%2)!= 0
            if not _validation.is_integer(num): raise TypeError
            num = int(num)
            ##print('half of', num)
            if odd(num): return (num//2, (num//2)+1)
            return (num//2, num//2)
        Halves = halves(height2)
        heightfromcenter = height1-center
        newheightfromcenter = max(heightfromcenter, Halves[1])
        offset1 = 0
        offset2 = 0
        ##print(Halves)
        if center>Halves[0]: offset1=center-Halves[0]
        elif center<Halves[0]: offset2 = Halves[0]-center
        objcenter = max(center, Halves[0])
        newheight = newheightfromcenter+objcenter
        firsts = self.strings
        seconds = other.strings
        new = []
        for num in range(newheight+1):
            ##print('num1:', (num-offset1))
            ##print('num2:', (num-offset2))
            
            try:
                if num-offset1<0: raise Exception
                first = firsts[num-offset1] 
            except: first = ' '*other.width
            try:
                if num-offset2<0: raise Exception
                second = seconds[num-offset2]
            except: second = ' '*self.width
            new.append(first+second)
        return multline(*new)'''

    def __contains__(self, value):
        if type(value) is not self.__class__:
            raise TypeError('other must be a multline class')
        shape = value.shape()
        firstline = value.strings[0]
        matching_starts = []
        for row, rowstr in enumerate(self.strings):
            while firstline in rowstr:
                column = rowstr.index(firstline)
                matching_starts.append((column, row))
                rowstr = rowstr[column+1:]
        for location in matching_starts:
            x, y = location
            nx = x+shape[0]
            ny = y+shape[1]
            if self[x:nx, y:ny] == value:
                return True
        return False

    def index(self, value):
        if type(value) is not self.__class__:
            raise TypeError('other must be a multline class')
        shape = value.shape()
        firstline = value.strings[0]
        matching_starts = []
        for row, rowstr in enumerate(self.strings):
            while firstline in rowstr:
                column = rowstr.index(firstline)
                matching_starts.append((column, row))
                rowstr = rowstr[column+1:]
        for location in matching_starts:
            x, y = location
            nx = x+shape[0]
            ny = y+shape[1]
            if self[x:nx, y:ny] == value:
                return True
        return False

    def shape(self):
        return self.getwidth(), self.getheight()

    def __len__(self):
        return self.getwidth()*self.getheight()

    def __add__(self, other):
        if type(other) is str: other = self.__class__(other)
        return self.extend(other)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.strings)

    def __radd__(self, other):
        if type(other) is str: other = other.__class__(other)
        return other.extend(self)

    def __mul__(self, other):
        n = self.strings
        nn = []
        if type(other) is not int: raise TypeError('Other must be int')
        for l in n:
            nn.append(l*other)
        return multline(*nn)

    def __rmul__(self, other):
        return self*other

#eof
