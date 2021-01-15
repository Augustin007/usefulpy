from random import *

def lowbias(low, high):
    '''return a random integer from low to high, lower numbers have higher
weights'''
    return randint(low, randint(low, randint(low, high)))

def highbias(low, high):
    '''return a random integer from low to high, higher numbers have higher
weights'''
    return randint(randint(randint(low, high), high), high)

def centerbias(low, high):
    '''return a random integer from low to high, center numbers have higher
weights'''
    return randint(randint(low, high//2), randint(high//2, high))

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
    return randint(1, 100) <= chance

def falsebias(chance = 75):
    '''return a random boolean value, biased to False, or a chance% to return
False'''
    return randint(1, 100) >= chance
