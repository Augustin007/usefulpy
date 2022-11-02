'''
mathfunc

DESCRIPTION
This file implements a cas system that works with a series of new types and the use of wrappers
around standard and custom math functions.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Merging of eq, mathfunc, and Expression classes into one class in one file.
  Version 0.0.1:
   bugfixes
 0.1
  Version 0.1.0:
   Improved useability, ability to calculate derivatives.
   Recursiveness battled
   more versatility
   trig func and inverse trig func decorators
   functions moved here
  Version 0.1.1:
   Small bugfixes. Changing small internal bits.
   Documentation
1
 1.0
  Version 1.0.0:
   Reimplemented CAS system, removed expression_check, now supports multiple
   variables using the cas_variable class.
   __all__ added.
  1.1
   Version 1.1.0:
    Adds hooks and new features to CAS
   Version 1.1.1:
    Bugfixes and more thorough documentation.
'''


if __name__ == '__main__':  # To account for relative imports when run directly
    __package__ = 'usefulpy.mathematics'

# SETUP FOR TESTING #
import logging

if __name__ == '__main__':
    print('Debug: 10', 'Info: 20', 'Warn: 30', 'Error: 40', 'Critical: 50', sep='\n')
    level = input('enter logging level: ')
    if level == '':
        level = '30'
    while not level.isnumeric():
        level = input('Invalid\nenter logging level: ')
        if level == '':
            level = '30'
    lvl = int(level)
    fmt = '[%(levelname)s] %(name)s - %(message)s'
    logging.basicConfig(format=fmt, level=lvl)

# IMPORTS #
# Relative imports
from .. import validation
from .. import decorators
# Utilities
from abc import abstractmethod
import types
import typing
from functools import wraps
from contextlib import suppress
from collections import OrderedDict
# Maths
import math
import cmath
from decimal import Decimal
from fractions import Fraction
from numbers import Number

class CAS(type):
    variables: dict = {}
    implicit: dict = {}
    functions: dict = {}
    identities: dict = {}
    system: tuple = ()

    def __class_getitem__(self, *args):
        if len(args)==0:
            return CAS()

        return CAS([CAS.parse_arg(arg) for arg in args])
    
    @staticmethod
    def parse_arg(arg):
        if type(arg) is not slice:
            return CASexpression(arg)
        match arg:
            case slice(start=None, stop=None, step=z):
                return CAScondition.create(z)
            case slice(start=None, stop=y, step=z):
                return CASset.create(x, parameters=y)
            case slice(start=x, stop=None, step=z):
                return CASexpression.create(x, parameters=z)
            case slice(start=x, stop=y, step=z):
                return CASequation.create(x, y, parameters=z)

class CASobject(CAS):
    pass

class arithmetic(CASobject):
    pass

class CASequation(CASobject):
    pass

class CASinequality(CASobject):
    pass

class CASexpression(arithmetic):
    pass

class CASset(CASobject):
    pass

class CASmatrix(CASobject):
    pass

class CAScondition(CASobject):
    pass

class CASfunction(CASobject):
    pass
