'''
IDE

Customized IDE and interpreter, this ide lets you change default types. 
This IDE allows you to access previous inputs and outputs easily.
This IDE also gives access to entire usefulpy library.

Most important functions:
   ide: start ide
   quit: while in ide, quits ide
   run_code: run a code file
   startup: run a code file and start the ide with the code's variables.


LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
Pre releases:
 pr 1
 ——Wednesday the thirteenth of the firstmonth Janurary, 2021——
  Run IDLE() to use Usefulpy's personal IDLE
1
 1.1
  Version 1.1.1:
   Custom ide and interpreter for usefulpy.

'''
__version__ = '1.1.1'
__author__ = 'Austin Garcia'
__package__ = 'usefulpy.IDE'

from .run_code import run_path
from .usefulpy_IDE import ide

def startup(with_, init_globals = None, run_name= '__umain__', usefulpy = True, launch_with =run_path, environment = ide):
    environment(launch_with(with_, init_globals, run_name, usefulpy))
