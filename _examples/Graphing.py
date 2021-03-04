'''
File: Graphing.py
Version: 2.1.1
Author: Austin Garcia

Graphing calculator for python

This is where my eq class was originally created

PLATFORMS:
Should run on a python platform where my usefulpy is available

INSTALLATION:
Put this file where Python can see it.

RELEASE NOTES:
1
 1.1
  1.1.1
   Version 1.1.1-20w01a
    System for processing an equation from a list and graphing it on a
    turtle canvas is set up
   Version 1.1.1-20w02a
    System is embeded into a tkinter system, grid is set up
   Version 1.1.1
    System is updated to include 'clear', is capable of processing text to
    generate lists.
 1.2
  1.2.1
   Version 1.2.1-20w03b
    Version adds the neq class, which recreated the original graphing system
    with an easier ways to access and process the data
   Version 1.2.1
    Added support for constant numbers π, τ, e, Φ,φ,ρ,σ, ς, κ, and ψ.
    improved generation in neq class and order of operations.
    Added inline support for greek letters
  1.2.2
   Version 1.2.2-20w04c
    Several bug fixes, improved efficiency.
   Version 1.2.2
    More bug fixes... increased efficiency.
2
 2.1
  2.1.1
   Version 2.1.1-20w05d
    Modified for use with Usefulpy
'''

__version__ = '2.1.1-20w05d'

###  Part 1  ###
### Graphics ###
from tkinter import *
import turtle
from turtle import Turtle, tracer
from usefulpy.gui import strField

###  Part 2  ###
###   Data   ###
from usefulpy.validation import tryint, is_float
from usefulpy.formatting import translate, greek_letters
replacements = greek_letters
replacements['lσ']='ς'
replacements['Uψlon']='Υ'
replacements['Eψlon']='Ε'
replacements[' ']=''
replacements['eψlon']='ε'
replacements['uψlon']='υ'


from threading import Thread
import time

###  Part 3  ###
###   Math   ###
from usefulpy.mathematics import *

def makegraph(t):
    tracer(False)
    jump = 1
    win = 400//(scale*jump)
    def scaledown(jump):
        if jump >= 1:
            if str(jump).startswith('1'):
                return jump/2
            if str(jump).startswith('5'):
                return 2*jump/5
            if str(jump).startswith('2'):
                return jump/2
        else:
            if str(jump).endswith('1'):
                return jump/2
            if str(jump).endswith('5'):
                return 2*jump/5
            if str(jump).endswith('2'):
                return jump/2
    def scaleup(jump):
        if jump >= 1:
            if str(jump).startswith('1'):
                return 2*jump
            if str(jump).startswith('5'):
                return 2*jump
            if str(jump).startswith('2'):
                return 5*jump/2
        else:
            if str(jump).endswith('1'):
                return 2*jump
            if str(jump).endswith('5'):
                return 2*jump
            if str(jump).endswith('2'):
                return 5*jump/2
    while win < 5:
        jump = scaledown(jump)
        win = 400//(scale*jump)
    while win > 15:
        jump = scaleup(jump)
        win = 400//(scale*jump)
    win = int(win)
    notch = (scale*jump)//5
    def makeaxis(t, negative = False):
        if negative:
            for x in range(int(win)):
                x = round((-1-x)*jump, 15)
                t.fd(scale*jump)
                t.rt(90)
                t.fd(notch)
                t.write(str(tryint(x)))
                t.bk(2*notch)
                t.fd(notch)
                t.lt(90)
        else:
            for x in range(int(win)):
                x = round((1+x)*jump, 15)
                t.fd(scale*jump)
                t.lt(90)
                t.fd(notch)
                t.write(tryint(x))
                t.bk(2*notch)
                t.fd(notch)
                t.rt(90)
    t.penup()
    t.goto(0,0)
    t.pendown()
    for x in range(4):
        makeaxis(t, {'1':False, '2': True, '3': True, '4': False}[str(x+1)])
        t.penup()
        t.goto(0, 0)
        t.pendown()
        t.rt(90)
    tracer(True)

def graph(t, neq):
    tracer(False)
    t.penup()
    t.goto(-400, t.pos()[1])
    frozen = True
    started = False
    for x in range(-400, 400):
        try:
            newheight = round(scale*neq.solve(x/scale), 15)
            t.goto(x, newheight)
            if frozen:
                t.pendown()
                frozen = False
                if not started:
                    started = True
        except:
            t.penup()
            t.goto(x, 0)
            if not frozen:
                frozen = True
    tracer(True)
    if not started:
        raise ValueError

