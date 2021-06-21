'''
py3d

Bringing 3d to tkinter.
A tkinter canvas that graphs 3d objects on a Python-wrought gui ...

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
Pre releases
 Pr 1
  Pr 1a:
   Capable of passing 3d points to 2d points.
   Not sure how to make this into a frame... in fact, I didn't think this
   through I only worked out the math part in my head, checked it on desmos
   (see https://www.desmos.com/calculator/bnk7wnndk1) and ... opened the .py
   document...

   The way this works is that you imagine a 3d vector from a point to an 'eye'
   (a point with a plane in front of it), where this vector intersects with the
   plane (in the plane) is where the point should be graphed at.
 Pr 2
  Pr 2a
   space object will hold figures and cameras. cameras now belong to a space.
   cameras have orientation and location with precomputations that allow
   it to pass 3d point methods for moving about
   A camera has two projection possibilities. project projects a point from the
   space while project1 projects an object that seems to hover in front of it
   though changes with orientation. (this is for an axis, for example: see
   newaxis in the desmos)
  Pr 2b
   The addition of figure classes.
   Figures can now be added to a space.
0
 0.0
  Version 0.0.0:
   Now can work with a canvas.
  Version 0.0.1:
   Now works with colors
   small bugfixes regarding objects going 'behind' a camera causing errors.
  Version 0.0.2:
   Better updating abilities
   Increased performance
   Increased handling
  Version 0.0.3:
   Stiched panes of 3d figures. (there was a gap between the panes)
 0.1
  Version 0.1.0:
   Heavy testing and debugging in movement... no more upside-down/backward/
   inverted movement when trying to navigate a 3d space. Also nicer loading.
  Version 0.1.1:
   make rectangle function... pseudo-shades the rectangles
   this is a placeholder for the actual shading abilities.
1
 1.0
  Version 1.0.0
   The entire system has been shifted for use with quaternion-coordinates.
   Lighting system implemented.
   Removing several bugs.
   Advanced transformation system for 3d objects
   Better ways to move camera around.
   More efficient code.
  Version 1.0.1
   Bugfixes
  Version 1.0.2 
   Bugfixes, efficiency improvements
'''

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__ = '1.0.0'

### IMPORTS ###
from .Cam import cam_base, cam_shape_method
from .shapes import pane, polyhedron, material
from .Simple_camera import simple_camera, make_rectangular_prism
from .Space import space
