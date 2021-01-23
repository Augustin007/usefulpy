'''
File: IDLE.py
Version: 1.1.1
Author: Austin Garcia

A IDLE for Usefulpy.

LICENSE:
This is a section of usefulpy. See usefulpy's lisence.md file.

PLATFORMS:
This is a section of usefulpy. See usefulpy.__init__'s "PLATFORMS" section.

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
     ——Wednesday the thirteenth of the firstmonth Janurary, 2021——
   Run IDLE() to use Usefulpy's personal IDLE
'''



##UPDATED TO: Usefulpy 1.2.1

__version__ = '1.1.1'
__author__ = 'Austin Garcia'

from runpy import run_path as run
from usefulpy.mathematics import *
from usefulpy.validation import *
from usefulpy.formatting import *
from usefulpy.quickthreads import *

##_hold = object()
def _usefulpy_correct_syntax(scource):
    if '"""' in scource or "'''" in scource:
        inchar = ''
        instr = False
        eschar = False
        runstr = ''
        lscource = []
        prev1 = ''
        prev2 = ''
        for char in scource:
            if not instr:
                if char in ('"', "'"):
                    if prev1 != char: continue
                    if prev2 != char: continue
                    inchar = char
                    instr = True
                    if runstr:
                        lscource.append(runstr)
                    runstr = char
                    continue
                runstr += char
                continue
            runstr += char
            if (char == inchar) and (not eschar):
                if prev1 != char: continue
                if prev2 != char: continue
                inchar = ''
                instr = False
                eschar = False
                lscource.append(runstr)
                runstr = ''
                continue
            eschar = (prev2 == '\\')
        if runstr: lscource.append(runstr)
        return scource if len(lscource) == 1 else ''.join(map(_usefulpy_correct_syntax, lscource))
    if '"' in scource or "'" in scource:
        inchar = ''
        instr = False
        eschar = False
        runstr = ''
        lscource = []
        for char in scource:
            if not instr:
                if char in ('"', "'"):
                    inchar = char
                    instr = True
                    if runstr:
                        lscource.append(runstr)
                    runstr = char
                    continue
                runstr += char
                continue
            runstr += char
            if (char == inchar) and (not eschar):
                inchar = ''
                instr = False
                eschar = False
                lscource.append(runstr)
                runstr = ''
                continue
            eschar = (char == '\\')
        if runstr: lscource.append(runstr)
        return scource if len(lscource) == 1 else ''.join(map(_usefulpy_correct_syntax, lscource))
    if ',' in scource:
        nscource = translate(scource, {'{':'\\{\\', '[':'\\[\\', '(':'\\(\\', '}':'\\}\\', ']':'\\]\\', ')':'\\)\\', ',':'\\,\\'})
        separated = multisplit(nscource, '\\')
        nstr = ''
        for n in separated:
            if n in ('{', '[', '(', '}', ']', ')', ','):
                nstr += n
                continue
            nstr += _usefulpy_correct_syntax(n)
        return nstr
    tmp = translate(scource, {'+':'\\+\\', '-':'\\-\\', '/':'\\/\\',
                              '*':'\\*\\', '(':'\\(\\', ')':'\\)\\',
                              '{':'\\{\\', ')':'\\}\\',
                              '[':'\\[\\', ')':'\\]\\'})
    ltmp = multisplit(tmp, '\\', whitespacetoo = True)
    qdict = {}
    for var in ltmp:
        if is_integer(var[0]):
            #TODO: multireplace translator from formatting
            string = var
            string = translate(string, {'i':'*i', 'j':'*j', 'k':'*k'})
            qdict[var] = string
    new = translate(scource, qdict)
    if '/0' in new:
        tmp = translate(scource, {'+':'\\+\\', '-':'\\-\\',
                                  '*':'\\*\\', '(':'\\(\\', ')':'\\)\\',
                                  '{':'\\{\\', ')':'\\}\\',
                                  '[':'\\[\\', ')':'\\]\\'})
        ltmp = multisplit(tmp, '\\', whitespacetoo = True)
        qdict = {}
        for n in ltmp:
            if '/0' in n:
                qdict[n] = 'nan'
        new = translate(scource, qdict)
    return new
        

