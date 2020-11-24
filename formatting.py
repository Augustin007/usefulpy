'''useful formatting functions'''
vowels = 'aeiou'
endingpuncuation = '.?!'
phrasepuncuation = ',–—()"\';:'
inwordpunctuation = '-_'

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


#Temporary
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
    if witha not in endingpuncuation: raise ValueError
    n.strip(endingpuncuation)
    n += witha
    return n

def translate(self, translator):
    '''Translate all items in treanslator'''
    for old, new in translator.items(): self=self.replace(old, new)
    return self

def scour(self, of= ''):
    if type(self) is str:
        if type(of) is str: return self.replace(of, '')
        for key in of: self=self.replace(key, '')
        return self
    if type(self) is list:
        if type(of) is str:
            count = 0
            for c in self.copy():
                if c == of: self.pop(count)
                else: count += 1
            return self
        for c in self.copy():
            if c in of: self.pop(count)
            else: count += 1
        return self

#NOT FINISHED, in progress

class multline(object):
    '''multi line string character stuff... in progress'''
    def __init__(self, *strings):
        self.height = len(strings)
        lens = [len(str(x)) for x in strings]
        self.width = max(lens)
        self.strings = [str(x).center(self.width) for x in strings]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join(self.strings)

    def getwidth(self):
        return self.width

    def getheight(self):
        return self.height

    def getrow(self, line=0):
        return self.strings[line]

    def getcolumn(self, line=0):
        return '/n'.join([x[line] for x in self.strings])

    def extend(self, other, center = None):
        if center == None: center = self.height//2
        print(center)
        height1 = self.height
        height2 = other.height
        print(height1)
        print(height2)
        if center not in range(height1): raise ValueError
        def halves(num):
            def odd(num): return num%2 != 0
            if not validation.is_integer(num): raise ValueError
            num = int(num)
            print('half of', num)
            if odd(num): return (num//2, (num//2)+1)
            return (num//2, num//2)
        Halves = halves(height2)
        heightfromcenter = height1-center
        newheightfromcenter = max(heightfromcenter, Halves[1])
        offset1 = 0
        offset2 = 0
        print(Halves)
        if center>Halves[0]: offset1=center-Halves[0]
        elif center<Halves[0]: offset2 = Halves[0]-center
        objcenter = max(center, Halves[0])
        newheight = newheightfromcenter+objcenter
        firsts = self.strings
        seconds = other.strings
        new = []
        for num in range(newheight+1):
            print('num1:', (num-offset1))
            print('num2:', (num-offset2))
            
            try:
                if num-offset1<0: raise Exception
                first = firsts[num-offset1] 
            except: first = ' '*other.width
            try:
                if num-offset2<0: raise Exception
                second = seconds[num-offset2]
            except: second = ' '*self.width
            new.append(first+second)
        return multline(*new)

    def __add__(self, other):
        if type(other) is str: other = self.__class__(other)
        return self.extend(other)

    def __radd__(other, self):
        if type(self) is str: self = other.__class__(self)
        return self.extend(other)
