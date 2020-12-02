'''
usefulpy
Version: 1.1.1
Author: Austin Garcia

Simple resources and modules for cleaner programming

LICENSE: See license file.

PLATFORMS:
These program import python's built in warnings, functools, math, statistics
random, collections and datetime, should work on any python platform where
these are available.

INSTALLATION:
Put the folder where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   This program is started as a collection of smaller programs filled with
   useful functions...
   validation.py v1.1.2
    This program contains many useful functions for validation of input and
    output.
   formatting.py v1.2.2
    This program contains several useful functions for formatting output.
   mathematics.py v1.1.3
    Several mathematical functions plopped together.

'''

try: import validation
except: import useful.validation as validation
try: import formatting
except: import useful.formatting as formatting
try: import mathematics
except: import useful.mathematics as mathematics
