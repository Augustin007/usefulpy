'''
decorators

This program is meant to contain decorators for a better python experience

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Decorators.py contains a few decorators
  Version 0.0.1:
   Maybe I should have looked through the functools module better
'''
## Prepping U.D0.1.0 for U0.3.0

if __name__ == '__main__':
    __package__ = 'usefulpy'
__version__ = '0.0.1'
__author__ = 'Augustin Garcia'
# __all__ = ('debug', 'repeat', 'timed_repeat', 'shift_args', 'default_setter',
#           'default_with_decorator', 'arg_modifier')

import functools
import time
import random
import logging
import types

def _logCallSub(level: int, function: types.FunctionType) -> types.FunctionType:
    '''_logCallSub _summary_

    Parameters
    ----------
    level : int
        _description_
    function : types.FunctionType
        _description_

    Returns
    -------
    types.FunctionType
        _description_
    '''    
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logging.log(level, f'{function.__name__} called with args {args} and kwargs {kwargs}')
        return function(*args, **kwargs)
    wrapper.logged = True
    return wrapper


# This was written this way for backward compatability.
# Intended functionality outlined in documentation summary.
def logCall(x: types.FunctionType | int) -> types.FunctionType:
    '''For logging calls and call signatures.
    @logCall(logging.DEBUG)
    def foo(bar):
        ...

    Parameters
    ----------
    x : types.FunctionType | int
        Level of logging or function to log

    Returns
    -------
    types.FunctionType
        Returns a decorator that wraps a function at a custom logging level or a function logged at level debug.
    '''    
    if type(x) is int:
        return lambda y: _logCallSub(x, y)
    else:
        return _logCallSub(logging.DEBUG, x)


# Haven't used this in ages, but then, who has?
def repeat(n: int) -> types.FunctionType:
    '''Make a function repeat n times.

    Parameters
    ----------
    n : int
        Number of times to repeat.

    Returns
    -------
    types.FunctionType
        Function wrapper for a repeating function
    '''
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat


def timed_repeat(n: int, t: float) -> types.FunctionType:
    '''Make a function repeat 'n' times, with a 't' time in the interval
between a return and a call

    Parameters
    ----------
    n : int
        Number of times to repeat
    t : float
        Time between repeats

    Returns
    -------
    types.FunctionType
        Function wrapper for repeating function
    '''
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n):
                value = func(*args, **kwargs)
                time.sleep(t)
            return value
        return wrapper_repeat
    return decorator_repeat


# Sample Dictionary: {2:(0, 1), 1:((10,), 0)}
def shift_args(dict_:dict) -> types.FunctionType:
    ''' Custom input-output for a function.

example:
@shift_args({2:(0, 1), 1:((10,), 0)})
def log(base, x):
    \'''log(x) -> log(10, x)\'''
    print(f'log base {base} of {x}')

>>> log(2)
log base 10 of 2
>>> log(1)
log base 10 of 1
>>> log(1, 2)
log base 1 of 2
'''
    # validation
    assert type(dict_) is dict
    for x, y in dict_.items():
        assert type(x) is int
        assert x >= 0
        assert type(y) is tuple
        for z in y:
            assert type(z) in (int, tuple)
            if type(z) is int:
                assert z < x
                assert z >= 0

    def decorator_shift_args(func):
        @functools.wraps(func)
        def wrapper_shift_args(*args, **kwargs):
            if kwargs:
                return func(*args, **kwargs)
            elif len(args) in dict_:
                tuple_ = dict_[len(args)]
                nargs = []
                for value in tuple_:
                    if type(value) is tuple:
                        nargs.append(random.choice(value))
                    elif type(value) is int:
                        nargs.append(args[value])
                return func(*nargs)
            return func(*args, **kwargs)
        return wrapper_shift_args
    return decorator_shift_args


#attribute.log(math.e))
class librarian:
    def __call__(self, name, strict=True, call=False):
        if call:
            def lookup(x):
                if strict:
                    y = getattr(x, name)
                else:
                    y = getattr(x, name) if hasattr(x, name) else x
                if callable(y):
                    try:
                        return y()
                    except TypeError:
                        pass
                return y
            return lookup
        if strict:
            return lambda x: getattr(x, name)
        return lambda x: getattr(x, name) if hasattr(x, name) else x

    def __getattr__(self, name):
        return self(name)

attribute = librarian()


def func_zip(*functions, raise_flag_exclusive=(Exception,), raise_flag_inclusive=(), final_exception=Exception()):
    '''Combine various functions into a single function'''
    @functools.wraps(functions[0])
    def wrapper(*args, **kwargs):
        for function in functions:
            flagged = False
            try:
                return function(*args, **kwargs)
            except BaseException as error:
                pasterror = error
                if not isinstance(error, raise_flag_exclusive):
                    flagged = True
                elif isinstance(error, raise_flag_inclusive):
                    flagged = True
            if flagged:
                raise pasterror
        raise final_exception
    return wrapper


def default_setter(func):
    '''Make a function with a forced first argument'''
    def wrapper_func(arg):
        @functools.wraps(func)
        def nfunc(*args, **kwargs):
            nfunc.__doc__ = func.__doc__.replace(
                '\\FIRSTARG', str(arg))
            return func(arg, *args, **kwargs)
        return nfunc
    wrapper_func.__doc__ = f'Makes a {func.__name__} function\
 with arg\nas a default first argument'
    wrapper_func.__name__ = func.__name__
    return wrapper_func


@functools.cache 
def default_with_decorator(*decorators, check=None):
    '''Make a function with a forced first argument.
     Apply decorators to the returning function function
     Check that the first argument is valid'''
    def default_setter(func):
        @functools.cache
        def wrapper_func(arg):
            if check:
                if not check(arg):
                    raise ValueError(f'{arg} is an inapropriate value for {func.__name__}')

            @functools.wraps(func)
            def nfunc(*args, **kwargs):
                return func(arg, *args, **kwargs)
            nfunc.__doc__ = func.__doc__.replace('\\FIRSTARG', str(arg))
            try:
                nfunc.__call__.__func__.__doc__ = func.__doc__.replace(
                    '\\FIRSTARG', str(arg))
            except Exception:
                pass
            for decorator in decorators:
                nfunc = decorator(nfunc)
            return nfunc
        wrapper_func.__doc__ = f'Makes a {func.__name__} function\
 with arg\nas a default first argument'
        wrapper_func.__name__ = func.__name__

        return wrapper_func
    return default_setter


def arg_modifier(modify: types.FunctionType) -> types.FunctionType:
    '''modify args according to modify function'''
    def wrapper_creator(func):
        @functools.wraps(func)
        def wrapper_modifier(*args, **kwargs):
            args = [modify(a) for a in args]
            for a, b in kwargs.items():
                new_kwarg = modify(b)
                if new_kwarg != b:
                    kwargs[a] = b
            return func(*args, **kwargs)
        return wrapper_modifier
    return wrapper_creator

# eof
