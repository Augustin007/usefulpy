'''
usefulpy

Simple resources and modules for cleaner programming

LICENSE: See license file.

PLATFORMS:
These program import python's built in warnings, functools, math, decimal,
fractions, random, collections and datetime, should work on any python platform
where these are available.

INSTALLATION:
pip install usefulpython

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   This program is started as a collection of smaller programs filled with
   useful functions...
  Version 0.0.1:
   Bugfixes and improvements throughout.
 0.1
  Version 0.1.0:
   Addition of more programs that contain more functions. Addition of
   usefulpy IDE. Improvement of functions.
  Version 0.1.1:
   Restructured to be supported as a package
  Version 0.1.2:
   A couple bugfixes
  Version 0.1.3:
   Fixed error in folder structure.
  Version 0.1.4:
   More bugfixes!
  Version 0.1.5:
   Succesfully restructured to be a package. Also bugfixes.
 0.2
  Version 0.2.0:
   Mathfunc class capabilities expanded with a simple algebraic simplifier
   system. Math sections improved for faster and better capabilities.
   Newer, faster prime sieve.

SECTIONS:
validation
This program contains many useful functions for validation of input and output.
formatting
This program contains several useful functions for formatting output.
mathematics
Several mathematical functions plopped together.
gui
Functions to help create a gui
decorators
A small group of decorators
IDE
Usefulpy IDE and interpreter

'''

# INFO #
__author__ = 'Austin Garcia'
__version__ = '0.2.0'
if __name__ != '__main__':
    __package__ = 'usefulpy'
__all__ = ('validation', 'formatting', 'mathematics', 'decorators')

# IMPORT #
from . import validation, formatting, mathematics, decorators
from .IDE import ide

if __name__ == '__main__':
    ide()
