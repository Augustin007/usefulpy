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

SECTIONS:
validation v1.1.2
 This program contains many useful functions for validation of input and output.
formatting v1.2.2
 This program contains several useful functions for formatting output.
mathematics v1.2.3
 Several mathematical functions plopped together.

'''

__version__ = '1.1.2'

try: import validation, formatting, mathematics
except: from usefulpy import validation, formatting, mathematics

import warnings

def python():
    '''return to python's regular IDLE'''

def IDLE():
    while True:
        try:
            Temporary_Variable_Of_Input = input('>>> ')
            while Temporary_Variable_Of_Input != 'python()':
                doraise = False
                try:
                    if '_' in Temporary_Variable_Of_Input and '_' not in multisplit(Temporary_Variable_Of_Input, '+', '-', '/', '*', '(', ')', '.', '__', '.', whitespacetoo = True):
                        doraise = True
                        _ = fromNumBaseFormat(Temporary_Variable_Of_Input)
                    else:
                        try:
                            _ = eval(Temporary_Variable_Of_Input)
                        except:               
                            _ = trynumber(fromstring(Temporary_Variable_Of_Input))
                    if _ != None:
                        print(repr(_))
                except BaseException as error:
                    if doraise: warnings.warn(error)
                    try: exec(Temporary_Variable_Of_Input)
                    except BaseException as error:
                        warnings.warn(error)
                Temporary_Variable_Of_Input = input('>>> ')
            return
        except BaseException as error:
            warnings.warn(error)

#eof
