'''
usefulpy
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
gui
decorators
IDLE

'''

##Not ready for 1.2.1

### INFO ###
__author__ = 'Austin Garcia'
__version__ = '1.1.2'
__package__ = 'usefulpy'

### IMPORT ###
from . import validation, formatting, mathematics, quickthreads, decorators
from .IDE import ide, run_path, startup

if __name__ == '__main__': ide()

### TO DO ###
# BEFORE ANY UPDATE:
# Check docstrings, 
#
# BEFORE UPDATE 1.2.1:
# Any tag 'PREREQUISITE1.2.1:' or 'PREREQUISITE1.2:'
# Update code tagged with '##UPDATEME' for usefulpy 1.2.1
# 
# OTHER:
# Finish any code tagged with '##UNFINISHED' by the
# prerequisite time
# 
# Any tag with TODO, FIXME, or BUG
#
#
# FUTURE PLANS:
# a 'typecast' object/function that moves a variable/operation to c++

### CURRENTLY WORKING ON ###
# Usefulpy IDLE 2.1.1

### UPDATE FORMAT ###
# x.y.z
# There is no 0, updates start at 1
# (so no 1.0.0, but 1.1.1)
#
# An update to z means refers to small changes, fixed bugs
# Improved performance, etc.
#
# An update to y refers to larger changes that include adding functions
# or changing their jobs
#
# An update to z refers to the entire code rewritten on a new file.

### BUGS ###
#

#eof
