'''
Code partitioning

Run code with usefulpy-syntax

Most important functions:
   run_path: usefulpy equilavent of runpy.run_path

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Runs code with usefulpy-syntax.
   bug: changes to __defaults__['#a'] cause bugs

'''

__version__ = '0.0.0'
__author__ = 'Augustin Garcia'

from . import usefulpy_syntax
import os

uglobals = usefulpy_syntax.namespace_management.usefulpy_namespace_globals
rglobals = usefulpy_syntax.namespace_management.blank_namespace_globals
bglobals = usefulpy_syntax.namespace_management.built_in_namespace


def _get_code(filename, defaults):
    file = open(filename)
    code = file.read()
    doc = None
    trydoc = usefulpy_syntax._partition_triple_quote(code.strip())[0]
    if trydoc.startswith('"""') or trydoc.startswith("'''"):
        doc = eval(trydoc)
    file.close()
    code = usefulpy_syntax._usefulpy_correct_syntax(code, defaults['#a'])
    return (code, doc)


def _get_doc(filename):
    file = open(filename)
    code = file.read()
    file.close()
    trydoc = usefulpy_syntax._partition_triple_quote(code.strip())[0]
    if trydoc.startswith('"""') or trydoc.startswith("'''"):
        return eval(trydoc)


def run_path(pathname, init_globals=None, run_name='__umain__', usefulpy=True):
    if init_globals is None:
        init_globals = {}

    if usefulpy:
        globals = {**uglobals.copy(), **init_globals}
    else:
        globals = {**rglobals.copy(), **bglobals, **init_globals}

    code, doc = _get_code(pathname, globals['__defaults__'])

    run_scope = globals.copy()

    run_scope['__file__'] = os.path.realpath(pathname)
    run_scope['__name__'] = run_name
    run_scope['__doc__'] = doc

    exec(code, run_scope)
    usefulpy_syntax.namespace_management.keep_unique(run_scope, globals)
    return run_scope