def _output(object, outnum):
    if object is None: return
    print(f'Out[{outnum}]: ', repr(object), sep = '')


def IDLE():
    '''An IDLE for usefulpy. Return a dictionary containing all variables
created during the IDLE (without including internal workings)

Based on ipython...
A list named In stores all previous inputs.
A dictionary named Out stores all previous outputs.
_ refers to previous output
__ refers to output two previous
___ refers to output three previous
naming a variable In or Out may cause Errors
'''
    
    
    In = []
    count_9b134ijhqrg8 = 0
    Out = {}
    while True:
        try:
            #long strings of random characters to prevent accidental overwriting 
            tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
            while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'\nIn [{count_9b134ijhqrg8}]: ').rstrip()
            while tmpvarofinp_039eifojv1u39fnb != 'quit()':
                if tmpvarofinp_039eifojv1u39fnb.endswith(':'):
                    tmpholdervarofobj_012984t099w0vfher8=tmpvarofinp_039eifojv1u39fnb
                    line23_r9j2q0iqenv = ' '*(len(str(count_9b134ijhqrg8))+3)+'--: '
                    tmpvarofinp_039eifojv1u39fnb = input(line23_r9j2q0iqenv)
                    while tmpvarofinp_039eifojv1u39fnb:
                        tmpholdervarofobj_012984t099w0vfher8 += '\n'+tmpvarofinp_039eifojv1u39fnb
                        tmpvarofinp_039eifojv1u39fnb = input(line23_r9j2q0iqenv).rstrip()
                    tmpvarofinp_039eifojv1u39fnb = tmpholdervarofobj_012984t099w0vfher8
                In.append(tmpvarofinp_039eifojv1u39fnb)
                correctedtext10932jf20h = _usefulpy_correct_syntax(tmpvarofinp_039eifojv1u39fnb)

                try:
                    try:
                        old_n_138f23rfw3 = _
                        old__n_138f23rfw3 = __
                    except: pass
                    
                    output1223efresv423 = eval(correctedtext10932jf20h)

                    if output1223efresv423 == None:
                        count_9b134ijhqrg8+=1
                        tmpvarofinp_039eifojv1u39fnb = input(f'\nIn [{count_9b134ijhqrg8}]: ').rstrip()
                        while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'\nIn [{count_9b134ijhqrg8}]: ').rstrip()
                        continue
                    _output(output1223efresv423, count_9b134ijhqrg8)
                    Out[count_9b134ijhqrg8] = output1223efresv423
                    try:
                        _ = output1223efresv423
                        __ = old_n_138f23rfw3
                        ___ = old__n_138f23rfw3
                    except: pass
                except BaseException as error:
                    #print(error)
                    try: exec(correctedtext10932jf20h)
                    except BaseException as error:
                        raise_separately(error)
                        time.sleep(1)
                count_9b134ijhqrg8+=1
                tmpvarofinp_039eifojv1u39fnb = input(f'\nIn [{count_9b134ijhqrg8}]: ').rstrip()
                while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'\nIn [{count_9b134ijhqrg8}]: ').rstrip()
            del In, Out, tmpvarofinp_039eifojv1u39fnb, count_9b134ijhqrg8
            try: del correctedtext10932jf20h, output1223efresv423
            except: pass
            try: del _
            except: pass
            try: del __, old_n_138f23rfw3
            except: pass
            try: del ___, old__n_138f23rfw3
            except: pass
            return locals()
        except BaseException as error:
            raise_separately(error)
            time.sleep(1)

if __name__ == '__main__':
    IDLElocalvariables_120324jw3hngv = IDLE()
    for localvariablename_1093jf32, localvariablevalue_1039jf10fnbc in IDLElocalvariables_120324jw3hngv.items():
        exec(f'{localvariablename_1093jf32} = localvariablevalue_1039jf10fnbc')
    del IDLElocalvariables_120324jw3hngv

#eof
