'''
shapes

3d shape processing for py3d

Most important functions:
   Material: material class for a surface
   pane: a surface class
   polyhedron: 3d surface

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Allows for processing of figures in 3d space. 
   Somewhat limited: especially in regards to there being no way to create 3d curves
'''

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__ = '0.0.0'

### IMPORTS ###
from ...mathematics.quaternion import quaternion, i, j, k
from .tools3d import is_on_plane, PointInTriangle, versor_from_points
import copy as _c

### UTILITY ###
def shift_iter(iter, num):
    amount =range(len(iter)-num+1)
    iters = []
    for n in amount:
        iters.append(iter[n, n+num])
    return zip(*iters)

def darken(r, g, b, by):
    r -= by
    if r > 255: r = 255
    if r < 0: r = 0
    g -= by
    if g > 255: g = 255
    if g < 0: g = 0
    b -= by
    if b > 255: b = 255
    if b < 0: b = 0
    return r, g, b


### MATERIALS CLASS ###
class material:
    def __init__(self, color, opacity, metallicity, roughness, normals_function):
        ##TODO: Replace 'color' argument with 'texture' that can support an image
        self.texture = color
        self.opacity = opacity
        self.metallicity = metallicity
        self.roughness = roughness
        self.normals = normals_function

    def bounce(material, ray, off):
        return NotImplemented

def smooth_normal(x, y):
    return k

default = material((255, 0, 0), 1, 1, 0, smooth_normal)

class pane:
    def __init__(self, universe, *points, material = None):
        if material == None:
            material = _c.copy(default)
        if len(points) < 3:
            raise TypeError('At least 3 points are needed')
        npoints = []
        
        for point in points:
            
            if type(point) is quaternion:
                if point.real != 0:
                    raise ValueError(f'Point {point} cannot properly be interpreted as a three-dimensional point')
                npoints.append(point)
                continue

            try:
                npoint = quaternion(point)
            except: pass
            else:
                if npoint.real != 0:
                    raise ValueError(f'Point {point} cannot properly be interpreted as a three-dimensional point')
                npoints.append(npoint)
                continue

            try:
                npoint = quaternion(0, *point)
            except: pass
            else:
                if npoint.real != 0:
                    raise ValueError(f'Point {point} cannot properly be interpreted as a three-dimensional point')
                npoints.append(npoint)
                continue

            raise ValueError(f'Point {point} cannot properly be interpreted as a three-dimensional point')
        points = tuple(npoints)
        del npoints
        
#        if len(points) > 3:
#            plane = points[0:3]
#            for point in points[3:]:
#                if not is_on_plane(plane, point):
#                    raise ValueError('Not all points are on the same plane')
#            plane = 0
        

        isum, jsum, ksum = 0, 0, 0
        lnth = len(points)
        for point in points:
            isum += point.i
            jsum += point.j
            ksum += point.k
        self.plane = points[0:3]
        self.points = points
        self.pos = quaternion(0, isum/lnth, jsum/lnth, ksum/lnth)
        self.normal = versor_from_points(self.plane)
        self.max = max([abs(point-self.pos) for point in points])
        self.material = material
        self.universe = universe
        self.universe.addfigure(self)
        self._updated = True

    def __iter__(self):
        '''iter through its 3d points'''
        return self.points.__iter__()

    def is_colliding(self, point):
        '''detects whether a point is touching the plane'''
        if not is_on_plane(self.plane, point): return False
        for a, b, c in shift_iter(self.points, 3):
            if PointInTriangle(point, a, b, c):
                return True
        return False

    def bounce(off_of, light_ray):
        return NotImplemented

    def rotate(self, r, v, a = None):
        if a is None: a = self.pos
        else: self.pos = self.pos.rotate(r, v, a)
        self.points = tuple([point.rotate(r, v, a) for point in self.points])
        self.normal = self.normal.rotate(r, v, a)
        self._updated = True

    def shift(self, by):
        self.points = tuple([point+by for point in self.points])
        self._updated = True

### SHAPES ###

#All valid shape types must include these
shape_methods = [
 'rotate', 'shift', '_tilt_up', '_tilt_dn', '_tilt_rt', '_tilt_lt',
 '_fdx', '_fdy', '_fdz', '_bkx', '_bky', '_bkz', '_fdxy', '_fdyz',
 '_fdzx', '_bkzx', '_bkxy', '_bkyz', '_rt', '_lt', '_up', '_dn',
 'tp', 'seth', '_fd', '_bk', 'setx', 'sety', 'setz'
 ]

class polyhedron:
    def __init__(self, universe, *faces):
        for face in faces:
            if face.universe is not universe:
                raise ValueError('Panes must all be in same universe')
            universe.remove_fig(face)
        self.faces = faces
        xsum, ysum, zsum = 0, 0, 0
        lnth = 0
        for polygon in self.faces:
            for point in polygon.points:
                lnth += 1
                xsum += point.i
                ysum += point.j
                zsum += point.k
        self.pos = quaternion(0, xsum/lnth, ysum/lnth, zsum/lnth)
        self.facing = quaternion()
        self.universe = universe
        self.universe.addfigure(self)

    def __iter__(self):
        return self.faces.__iter__()

    def rotate(self, r, v, a = None):
        if a is None: a = self.pos
        else: self.pos = self.pos.rotate(r, v, a)
        for plane in self.faces: plane.rotate(r, v, a)
        self.facing = self.facing.rotate(r, v, a)
        
