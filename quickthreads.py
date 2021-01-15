from _thread import *
from threading import *
import time

def _raise(error):
    raise error

def raise_separately(error):
    nthread = Thread(target=_raise, args=(error))
    nthread.start()

def run_in_thread(func, *args, **kwargs):
    #creates a thread... there are less args
    #this way it is easier to put in the arguments
    #so you can quickly run a function in a thread
    #it also auto-starts the function... not always desirable
    #but shortens
    nthread = Thread(target=func, args=args, kwargs=kwargs)
    nthread.start()