class replacer(Thread):
    def __init__(self, field):
        Thread.__init__(self, name = 'Replace_in_'+str(field))
        self.field = field
    def run(self):
        while True:
            try:
                old = self.field.get()
                if '"' in old:
                    nindex = old.index('"')
                    new = translate(old[:nindex], replacements)+old[nindex:]
                else:
                    new = translate(old, replacements)
                if old != new:
                    self.field.set(new)
                time.sleep(0.001)
            except: break

class NewWindow(object):
    def __init__(self):
        self.root = turtle._root = Tk()
        self.fields = {}
        pane = PanedWindow(orient=VERTICAL, sashwidth=1,
                           sashrelief=SOLID, bg='#ddd')
        pane.add(self.addButton(pane, 'calculate', command = self.calculate))
        pane.add(self.addTextField(pane, 'input'))
        pane.add(self.makeGraphFrame(pane))
        pane.add(self.addButton(pane, 'clear', command = self.refreshCanvas))
        pane.add(self.addTextField(pane, 'scale', str(scale)))
        pane.add(self.addButton(pane, 'refresh scale', command = self.refreshscale))
        pane.add(self.addButton(pane, 'restart', command = main))
        pane.grid(row=0, columnspan=4, sticky='news')
        self.dirty = False
        self.t = Turtle()
        self.t.hideturtle()
        self.g = Turtle()
        self.g.hideturtle()
        self.nscale = self.fields['scale']
        self.input = self.fields['input']
        makegraph(self.g)
        self.errortext='" This equation contains a detail that has not been fully resolved'
        self.rungraphs=[]
        

    def addTextField(self, master, name, text = 'f(x)=', row = 2, column =1,
                     columnspan = 1, rowspan = 1,
                     width = 20, sticky = N+E, state = NORMAL):
        """Creates and inserts a text field at the row and column,
and returns the text field."""
        field = strField(master, text, width, state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        field.grid(row = row, column = column,
                   columnspan = columnspan, rowspan = rowspan,
                   padx = 5, pady = 5, sticky = sticky)
        self.fields[name] = field
        return field

    def addButton(self, master, text, row = 1, column =1,
                  columnspan = 1, rowspan = 1,
                  command = lambda: None,
                  state = NORMAL):
        """Creates and inserts a button at the row and column,
        and returns the button."""
        button = Button(master, text = text,
                                command = command, state = state)
        master.rowconfigure(row, weight = 1)
        master.columnconfigure(column, weight = 1)
        button.grid(row = row, column = column,
                    columnspan = columnspan, rowspan = rowspan,
                    padx = 5, pady = 5)
        return button

    def makeGraphFrame(self, root):
        turtle._Screen._root = root
        self.canvwidth = 850
        self.canvheight = 850
        turtle._Screen._canvas = self._canvas = canvas = turtle.ScrolledCanvas(
                root, 800, 550, self.canvwidth, self.canvheight)
        canvas.adjustScrolls()

        self.screen = _s_ = turtle.Screen()
        turtle.TurtleScreen.__init__(_s_, _s_._canvas)
        self.scanvas = _s_._canvas
        turtle.RawTurtle.screens = [_s_]
        return canvas

    def get(self):
        return self.input.get()

    def refreshCanvas(self, boolean = True):
        if self.dirty:
            self.t.clear()
            self.dirty=False
            if boolean:
                self.rungraphs=[]
            

    def clearCanvas(self):
        self.refreshCanvas()
        self.screen._delete('all')
        self.scanvas.config(cursor='')
        self.configGUI(NORMAL, DISABLED, DISABLED)

    def calculate(self):
        original = self.get()
        try: neq = create(original)
        except:
            if original.endswith(self.errortext): return
            self.input.set(original + self.errortext)
            return
        
        t = self.t
        if neq in self.rungraphs: return

        try: graph(t, neq)
        except:
            if original.endswith(self.errortext): return
            self.input.set(original + self.errortext)
            return
        self.rungraphs.append(neq)
        self.dirty=True

    def refreshscale(self):
        global scale
        nscale = self.nscale.get()
        if is_float(nscale) and float(nscale)>0 and float(nscale) != scale:
            graph(self.t, create('0'))
            self.dirty = True
            scale = tryint(float(nscale))
            
            self.refreshCanvas(False)
            self.g.clear()
            makegraph(self.g)
            if self.rungraphs:
                for neq in self.rungraphs:
                    graph(self.t, neq)
                self.dirty = True
        else:
            nscale = self.nscale.set(str(scale))

scale = 50
def main():
    global grapher
    grapher = NewWindow()
    tracer(False)
    replace = replacer(grapher.input)
    replace.start()
    grapher.root.mainloop()

if __name__ == '__main__':
    main()
