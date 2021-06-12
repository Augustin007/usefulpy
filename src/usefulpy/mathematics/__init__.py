'''
usefulpy mathematics

Several mathematical functions plopped together.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   mathematics.py contains many mathematical functions.
  Version 0.0.1:
   An updated description and various bug fixes. Cleaner looking code with more
   comments.
  Version 0.0.2:
   Some small bug fixes
   Raises warnings at unfinished sections
 0.1
  Version 0.1.0
   Separated into sections and placed into a folder of its own
  Version 0.1.1
   Mostly some small bugfixes and clearer commenting throughout
  Version 0.1.2
   Several bugfixes, some work on algebraic solver and improvements on eq
  Version 0.1.3
   Heavy improvements in nmath, small bugfixes throughout
  Version 0.1.4
   Small improvement throughout.

SECTIONS:
PrimeComposite
 Several functions to do with gcd, lcf, and numbers being prime or composite.
nmath
 This file is essentially the importation of the math module, but a few small
 functions are added or changed
triangles
 Several functions to do with triangles
basenum
 A basenum class, can hold numbers in a any counting system
eq
 This program stores the 'eq' class. It takes a string of an expression of a
 function and returns an 'eq' object, which can be called with a number which
 replaces the variable with a number.
algebraicsolvers
 Algebraic expressions/algebraic simplification
quaternion
 a quaternion class
'''

##UPDATED TO: Usefulpy 1.2.1

### INFO ###
__version__ = '0.1.4'
__author__ = 'Augustin Garcia'
__package__ = 'usefulpy.mathematics'

### IMPORTS ###
from .basenum import *
from .nmath import *
from .PrimeComposite import *
from .quaternion import *
from .triangles import *

#eof
