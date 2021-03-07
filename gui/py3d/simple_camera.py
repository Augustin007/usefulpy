'''
Simple_camera

Simple camera class for py3d

Most important functions:
   simple_camera: camera

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
1
 1.1
  Version 1.1.1:
   Simple camera type.
'''
__author__ = 'Austin Garcia'
__version__ = '1.1.1'
__package__ = 'usefulpy.gui.py3d'

from .Cam import cam_base, cam_shape_method
from ...mathematics import nmath as _m
from ...mathematics import quaternion, i, j, k
from .shapes import polyhedron, pane, darken
from .Space import space
import time

_m.degrees()

light_scource = k
old_light = light_scource

def rgb2hex(r, g, b):
    r = hex(r)[2:]
    if len(r) == 1: r = '0'+r
    g = hex(g)[2:]
    if len(g) == 1: g = '0'+g
    b = hex(b)[2:]
    if len(b) == 1: b = '0'+b
    return '#'+r+g+b

light_scalar = _m.polynomial(1.4834383937541313, -74.97492931129165, 264.354983605755, -249.77887679968808, 90.73400104839939, -10.067233808282387)

def light(object):
    a1 = get_light(object.normal)
    a2 = get_light(-object.normal)
    r, g, b = object.material.texture
    r1, g1, b1 = darken(r, g, b, a1)
    r2, g2, b2 = darken(r, g, b, a2)
    return (r1, g1, b1), (r2, g2, b2)

def get_light(normal):
    a = abs(light_scource - normal)
    a = scale_light(a)
    return a

def scale_light(a):
    if a < 0:
        a = 0
    if a > 2:
        a = 2
    return int(light_scalar(a))

def get_thetax(q):
    return (_m.atan2(q.k, _m.hypot(q.i, q.j)) + 90)%360

def get_thetaz(q):
    return (_m.atan2(q.j, q.i) - 90)%360

def euler_angle(q):
    return get_thetax(q), get_thetaz(q)

class simple_camera(cam_base):
    def __init__(self, universe, position, heading, fov = 0.5, renderdistance = 12, personal_objects = None, shape = None):
        self.shape = shape
        self.fov = fov
        cam_base.__init__(self, universe, position, heading, renderdistance, personal_objects)

    def __repr__(self):
        return 'py3d.cam at {hex(id(self))}'

    def _compute(self):
        thetax, thetaz = euler_angle(self.heading)
        self.thetax, self.thetaz = self.euler = thetax, thetaz
        self.x3, self.y3, self.z3 = x3, y3, z3 = self.position.vtuple()
        self.pre1 = _m.cos(thetaz)
        self.pre2 = _m.sin(thetaz)
        self.pre3 = -_m.cos(thetax)
        self.pre4 = _m.sin(thetax)
        self.pre5 = -self.pre1*self.pre3
        self.pre6 = self.pre2*self.pre3
        self.pre7 = self.pre1*self.pre4
        self.pre8 = -self.pre2*self.pre4
        self.x = x3+self.fov*self.pre8
        self.y = y3+self.fov*self.pre7
        self.z = z3+self.fov*self.pre3
        self.x31 = -10*self.pre8
        self.y31 = -10*self.pre7
        self.z31 = -10*self.pre3
        self.plane_pos = quaternion(0, self.x, self.y, self.z)
        self.lighting_dict={}
    
    def project(self, object):
        if isinstance(object, (polyhedron, cam_base)):
            if isinstance(object, cam_base):
                if object.shape is None: return
            fig_list = list(object)
            distances = [abs(self.position-p.pos) for p in fig_list] 
            while distances:
                distance = max(distances)
                index = distances.index(distance)
                distances.pop(index)
                plane = fig_list.pop(index)
                self.project(plane)
            return
        if isinstance(object, pane):
            npoints = [self._project(point) for point in object]
            if None in npoints: return
            if (object._updated) or (id(object) not in self.lighting_dict) or (old_light != light_scource):
                self.lighting_dict[id(object)] = light(object)
                object._updated = False
            heading = (self.position - object.pos).normal()
            tup = abs(heading - object.normal), abs(object.normal + heading)
            if tup[0] >= tup[1]: r, g, b = self.lighting_dict[id(object)][1]
            else: r, g, b = self.lighting_dict[id(object)][0]
            for canvas in self.running_canvases:
                nnpoints = [rescale(point, canvas) for point in npoints]
                hex = rgb2hex(r, g, b)
                add_polygon(nnpoints, hex, canvas)
            return
        raise TypeError('This type of object is not supported yet')

    def _xr(self, x, y):
        '''x rotation of point'''
        xrs1 = self.pre1*(x-self.x3)
        xrs2 = self.pre2*(y-self.y3)
        return xrs1 + xrs2

    def _yr(self, x, y, z):
        '''y rotation of point'''
        yrs1 = self.pre6*(x-self.x3)
        yrs2 = self.pre5*(y-self.y3)
        yrs3 = self.pre4*(z-self.z3)
        return yrs1 + yrs2 + yrs3

    def _zr(self, x, y, z):
        '''z rotation of point'''
        zrs1 = self.pre8*(x-self.x3)
        zrs2 = self.pre7*(y-self.y3)
        zrs3 = self.pre3*(z-self.z3)
        return zrs1 + zrs2 + zrs3

    def _xr1(self, x, y):
        '''x rotation of point (ignores position and fov)'''
        xrs1 = self.pre1*(x-self.x31)
        xrs2 = self.pre2*(y-self.y31)
        return xrs1 + xrs2

    def _yr1(self, x, y, z):
        '''y rotation of point (ignores position and fov)'''
        yrs1 = self.pre6*(x-self.x31)
        yrs2 = self.pre5*(y-self.y31)
        yrs3 = self.pre4*(z-self.z31)
        return yrs1 + yrs2 + yrs3

    def _zr1(self, x, y, z):
        '''z rotation of point (ignores position and fov)'''
        zrs1 = self.pre8*(x-self.x31)
        zrs2 = self.pre7*(y-self.y31)
        zrs3 = self.pre3*(z-self.z31)
        return zrs1 + zrs2 + zrs3

    def _project_to_x(self, x, y, z):
        '''projection to x of point'''
        xrot = self._xr(x, y)
        zrot = self._zr(x, y, z)
        if zrot > 0: return xrot/zrot #zrot > 0 means object is behind

    def _project_to_y(self, x, y, z):
        '''projection to y of point'''
        yrot = self._yr(x, y, z)
        zrot = self._zr(x, y, z)
        if zrot > 0: return -yrot/zrot #zrot > 0 means object is behind

    def _project_to_x1(self, x, y, z):
        '''projection to x of point (ignores position and fov)'''
        xrot = self._xr1(x, y)
        zrot = self._zr1(x, y, z)
        if zrot != 0: return xrot/zrot

    def _project_to_y1(self, x, y, z):
        '''projection to y of point (ignores position and fov)'''
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        if zrot != 0: return -yrot/zrot

    def projectx(self, point):
        '''projection to x of point'''
        x, y, z = point.vtuple()
        return self._project_to_x(x, y, z)

    def projecty(self, point):
        '''projection to y of point'''
        x, y, z = point.vtuple()
        return self._project_to_y(x, y, z)

    def projectx1(self, point):
        '''projection to x of point (ignores position and fov)'''
        x, y, z = point.vtuple()
        return self._project_to_x1(x, y, z)

    def projecty1(self, point):
        '''projection to y of point (ignores position and fov)'''
        x, y, z = point.vtuple()
        return self._project_to_y1(x, y, z)

    def _project(self, p):
        x, y, z = p.vtuple()
        xrot = self._xr(x, y)
        yrot = self._yr(x, y, z)
        zrot = self._zr(x, y, z)
        if zrot > 0: return (xrot/zrot, -yrot/zrot)

    def _project1(self, point):
        x, y, z = point.vtuple()
        xrot = self._xr1(x, y)
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        if zrot > 0: return (xrot/zrot, -yrot/zrot)

