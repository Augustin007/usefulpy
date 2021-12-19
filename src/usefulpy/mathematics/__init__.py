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
 0.2
  Version 0.2.0
   Heavy bugfixing throughout. Deprecated algebraic solver and eq
  Version 0.2.1
   More bugfixing, some more functions. Efficiency increased
1
 1.0
  Version 1.0.0
   Entirety of folder restructured. Much improved use of mathfuncs. Expression
   check has taken the place of eq and algebraic solver. Basic CAS implemented
   for the new mathfunc-eq-solver merge. Greater efficiency and power to most
   other areas. nmath made much smaller, most of its functionality has been
   moved to the mathfunc file.
'''

# INFO #
__version__ = '1.0.0'
__author__ = 'Augustin Garcia'
if __name__ == '__main__':
    __package__ = 'usefulpy.mathematics'

# IMPORTS #
from math import comb, copysign, erf, erfc, fabs, fmod, fsum, gamma, lgamma
from math import modf, nextafter, perm, remainder, trunc, ulp, ldexp, frexp
from .constants import *
from .mathfuncs import *
from .nmath import *
from .basenum import *
from .quaternion import *
from .vector import *
from .intervals import *

# eof
