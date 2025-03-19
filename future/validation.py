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
  Version 0.1.0:
    ——Friday, the fifteenth day of the firstmonth Janurary, 2021——
   Code is shorter by about fifty lines, and yet its functionality has
   increased... Simplicity is better! Who knew?
  Version 0.1.1:
   Small bugfixes
  Version 0.1.2:
   Code cleanup.
  Version 0.1.3:
   Bugfixes, conforming to PEP
'''

if __name__ == '__main__':
    __package__ = 'usefulpy'
__author__ = 'Austin Garcia'
__version__ = '0.2.0'

from collections import abc

import types
import typing
import datetime

_chastise = '\nYour input was invalid, please try again.\n'

#Just for easy reference to the function type.
function = type(lambda:None)

def validate(obj, annotation):
    if isinstance(annotation, type):
        return isinstance(obj, annotation)
    if isinstance(annotation, types.GenericAlias):
        origin = annotation.__origin__
        args = annotation.__args__
    return True

def is_function(s):
    '''Check whether variable s points to a function, not the same as callable'''
    return type(s) is function


def is_integer(s):
    '''Check if an object is an integer or can be turned into an integer without
losing any value'''
    try:
        return int(float(s)) == float(s)
    except Exception:
        return False

