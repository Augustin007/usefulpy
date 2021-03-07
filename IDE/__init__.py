__package__ = 'usefulpy.IDE'

from .run_code import run_path
from .usefulpy_IDE import ide

def startup(with_, init_globals = None, run_name= '__umain__', usefulpy = True, launch_with =run_path, environment = ide):
    environment(launch_with(with_, init_globals, run_name, usefulpy))
