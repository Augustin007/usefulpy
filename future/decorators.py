import logging
import sys

if __name__ == '__main__':
    if len(sys.argv)>=2:
        fmt = '[%(levelname)s] %(name)s - %(message)s'
        logging.basicConfig(format=fmt, level=int(sys.argv[1]))

import traceback
from abc import ABC, abstractmethod
from functools import wraps
from inspect import signature
import typing
import types
import functools
import random

UnionTypes = types.UnionType, typing.Union

def FunctionWrapper(n):
    @wraps(n)
    def internal(obj, *args, **kwargs):
        new = n(obj, *args, **kwargs)
        return wraps(new.func)(n.__call__).__get__(new)
    return internal

class _FunctionWrapper(ABC):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.on_init()

    def on_init(self):
        pass

    @abstractmethod
    def __pre_call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __post_call__(self, result):
        pass

    def __call__(self, *args, **kwargs):
        try:
            self.__pre_call__(*args, **kwargs)
            result = self.func(*args, **kwargs)
            self.__post_call__(result)
            return result
        except Exception:
            t, v, tb = sys.exc_info()
            sys.excepthook(t, v, tb.tb_next)
        sys.exit()


@FunctionWrapper
class _log(_FunctionWrapper):
    def on_init(self):
        self.func._logger = self
        self.logger = self.args[0]
    level = 0

    def __pre_call__(self, *args, **kwargs):
        if self.level>0:
            logging.log(self.logger, f'{self.level}: - {self.func} called with arguments {args!r} and keywords {kwargs!r}')
            #TODO:change the logger?
        self.level+=1

    def __post_call__(self, result):
        self.level -= 1
        if self.level>0:
            logging.log(self.logger, f'{self.level}: - {self.func} returned {result!r}')
            #TODO:change the logger?

def logged(x: types.FunctionType | int):
    if isinstance(x, int):
        return lambda y: _log(y, x)
    return _log(x, logged.default)
logged.default = logging.DEBUG

def _hint(instance, hint):
    if hint == typing.Any:
        return True
    if isinstance(hint, type):
        return isinstance(instance, hint)
    if hasattr(hint, '__origin__') and hasattr(hint, '__args__'):
        if hint.__origin__ in UnionTypes:
            return any(map(lambda a: _hint(instance, a), hint.__args__))
        if not isinstance(hint, types.GenericAlias):
            hint = types.GenericAlias(hint.__origin__, hint.__args__)
        if isinstance(instance, hint.__origin__):
            if ... not in hint.__args__:
                if len(hint.__args__)!=len(instance):
                    return False
                for element, arg in zip(instance, hint.__args__):
                    if not _hint(element, arg):
                        return False
                return True
            # ind = 0
            # prev = None
            #for arg in hint.__args__:
            #    return False
            #prev = arg
    return False


@FunctionWrapper
class typed(_FunctionWrapper):
    def on_init(self):
        self.annotations = self.func.__annotations__
        self.signature = signature(self.func)
        for param in self.signature.parameters:
            assert param in self.annotations, f'Missing annotations for {param!r}'
        assert 'return' in self.annotations, f'Missing annotation for return'
        self.retanot = self.annotations['return']
    
    def __pre_call__(self, *args, **kwargs):
        bound = self.signature.bind(*args, **kwargs)
        bound.apply_defaults()
        annotations = self.annotations
        try:
            for name, value in bound.arguments.items():
                if not _hint(value, annotations[name]):
                    raise TypeError(f'Argument {name} must be of type {annotations[name]}')
            return
        except TypeError:
            t, v, tb = sys.exc_info()
            sys.excepthook(t, v, tb.tb_next)
        sys.exit()

    def __post_call__(self, result):
        try:
            if not _hint(result, self.retanot):
                raise TypeError(f'Return value should be a type {self.retanot}')
            return
        except TypeError:
            t, v, tb = sys.exc_info()
            sys.excepthook(t, v, tb.tb_next)
        sys.exit()

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


#attribute.log
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
