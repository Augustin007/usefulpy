from distutils.core import setup
from distutils.sysconfig import get_python_lib

setup(
    name = 'usefulmodules',
    version = '1.0.0',
    description = 'Simple resources and modules for a cleaner looking program',
    author = 'Augustin Garcia',
    author_email = 'albusdumbledore101123@gmail.com',
    py_modules = ['validation', 'mathematics']
    )
