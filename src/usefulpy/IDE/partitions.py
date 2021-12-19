'''
Code partitioning

partitions the code into code and non-code sections.

Most important functions:
   _partition_triple_quotes: slices away triple_quote sections
   _partition_single_quotes: partitions away single quote sections
   _partition_comments: partitions away comment sections


LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Slicing... some bugs occur when quotes occur in comments, or comments
   in quotes.

'''

__version__ = '0.0.0'
__author__ = 'Augustin Garcia'


def _move(string, fornum):
    list = [string]
    for n in range(1, fornum+1):
        list.append((' '*n)+(string[:-n]))
    return zip(*list)


def _partition_triple_quote(scource):
    inchar = ''
    instr = False
    eschar = False
    runstr = ''
    lscource = []
    for char, prev1, prev2 in _move(scource, 2):
        if not instr:
            if char in ('"', "'"):
                if prev1 != char:
                    runstr += char
                    continue
                if prev2 != char:
                    runstr += char
                    continue
                inchar, instr = char, True
                runstr = (runstr[:-2])
                if runstr:
                    lscource.append(runstr)
                runstr = char*3
                continue
            runstr += char
            continue
        runstr += char
        if (char == inchar) and (not eschar):
            if prev1 != char:
                if not eschar:
                    eschar = (prev2 == '\\')
                else:
                    eschar = False
                continue
            if prev2 != char:
                if not eschar:
                    eschar = (prev2 == '\\')
                else:
                    eschar = False
                continue
            inchar = ''
            instr = False
            eschar = False
            lscource.append(runstr)
            runstr = ''
            continue
        if not eschar:
            eschar = (prev2 == '\\')
        else:
            eschar = False
    if runstr:
        lscource.append(runstr)
    return tuple(lscource)


def _partition_single_quote(scource):
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
    if runstr:
        lscource.append(runstr)
    return tuple(lscource)


def _partition_comments(scource):
    lscource = scource.splitlines(True)
    lscource1 = []
    for n in lscource:
        if '#' in n:
            nm = n.index('#')
            lscource1.extend((n[:nm], n[nm:-1], n[-1]))  # catches the \n
            continue
        lscource1.append(n)
    return lscource1
