'''
usefulpy mathematics

Several mathematical functions plopped together.

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   mathematics.py contains many mathematical functions.
  Version 1.1.2:
   An updated description and various bug fixes. Cleaner looking code with more
   comments.
  Version 1.1.3:
   Some small bug fixes
   Raises warnings at unfinished sections
 1.2
  Version 1.2.1
   Separated into sections and placed into a folder of its own
  Version 1.2.2
   Mostly some small bugfixes and clearer commenting throughout
  Version 1.2.3
   Several bugfixes, some work on algebraic solver and improvements on eq
  Version 1.2.4
   Heavy improvements in nmath, small bugfixes throughout
  Version 1.2.5
   Small improvement throughout.

SECTIONS:
PrimeComposite v1.1.1
 Several functions to do with gcd, lcf, and numbers being prime or composite.
nmath v1.1.2
 This file is essentially the importation of the math module, but a few small
 functions are added or changed
triangles v1.1.2
 Several functions to do with triangles
basenum v1.1.1
 A basenum class, can hold numbers in a any counting system
eq v2.1.5
 This program stores the 'eq' class. It takes a string of an expression of a
 function and returns an 'eq' object, which can be called with a number which
 replaces the variable with a number.
algebraicsolvers pr 5 (1.1.1)
 Algebraic expressions/algebraic simplification
quaternion v1.2.2
 a quaternion class
'''

##UPDATED TO: Usefulpy 1.2.1

### INFO ###
__version__ = '1.2.5'
__author__ = 'Austin Garcia'
__package__ = 'usefulpy.mathematics'

### IMPORTS ###
from .basenum import *
from .nmath import *
from .PrimeComposite import *
from .quaternion import *
from .triangles import *

#eof
