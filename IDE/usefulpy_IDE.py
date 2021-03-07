'''
IDE

Custom ide for usefulpy.
This IDE allows you to access previous inputs and outputs easily.
This IDE also gives access to entire usefulpy library.

Most important functions:
   ide: start ide

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   Custom ide for usefulpy.

'''

__version__ = '1.1.1'
__author__ = 'Austin Garcia'
__package__ = 'usefulpy.IDE'

import usefulpy.IDE.usefulpy_syntax as usefulpy_syntax
from usefulpy.quickthreads import raise_separately
import time
def _output(object, count):
    if object is None: return
    print(f'Out[{count}] : ', repr(object), sep = '')
    print()

def _input(count):
    input_ = input(f'In [{count}] : ').rstrip()
    while not input_:
        print()
        input_ = input(f'In [{count}] : ').rstrip()
    if input_.endswith(':'):
        empty = ' '*(len(str(count))+3)+'-- : '
        next_line = input(empty).rstrip()
        while next_line:
            input_+= '\n'+next_line
            next_line = input(empty).rstrip()
    return input_
    

def _quit():
    ide.quit = True

def ide(namespace = None):
    ide.quit = False
    if namespace is None: namespace = {}
    namespace = {**namespace, **usefulpy_syntax.namespace_management.usefulpy_namespace_globals}
    original = namespace.copy()
    In = []
    Out = {}
    addedOuts = {}
    if 'In' not in namespace: namespace['In'] = In
    if 'Out' not in namespace: namespace['Out'] = Out
    namespace['quit'] = _quit
    count = 0
    while not ide.quit:
        try:
            input_ = _input(count)
            
            corrected_input = usefulpy_syntax._usefulpy_correct_syntax(input_, namespace['__defaults__']['#a'])
            try:
                try:
                    old_1 = namespace['_']
                    old__1 = namespace['__']
                except: pass

                output = eval(corrected_input, namespace)
                print()
                if output is None: count += 1; In.append(input_); continue
                _output(output, count)
                Out[count] = output
                namespace[f'_{count}'] = output
                addedOuts[f'_{count}'] = output
                try:
                    namespace['_'] = output
                    namespace['__'] = old_1
                    namespace['___'] = old__1
                except: pass
            except:
                try:
                    exec(corrected_input, namespace)
                    print()
                except BaseException as err:
                    print()
                    print(err) ##raise seperately later
                    Out[count] = err
                    namespace[f'_{count}'] = err
                    addedOuts[f'_{count}'] = err
                    print()
            In.append(input_)
            count += 1
        except:
            print('...')
            print('Internal Error Occured:')
            print('...')
            print()
    usefulpy_syntax.namespace_management.keep_unique(namespace, original)
    usefulpy_syntax.namespace_management.keep_unique(namespace, addedOuts)
    try:
        del namespace['_']
        del namespace['__']
        del namespace['___']
    except: pass
    del namespace['In']
    del namespace['Out']
    del namespace['quit']
    return namespace

ide.quit = False

if __name__ == '__main__':
    ide()
