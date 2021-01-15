from usefulpy.mathematics import *
from usefulpy.validation import *
from usefulpy.formatting import *
from usefulpy.quickthreads import *
#import threading
#import time

#eventually will catch other stuff.

_hold = object()
def _usefulpy_correct_syntax(scource):
    if '"""' in scource or "'''" in scource: #Not Implimented
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
    tmp = translate(scource, {'+':'\\+\\', '-':'\\-\\', '/':'\\/\\',
                              '*':'\\*\\', '(':'\\(\\', ')':'\\)\\'})
    ltmp = multisplit(tmp, '\\', whitespacetoo = True)
    qdict = {}
    for num, var in enumerate(ltmp):
        if is_integer(var[0]):
            string = var
            string = string.replace('i', '*i')
            string = string.replace('+*i', '+i')
            string = string.replace('/*i', '/i')
            string = string.replace('**i', '*i')
            string = string.replace('-*i', '-i')
            string = string.replace('j', '*j')
            string = string.replace('+*j', '+j')
            string = string.replace('/*j', '/j')
            string = string.replace('**j', '*j')
            string = string.replace('-*j', '-j')
            string = string.replace('k', '*k')
            string = string.replace('+*k', '+k')
            string = string.replace('/*k', '/k')
            string = string.replace('**k', '*k')
            string = string.replace('-*k', '-k')
            qdict[var] = string
    return translate(scource, qdict)

def _output(object, outnum):
    if object is None: return
    print(f'Out[{outnum}]: ', repr(object), sep = '')


def IDLE():
    '''An IDLE for '''
    In = []
    count_9b134ijhqrg8 = 0
    Out = {}
    while True:
        try:
            #long strings of random characters to prevent accidental overwriting 
            tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
            while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
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
                        tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
                        while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
                        continue
                    _output(output1223efresv423, count_9b134ijhqrg8)
                    Out[count_9b134ijhqrg8] = output1223efresv423
                    try:
                        _ = output1223efresv423
                        __ = old_n_138f23rfw3
                        ___ = old__n_138f23rfw3
                    except: pass
                except BaseException as error:
                    try: exec(correctedtext10932jf20h)
                    except BaseException as error:
                        raise_separately(error)
                        time.sleep(1)
                count_9b134ijhqrg8+=1
                tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
                while not tmpvarofinp_039eifojv1u39fnb: tmpvarofinp_039eifojv1u39fnb = input(f'In [{count_9b134ijhqrg8}]: ').rstrip()
            del tmpvarofinp_039eifojv1u39fnb, _, __, ___, old_n_138f23rfw3
            del old__n_138f23rfw3, count_9b134ijhqrg8, In, Out, correctedtext10932jf20h
            return locals()
        except BaseException as error:
            raise_separately(error)
            time.sleep(1)

if __name__ == '__main__':
    IDLElocalvariables_120324jw3hngv = IDLE()
    for localvariablename_1093jf32, localvariablevalue_1039jf10fnbc in IDLElocalvariables_120324jw3hngv.items():
        exec(f'{localvariablename_1093jf32} = localvariablevalue_1039jf10fnbc')
    del IDLElocalvariables_120324jw3hngv
