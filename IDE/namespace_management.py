blank_namespace_globals = globals().copy()

del blank_namespace_globals['__name__']
del blank_namespace_globals['__doc__']
del blank_namespace_globals['__loader__']
del blank_namespace_globals['__file__']
blank_namespace_globals['__defaults__'] = {'#':int, '.':float, '#a': tuple()}


built_in_namespace = {}
exec('print(end = \'\')', built_in_namespace)

from usefulpy.mathematics import *
from usefulpy.validation import *
from usefulpy.formatting import *

usefulpy_namespace_globals = {**built_in_namespace, **globals().copy()}

del usefulpy_namespace_globals['blank_namespace_globals']
del usefulpy_namespace_globals['__name__']
del usefulpy_namespace_globals['__doc__']
del usefulpy_namespace_globals['__loader__']
del usefulpy_namespace_globals['__file__']
del usefulpy_namespace_globals['built_in_namespace']
usefulpy_namespace_globals['__defaults__'] = {'#':int, '.':float, '#a': ('i', 'j', 'k')}

def reset_scope(scope, save, except_ = None):
    if except_ is None: except_ = []

    for value in scope.copy():
        if value in except_: continue
        if value not in save: del scope[value]
        if value in save: scope[value] = save[value]

def set_scope(scope, new):
    scope.clear()
    for name, value in new.items():
        scope[name] = value

reset_scope(globals(), blank_namespace_globals, ['blank_namespace_globals', 'usefulpy_namespace_globals', 'reset_scope', 'set_scope', 'built_in_namespace'])

def new_locals_dict():
    return dict()

def keep_unique(in_, from_):
    for n in in_.copy():
        if n not in from_: continue
        if in_[n] is not from_[n]: continue
        del in_[n]
