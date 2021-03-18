'''
This program creates what is called a langton ant
The default settings have it grouped by 1 and a
simple 'rl' termite
rllr
'''

from turtle import Turtle, tracer, update
import time
import turtle
from random import choice
from usefulpy.validation import is_integer, intinput

def matrix(dim = [], fill = 'white'):
    dimensions, prev = len(dim), fill
    if dimensions == 0: return fill
    for x in dim:
        nprev = []
        for n in range(x):
            if type(prev) == type([]): nprev.append(prev.copy())
            else: nprev.append(prev)
        prev = nprev.copy()
    return prev

def turn(t, tn, deg):
    if tn in ('r', 'rt', 'right'): t.rt(deg)
    elif tn in ('l', 'lt', 'left'): t.lt(deg)
    else: raise BaseException

def langton(ant, group, info, fdrate):
    grid, count = matrix([turtle.window_height()//fdrate, turtle.window_width()//fdrate], info['start']), 0
    ant.hideturtle(); tracer(False)
    while True:
        if count == group-1: update(); time.sleep(0.25); count = 0
        else: count += 1
        xpos, ypos = int(ant.xcor()), int(ant.ycor())
        if xpos%fdrate != 0:
            xadj = xpos%fdrate
            if xadj < (fdrate//2): xpos = xpos-xadj
            else: xpos = xpos+(fdrate-xadj)
            ant.goto(xpos, ypos)
        if ypos%fdrate != 0:
            yadj = ypos%fdrate
            if yadj < (fdrate//2): ypos = ypos-yadj
            else: ypos = ypos+(fdrate-yadj)
            ant.goto(xpos, ypos)
        try: pos = grid[xpos//fdrate][ypos//fdrate]; ncolor, tn = info[pos]
        except: return
        grid[xpos//fdrate][ypos//fdrate] = ncolor; ant.color(ncolor); ant.stamp(); turn(ant, tn, 90); ant.fd(fdrate)

group, fdrate = 1, 11
info = {'white': ['black', 'r'], 'black': ['white', 'l'], 'start': 'white'}
sampleinfo = {'start': 'red', 'red':['white', 'r'], 'white': ['brown', 'r'], 'brown': ['black', 'r'], 'black': ['red', 'l']}

def prep(fdrate):
    t = Turtle(); t.up(); turtle.bgcolor('grey'); t.shape("square"); t.shapesize((fdrate-1)/20, (fdrate-1)/20)
    return t

def fromstr(strinfo):
    if strinfo == '': return {'white': ['black', 'r'], 'black': ['white', 'l'], 'start': 'white'}
    elif strinfo == 'sample': return sampleinfo
    colors, colorlist = ['yellow', 'gold', 'orange', 'red', 'maroon', 'violet', 'magenta', 'purple', 'navy', 'blue', 'skyblue', 'cyan', 'turquoise', 'lightgreen', 'green', 'darkgreen', 'chocolate', 'brown', 'black', 'white'], []
    start = choice(colors)
    prev, newinfo, endcount, count = start, {'start': start}, len(strinfo), 1
    colorlist.append(prev)
    for letter in strinfo:
        if count < endcount:
            newcolor = choice(colors)
            colors.remove(newcolor)
            colorlist.append(newcolor); newinfo[prev] = [newcolor, letter]; prev = newcolor; count += 1
        else: newinfo[prev] = [start, letter]
    return newinfo

def settings():
    global group, info, fdrate
    group = intinput('Input speed (default = 1: number of moves made per 0.25 seconds): '); fdrate = intinput('Input size (default = 10: smaller sizes may cause errors): ')+1; strinfo = input('Type in a series of "r"s and "l"s\nrepresenting turns\ntype sample for "rrrl"\nMaximum = 23, type nothing for default: ').lower()
    while (strinfo != 'sample') and (strinfo.replace('r', '').replace('l', '')!='' or len(strinfo)>21): strinfo = input('Invalid input, try again: ').lower()
    info = fromstr(strinfo)

def main():
    x = input('Input nothing to start\nInput "settings" to change settings\n')
    if x == 'settings': settings()
    elif x != '': return
    ant = prep(fdrate)
    langton(ant, group, info, fdrate)

if __name__ == '__main__':main()
