'''
Scope and namespace management

Contains several objects to be used as variable scopes and tools to
manipulate them.


LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Doesn't do much yet, mostly placeholder and driver for usefulpy-ide
   purposes
'''

# DUNDERS #
__version__ = '0.0.0'
__author__ = 'Augustin Garcia'

blank_namespace_globals = globals().copy()

del blank_namespace_globals['__name__']
del blank_namespace_globals['__doc__']
del blank_namespace_globals['__loader__']
del blank_namespace_globals['__file__']
blank_namespace_globals['__defaults__'] = {'#': int, '.': float, '#a': tuple()}

built_in_namespace = {'globals': globals}
exec('print(end = \'\')', built_in_namespace)

usefulpy_namespace_globals = built_in_namespace.copy()
exec('from ..mathematics import *',
     usefulpy_namespace_globals, usefulpy_namespace_globals)
exec('from ..validation import *',
     usefulpy_namespace_globals, usefulpy_namespace_globals)
exec('from ..formatting import *',
     usefulpy_namespace_globals, usefulpy_namespace_globals)

del usefulpy_namespace_globals['blank_namespace_globals']
del usefulpy_namespace_globals['__name__']
del usefulpy_namespace_globals['__doc__']
del usefulpy_namespace_globals['__loader__']
del usefulpy_namespace_globals['__file__']
del usefulpy_namespace_globals['built_in_namespace']
usefulpy_namespace_globals['__defaults__'] = {'#': int, '.': float,
                                              '#a': ('i', 'j', 'k')}


def reset_scope(scope, save, except_=None):
    if except_ is None:
        except_ = []

    for value in scope.copy():
        if value in except_:
            continue
        if value not in save:
            del scope[value]
        if value in save:
            scope[value] = save[value]


def set_scope(scope, new):
    scope.clear()
    for name, value in new.items():
        scope[name] = value


reset_scope(globals(), blank_namespace_globals,
            ['blank_namespace_globals', 'usefulpy_namespace_globals',
            'reset_scope', 'set_scope', 'built_in_namespace'])


def new_locals_dict():
    return dict()


def keep_unique(in_, from_):
    for n in in_.copy():
        if n not in from_:
            continue
        if in_[n] is not from_[n]:
            continue
        del in_[n]
