# Contributing

## A note on documentation

Since this is meant to be the kind of code that you can just "dive into" usefulpy has to be well documented.

I'm not the best at this, though, and there is a long way to go. A couple notes on the documentation

### Triple quotes

Triple quotes are only to be used when writing docstrings or long strings, use `#` for multi line commenting

### Comments

Single `#` for comments, These include comments on how something works, what something is, or a mathematical proof!

from 'validation.py'

```python
#for easier reference of the function type.
function = type(lambda: None)
```

Double `##` for markers that mark something that needs to be done. Additional stuff like `BUG`, `TODO`, or `FIXME` may be there as well.
This is also used for deactivating statements that were only there for the purposes of debuging

from (an older version of) 'quaternion.py'

```python
##TODO: I need to get log/ln for these first...
raise NotImplementedError('Raising quaternions to non-real powers has not been implemented yet')
```

Triple `###` on each side of the name of a segment of code; these serve to partition the code into several parts. Search for the `###` to find the headers of these sections.

from '\_\_init\_\_.py' for usefulpy

```python
### IMPORTS ###
from . import validation, formatting, mathematics, quickthreads, decorators
from .IDE import ide, run_path, startup
```

## Versionieering

We use [semantic versioning](https://semver.org/)

Versions are formatted as x.y.z, or MAJOR.MINOR.PATCH.

In summary:

An update to z (a patch) means refers to small changes, fixed bugs, improved performance, _et cetera_.

An update to y (a minor update) refers to larger changes that include adding functions or changing their jobs. This type of change is not backward compatible so something that is supposed to be possible in the new version was not possible in the version before. But something that used to work still works

An update to x (a major update) refers to an update that is not forward compatible so something that used to work no longer works.

## What to do

You've opened a branch to contribute, but don't know what to do? I've got a lot to do... here is some of it.

### Plans

There already some stuff planned out, some visible from the placeholders. More 3d projection ability would be nice, but I haven't worked out exactly what to do. For the sake of efficiency I would like would be to move some stuff over to some form of compiled code, and I am trying to learn how to combine those. I am continuously sifting through and improving the code to better the quality.

## Bugs

Bug reporting helps alot, I accidentally broke the three-dimensional projection system and didn't realize for a few months.

Bugs are reported [here](https://github.com/Augustin007/usefulpy/issues).
