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

if __name__ == '__main__':
    __package__ = 'usefulpy'
__version__ = '0.0.1'
__author__ = 'Augustin Garcia'
__all__ = ('debug', 'repeat', 'timed_repeat', 'shift_args', 'default_setter',
           'default_with_decorator', 'arg_modifier')

import functools
import time
import random


def debug(func):
    '''Print the function signature and return value'''
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f'{k}={v!r}' for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f'Calling {func.__name__}({signature})')
        value = func(*args, **kwargs)
        print(f'{func.__name__!r} returned {value!r}')
        return value
    return wrapper_debug


@functools.cache
def repeat(n):
    '''Make a function repeat 'n' times'''
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat


@functools.cache
def timed_repeat(n, t):
    '''Make a function repeat 'n' times, with a 't' time in the interval
between a return and a call'''
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
def shift_args(dict_):
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


def _getstr(fn, *args):
    '''Generates a string representation for pipeline'''
    if len(args) != 0:
        args = list(args)
        args[0:1] = [fn, args[0]]
        return tuple([_getstr(a) for a in args])
    if type(fn) is str:
        return fn
    if hasattr(fn, '__name__'):
        return fn.__name__
    if hasattr(fn, '__str__'):
        return str(fn)
    return repr(fn)


@functools.cache
def pipeline(b):
    class _pipeline(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        @functools.wraps(b)
        def __call__(self, *args, **kwargs):
            return self.a(self.b(*args, **kwargs))

        def __str__(self):
            a, b = _getstr(self.a, self.b)
            return a+'———'+b

        def __repr__(self):
            return f'<Pipeline[{str(self)}] at {hex(id(self))}>'

    def pipe_dec(a): return _pipeline(a, b)

    return pipe_dec


@functools.cache
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


@functools.cache  # minimize exact returns
def default_with_decorator(*decorators, check=None):
    '''Make a function with a forced first argument.
     Apply decorators to the returning function function
     Check that the first argument is valid'''
    def default_setter(func):
        @functools.cache  # minimizes duplicate functions in this case
        def wrapper_func(arg):
            if check:
                if not check(arg):
                    raise ValueError(f'{arg} is an inapropriate value\
 for {func.__name__}')

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


def arg_modifier(modify):
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
