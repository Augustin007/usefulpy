'''
Code partitioning

partitions the code into code and non-code sections, but allows
for modification of code sections

Most important functions:
   _partition_fix: partitions code and fixes code sections
   _usefulpy_correct_syntax: modifies full code

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file.

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Slicing... some bugs occur when quotes occur in comments, or comments
   in quotes. Uses __defaults__... might be improvable?
'''

__version__ = '0.0.0'
__author__ = 'Augustin Garcia'

from .partitions import _partition_triple_quote, _partition_single_quote
from .partitions import _partition_comments
from .. import formatting as _formatting, validation as _validation

splitter = '\\1r3f2g4\\'
trnsltdct = {}
splitting_iter = ('+', '-', '*', '/', '(', ')', ',', '[', ']', '{', '}', '}',
                  ':', ';', '=', ' ', '\n', '\t')
for n in splitting_iter:
    trnsltdct[n] = splitter+n+splitter


def _partition_delegator(lscource):
    if len(lscource) <= 1:
        return tuple(lscource)
    new = []
    for n in lscource:
        new.extend(_partition_fix(n))
    return tuple(new)


def _partition_fix(scource):
    if len(scource) == 0:
        return (scource,)
    if scource.startswith('#'):
        if '\n' not in scource:
            return (scource, )
    if '"""' in scource or "'''" in scource:
        return _partition_delegator(_partition_triple_quote(scource))
    elif '"' in scource or "'" in scource:
        return _partition_delegator(_partition_single_quote(scource))
    # I need to make a '_partition_comments'
    elif '#' in scource:
        return _partition_delegator(_partition_comments(scource))
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


def _usefulpy_correct_syntax(scource, keys=['i', 'j', 'k']):
    key = {}
    for k in keys:
        key[k] = '*'+k
    _partition_fix.key = key
    return ''.join(_partition_fix(scource))
