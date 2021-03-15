import _thread as thread
from threading import Thread
import threading
import time
import warnings

##TODO: Document code
##PREREQUISITE1.2.2: quickthreads 1.1.1

def _raise(error):
    raise error

def raise_separately(error):
    nthread = Thread(target=_raise, args=(error,))
    nthread.start()

def run_in_thread(func, *args, **kwargs):
    #creates a thread... there are less args
    #this way it is easier to put in the arguments
    #so you can quickly run a function in a thread
    #it also auto-starts the function... not always desirable
    #but shortens
    nthread = Thread(target=func, args=args, kwargs=kwargs)
    nthread.start()