def rescale(point, to):
    h = int(to.getHeight())
    w = int(to.getWidth())
    x, y = point
    scale = max(h, w)//2
    xadj = w//2
    yadj = h//2
    x *= scale
    y *= scale
    x += xadj
    y += yadj
    return x, y

def add_polygon(points, hex, canvas):
    args = []
    for point in points: args.extend(point)
    canvas.create_polygon(*args, fill = hex, outline = hex)

def point(x, y, z):
    return quaternion(0, x, y, z)

def make_rectangular_prism(universe, point1, point2, color):
    x1, y1, z1 = point1.vtuple()
    x2, y2, z2 = point2.vtuple()
    rectangular_prism = polyhedron(
        universe,
        cpane(universe, point(x1, y2, z2), point(x2, y2, z2), point(x2, y1, z2), point(x1, y1, z2), color = color),
        cpane(universe, point(x1, y2, z1), point(x1, y2, z2), point(x2, y2, z2), point(x2, y2, z1), color = color),
        cpane(universe, point(x2, y1, z1), point(x2, y2, z1), point(x2, y2, z2), point(x2, y1, z2), color = color),
        cpane(universe, point(x1, y1, z1), point(x2, y1, z1), point(x2, y1, z2), point(x1, y1, z2), color = color),
        cpane(universe, point(x1, y1, z1), point(x1, y2, z1), point(x1, y2, z2), point(x1, y1, z2), color = color),
        cpane(universe, point(x1, y1, z1), point(x1, y2, z1), point(x2, y2, z1), point(x2, y1, z1), color = color)
        )
    
    return rectangular_prism

def cpane(universe, *points, color):
    npane = pane(universe, *points)
    npane.material.texture = color
    return npane

if __name__ == '__main__':
    import tkinter
    from ...gui import Frame
    Space = space()
    cube = make_rectangular_prism(Space, -i-j-k, i+j+k, (255, 0, 0))
#    Pane = pane(i+j, i-j, -i-j, -i+j)
#    Space.addfigure(Pane)
    canv = Frame(width = 800, height =800).addCanvas(width = 800, height =800)
    cam = simple_camera(Space, quaternion(), i)
    cam.add_canvas(canv)