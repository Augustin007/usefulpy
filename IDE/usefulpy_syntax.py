__package__ = 'usefulpy.IDE'

import usefulpy.IDE.namespace_management as namespace_management
from .partitions import _partition_triple_quote, _partition_single_quote, _partition_comments
from usefulpy import formatting as _formatting, validation as _validation

splitter = '\\1r3f2g4\\'
trnsltdct = {}
for n in ('+', '-', '*', '/', '(', ')', ',', '[', ']', '{', '}', '}', ':', ';', '=', ' ', '\n', '\t'): trnsltdct[n] = splitter+n+splitter

def _partition_delegator(lscource):
    if len(lscource) <= 1:return tuple(lscource)
    new = []
    for n in lscource:
        new.extend(_partition_fix(n))
    return tuple(new)

def _partition_fix(scource):
    if len(scource) == 0: return (scource,)
    if scource.startswith('#'):
        if '\n' not in scource:
            return (scource, )
    if '"""' in scource or "'''" in scource: return _partition_delegator(_partition_triple_quote(scource))
    elif '"' in scource or "'" in scource: return _partition_delegator(_partition_single_quote(scource))
    # I need to make a '_partition_comments'
    elif '#' in scource: return _partition_delegator(_partition_comments(scource))
    tmp = _formatting.translate(scource, trnsltdct)
    ltmp = _formatting.scour(tmp.split(splitter))
    nstr = ''
    for var in ltmp:
        if _validation.is_integer(var[0]):
            if _validation.is_integer(var):
                nstr += '__defaults__[\'#\']('+var+')'
                continue
            if _validation.is_float(var):
                nstr += '__defaults__[\'.\']('+var+')'
                continue
            nstr += _formatting.translate(var, _partition_fix.key)
            continue
        nstr += var
    return (nstr,)

def _usefulpy_correct_syntax(scource, keys = ['i', 'j', 'k']):
    key = {}
    for k in keys: key[k] = '*'+k
    _partition_fix.key = key
    return ''.join(_partition_fix(scource))
