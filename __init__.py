'''
usefulmodules
Version: 1.1.1
Author: Austin Garcia

Simple resources and modules for cleaner programming

LICENSE: See license file.

PLATFORMS:
These program import python's built in warnings, functools, math, decimal,
fractions, random, collections and datetime, should work on any python platform
where these are available.

INSTALLATION:
Put the folder where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   This program is started as a collection of smaller programs filled with
   useful functions...
  Version 1.1.2:
   Bugfixes and improvements throughout.
  Version 1.2.1:
     ——  ——
   Addition of more programs that contain more functions. Addition of usefulpy
   IDLE.
   

SECTIONS:
validation v1.1.2
 This program contains many useful functions for validation of input and output.
formatting v1.2.2
 This program contains several useful functions for formatting output.
mathematics v1.2.3
 Several mathematical functions plopped together.

'''

__version__ = '1.1.2'

try: import validation, formatting, mathematics, quickthreads
except: from usefulpy import validation, formatting, mathematics, quickthreads

import warnings

try: from IDLE import IDLE
except: from usefulpy.IDLE import IDLE

if __name__ == '__main__': IDLE()

#eof
