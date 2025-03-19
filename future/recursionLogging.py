# Import the necessary modules
import logging
import functools
import sys

# If no arguments are provided, ask the user to enter a logging level
if len(sys.argv)==1:
    # Print out the log levels
    print('Debug:10', 'Info: 20', 'Warn: 30', 'Error:40', 'Critical:50', sep='\n')
    level = input('enter logging level: ')
    # If user input is empty, set default logging level to '30' (WARN)
    if level == '':
        level = '30'
    # If the user doesn't enter a numeric value, ask them to enter the level again
    while not level.isnumeric():
        level = input ('Invalid\nenter logging level: ')
        if level == '':
            level = '30'
    # Convert the level to an integer
    lvl = int(level)
    # Define the log format
    fmt = '[%(levelname)s] %(name)s - %(message)s'
    # Configure the logging system with the provided level and format
    logging.basicConfig(format=fmt, level=lvl)
    # Delete temporary variables
    del lvl, fmt, level
else:  # If command-line arguments are provided, use the first argument as the logging level
    fmt = '[%(levelname)s] %(name)s - %(message)s'
    logging.basicConfig(format=fmt, level=int(sys.argv[1]))

# Function to add a string for each recursion level
def _recursion():
    return ' | '*_debug.recursion

# Function to add an arrow at the end of the string from _recursion
def _recursion_msg():
    return _recursion() + ' -> '

# Function decorator that logs before and after calling a function
def _debug(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Log the function call if the recursion level is greater than or equal to 0
        if _debug.recursion >= 0:
            logging.debug(_recursion()+f'{f} called with args {args} and kwargs {kwargs}')
        # Increase the recursion level
        _debug.recursion += 1
        
        try:
            # Call the function and save the return value
            Value = f(*args, **kwargs)
        except Exception as e:
            # Adjust the traceback to skip this frame (i.e., the wrapper frame)
            tb = sys.exc_info()[2]
            if _debug.recursion >= 0:
                logging.info(_recursion()+f'{e.__class__.__name__}: {e}')
            raise e.with_traceback(tb.tb_next)
        finally:
            # Decrease the recursion level
            _debug.recursion -= 1

        # Log the function's return if the recursion level is greater than or equal to 0
        if _debug.recursion >= 0:
            logging.debug(_recursion()+f'{f} returned {Value}')
        # Return the function's return value
        return Value
    return wrapper


# Set the recursion level to the second command-line argument if it exists, else set it to 0
if len(sys.argv) == 3:
    _debug.recursion = int(sys.argv[2])
else:
    _debug.recursion = 0

# Remove the used command-line arguments
sys.argv = sys.argv[0:1]+sys.argv[3:]


class _debugClass(type):
    def __new__(self, name, bases, namespace, **kwargs):
        for name, func in namespace.items():
            if callable(func):
                namespace[name] = _debug(func)
        return type.__new__(self, name, bases, namespace, **kwargs)
