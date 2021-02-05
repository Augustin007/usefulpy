import functools
import time
import random

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
    return decorator_repeat

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
