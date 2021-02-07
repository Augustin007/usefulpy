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

def timer(func):
    '''Print the runtime of the decorated function'''
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Finished {func.__name__!r} in {run_time:.4f} secs')
        return value
    return wrapper_timer

@io_opt
def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

@io_opt
def timed_repeat(num_times, timing):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
                time.sleep(timing)
            return value
        return wrapper_repeat
    return decorator_repeat


# Sample Dictionary: {2:(0, 1), 1:((10,), 0)}
@io_opt
def shift_args(dict_):
    ''' Decorator for a function

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
    def deccorator_shift_args(func):
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
    return deccorator_shift_args

@io_opt
def pipeline(b):
    class _pipeline(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b
        @functools.wraps(b)
        def __call__(self, *args, **kwargs):
            return self.a(self.b(*args, **kwargs))
        def __str__(self):
            try: a = self.a.__name__
            except:
                try: a = str(self.a)
                except:
                    a = repr(self.a)
            try: b = self.b.__name__
            except:
                try: b = str(self.b)
                except:
                    b = repr(self.b)
            return a+'———'+b
        def __repr__(self):
            return f'Pipeline[{str(self)}]'
    def pipe_dec(a): return _pipeline(a, b)
    return pipe_dec

@io_opt
def default_setter(func):
    def wrapper_func(arg):
        @functools.wraps(func)
        def nfunc(*args, **kwargs):
            nfunc.__doc__ = func.__doc__.replace('\\FIRSTARG', str(arg))
            return func(arg, *args, **kwargs)
        return nfunc
    wrapper_func.__doc__ = f'Makes a {func.__name__} function with arg\nas a default first argument'
    wrapper_func.__name__ = func.__name__
    return wrapper_func

@io_opt # minimize exact returns
def default_with_decorator(*decorators, check = None):
    def default_setter(func):
        @io_opt #io_opt minimizes duplicate functions in this case
        def wrapper_func(arg):
            if check:
                if not check(arg):
                    raise ValueError(f'{arg} is an inapropriate value for {func.__name__}')
            @functools.wraps(func)
            def nfunc(*args, **kwargs):
                return func(arg, *args, **kwargs)
            nfunc.__doc__ = func.__doc__.replace('\\FIRSTARG', str(arg))
            try: nfunc.__call__.__func__.__doc__ = func.__doc__.replace('\\FIRSTARG', str(arg))
            except: pass
            for decorator in decorators:
                nfunc = decorator(nfunc)
            return nfunc
        wrapper_func.__doc__ = f'Makes a {func.__name__} function with arg\nas a default first argument'
        wrapper_func.__name__ = func.__name__
        
        return wrapper_func
    return default_setter

def arg_simplifier(simplify)
    def wrapper_creator(func):
        def wrapper_simplifier(*args, **kwargs):
            args = [simplify(a) for a  in args]
            for a, b in kwargs.items():
                new_kwarg = simplify(b)
                if new_kwarg != b: kwargs[a] = b
            return func(*new_args, **new_kwargs)
        return wrapper_simplifier
    return wrapper_creator

def io_opt(func):
    '''Minimizes duplicate functions returned from a function'''
    func_store = {}
    @functools.wraps(func)
    def nfunc(*args, **kwargs):
        input = str((args, kwargs))
        if input in func_store: return func_store[input]
        output = func(*args, **kwargs)
        func_store[input] = output
        return output
    return nfunc
