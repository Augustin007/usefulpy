'''
File: py3d.py
Version: 
Author: Austin Garcia

A frame ish thing that graphs 3d objects on a Python-wrought gui...

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
   Capable of passing 3d points to 2d points.
   Not sure how to make this into a frame... in fact, I didn't think this
   through I only worked out the math part in my head, checked it on desmos
   (see https://www.desmos.com/calculator/bnk7wnndk1) and ... opened the .py
   document...

   The way this works is that you imagine a 3d vector from a point to an 'eye'
   (a point with a plane in front of it), where this vector intersects with the
   plane (in the plane) is the point is should be graphed at.
 1.2
  Version 1.2.1:
   space object will hold figures and cameras. cameras now belong to a space.
   cameras have orientation and location with precomputations that allow
   it to pass 3d point methods for moving about
   A camera has two projection possibilities. project projects a point from the
   space while project1 projects an object that seems to hover in front of it
   though changes with orientation. (this is for an axis, for example, see new
   axis in the desmos)
  Version 1.2.2:
   The addition of figure classes.
   Figures can now be added to a space.
2
 2.1
  Version 2.1.1:
   Entire code rewritten, now can work with a canvas.
  Version 2.1.2:
   Now works with colors
   small bugfixes regarding objects going 'behind' a camera causing errors.
  Version 2.1.3:
   Better updating abilities
   Increased performance
   Increased handling
  Version 2.1.4:
   Stiched panes of 3d figures. (there was a gap between the panes)

'''

from usefulpy.mathematics.nmath import *
import usefulpy.validation as _validation
degrees()

from collections import namedtuple
Point3d = namedtuple('Point3d', ('x', 'y', 'z'))
Point2d = namedtuple('Point2d', ('x', 'y'))

class space(object):
    '''Spaces store information about canvases, cameras, and figures'''
    def __init__(self):
        '''init for space class, a space's data is added separately.'''
        self.space = []
        self.cameras = {}
        self.runningCanvases = {}
        self.frozenCanvases = {}
        self.view = None

    def addcamera(self, name, fov=0.5, x=0, y=0, z=0, thetax=0, thetaz=0, visible=False, shape=None, renderdistance=12):
        '''Adds a camera to the space'''
        if type(name) is not str: raise TypeError('name must be str')
        newcam = _camera(self, fov, x, y, z, thetax, thetaz, visible=visible, shape=shape, renderdistance=renderdistance)
        if name in self.cameras: raise KeyError(f'camera {name} already exists in this space')
        self.cameras[name] = newcam
        self.space.append(newcam)
        return newcam

    def addfigure(self, figure):
        '''adds a figure to the space'''
        if type(figure) != figure3d: raise TypeError('Figure must be a figure3d object')
        self.space.append(figure)
        return figure

    def setview(self, to):
        '''set a default view for the space'''
        if type(to) is str:
            if to not in self.cameras: raise KeyError(f'{to} not found')
            self.view = self.cameras[to]
            return
        if type(to) is _camera:
            if to.universe != self: raise ValueError(f'{to} not in this universe')
            self.view = to
            return
        raise TypeError(f'{to} should be str or py3d._camera')

    def view_in_canvas(self, at):
        '''view from default view at a canvas 'at' '''
        if self.view is None: raise Exception('self.view is not defined')
        return self._view_from(self.view, at)

    def _recieve_update_msg(self):
        for canv in self.runningCanvases:
            self._update(canv)

    def _update(self, canv):
        if canv not in self.runningCanvases: raise ValueError
        cam = self.runningCanvases[canv]
        self._view_from(cam, canv)
        canv.update()

    def view_from(self, cam, at):
        '''view from cam at a canvas 'at' '''
        if type(cam) is str:
            if to not in self.cameras: raise KeyError(f'{cam} not found')
            cam = self.cameras[cam]
        if type(cam) is _camera:
            if cam.universe != self: raise ValueError(f'{cam} not in this universe')
        else: raise TypeError(f'{to} should be str or py3d._camera')
        return self._view_from(cam, at)

    def _view_from(self, cam, at):
        self.runningCanvases[at] = cam
        cam.runningCanvases.append(at)
        tempspace = self.space.copy()
        distances = [Distance(cam.posa, fig.pos) for fig in tempspace]

        at.delete('all')

        while tempspace: #nesting here is a bit deep, can probably be improved.
            distance = max(distances)
            if distance < cam.renderdistance:
                
                figindex = distances.index(distance)
                fig = tempspace.pop(figindex)
                distances.pop(figindex)
                if fig is not cam:
    
                    minidistances = [Distance(cam.posa, pane.pos) for pane in fig]
                    fig = list(fig)
                    while minidistances:
                        
                        minidistance = max(minidistances)
                        paneindex = minidistances.index(minidistance)
                        minidistances.pop(paneindex)
                        pane = fig.pop(paneindex)
                        try:
                            npoints = [cam.project(point, at) for point in pane]
                            #print(pane.color)
                            squishedfig = figure2d(*npoints, color = pane.color, outline = pane.outline)
                            squishedfig.project_to_canvas(at)
                        except: pass
                
    def freezecanvas(self, canvas):
        '''freezes 3d updates to a canvas'''
        cam = self.runningCanvases[canvas]
        del self.runningCanvases[canvas]
        self.frozenCanvases[canvas] = cam

    def pop(self, canvas):
        '''unlinks a canvas from the space, returns canvas'''
        try:
            del self.runningCanvases[canvas]
            return canvas
        except: pass
        try:
            del self.frozenCanvases[canvas]
            return canvas
        except: pass
        raise f'canvas {canvas} is not displaying this universe.'

    def unfreezecanvas(self, canvas):
        '''unfreeze 3d updates to a canvas'''
        cam = self.frozenCanvases[canvas]
        del self.frozenCanvases[canvas]
        self.runningCanvases[canvas] = cam

    def __iter__(self):
        '''__iter__ for space... goes through all items in the space.'''
        return self.space.__iter__()

def Distance(a, b):
    '''distance for tuples/Point3d/Point2d objects'''
    return hypot(*[x - y for x, y in zip(a, b)])

class _camera(object):
    '''Camera for a space'''
    def __init__(self, universe, fov=0.5, x=0, y=0, z=0, thetax=0, thetaz=0, visible=False, shape=None, renderdistance=12):
        assert type(universe) is space
        assert _validation.is_float(x)
        assert _validation.is_float(y)
        assert _validation.is_float(z)
        assert _validation.is_float(thetax)
        assert _validation.is_float(thetaz)
        assert _validation.is_float(fov)
        assert _validation.is_float(renderdistance)
        assert (shape is None) or (type(shape) is figure3d)
        #x, y, z, camera's coordinates
        #theta, rho camera angles
        #fov, distance of pane from point
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.universe = universe #This is the space that the camera exists in
        self.thetax = float(thetax)
        self.thetaz = float(thetaz)
        self.renderdistance = float(renderdistance)
        self.fov = float(fov)
        self.is_visible = bool(visible)
        self.shape = shape
        self.runningCanvases = []
        self._precompute() #computations

    def _precompute(self):
        '''stuff its going to use tons of times so I might as well calculate
        now'''
        thetax = self.thetax = self.thetax%360
        thetaz = self.thetaz = self.thetaz%360
        x, y, z = (self.x, self.y, self.z)
        #print(x, y, z)
        self.pos = Point3d(x, y, z)
        self.heading = (thetax, thetaz)
        self.pre1 = cos(thetaz)
        self.pre2 = sin(thetaz)
        self.pre3 = -cos(thetax)
        self.pre4 = sin(thetax)
        self.pre5 = -self.pre1*self.pre3
        self.pre6 = self.pre2*self.pre3
        self.pre7 = self.pre1*self.pre4
        self.pre8 = -self.pre2*self.pre4
        self.x3 = x-self.fov*self.pre8
        self.y3 = y-self.fov*self.pre7
        self.z3 = z-self.fov*self.pre3
        self.x31 = -10*self.pre8
        self.y31 = -10*self.pre7
        self.z31 = -10*self.pre3
        self.posa = Point3d(self.x3, self.y3, self.z3)
        if self.runningCanvases: self.universe._recieve_update_msg()

    #Rotations
    #rs (rotation section) = self.pre[n]*([d]-self.[d]3)

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
        if zrot > 0: return yrot/zrot #zrot > 0 means object is behind

    def _project_to_x1(self, x, y, z):
        '''projection to x of point (ignores position and fov)'''
        xrot = self._xr1(x, y)
        zrot = self._zr1(x, y, z)
        if zrot != 0: return xrot/zrot

    def _project_to_y1(self, x, y, z):
        '''projection to y of point (ignores position and fov)'''
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        if zrot != 0: return yrot/zrot

    def projectx(self, point):
        '''projection to x of point'''
        x, y, z = point
        return self._project_to_x(x, y, z)

    def projecty(self, point):
        '''projection to y of point'''
        x, y, z = point
        return self._project_to_y(x, y, z)

    def projectx1(self, point):
        '''projection to x of point (ignores position and fov)'''
        x, y, z = point
        return self._project_to_x1(x, y, z)

    def projecty1(self, point):
        '''projection to y of point (ignores position and fov)'''
        x, y, z = point
        return self._project_to_y1(x, y, z)

    def project(self, point, at):
        '''projection of 3d point to 2d'''
        x, y, z = point
        pt2ds = self._project(x, y, z)
        if pt2ds is None: return
        return rescale(pt2ds, at)

    def _project(self, x, y, z):
        '''projection of 3d point to 2d'''
        xrot = self._xr(x, y)
        yrot = self._yr(x, y, z)
        zrot = self._zr(x, y, z)
        if zrot > 0: return Point2d(xrot/zrot, yrot/zrot)

    def _project1(self, x, y, z):
        '''projection of 3d point to 2d (ignores position and fov)'''
        xrot = self._xr1(x, y)
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        if zrot > 0: return Point2d(xrot/zrot, yrot/zrot)

    def project1(self, point, at):
        '''projection of 3d point to 2d (ignores position and fov)'''
        x, y, z = point
        pt2ds = self._project1(x, y, z)
        if pt2ds is None: return
        return rescale(pt2s, at)        

    def tiltup(self, degrees):
        '''tilt camera up degrees'''
        self.thetax += degrees
        self._precompute()

    def tiltdown(self, degrees):
        '''tilt camera down degrees'''
        self.thetax -= degrees
        self._precompute()

    def tiltleft(self, degrees):
        '''tilt camera left degrees'''
        self.thetaz += degrees
        self._precompute()

    def tiltright(self, degrees):
        '''tilt camera right degrees'''
        self.thetaz -= degrees
        self._precompute()

    def fdx(self, amount):
        '''move cam fd along the x axis'''
        self.x += amount
        self._precompute()

    def fdy(self, amount):
        '''move cam fd along the y axis'''
        self.y += amount
        self._precompute()

    def fdz(self, amount):
        '''move cam fd along the z axis'''
        self.z += amount
        self._precompute()

    def bkx(self, amount):
        '''move cam bk along the x axis'''
        self.x -= amount
        self._precompute()

    def bky(self, amount):
        '''move cam bk along the y axis'''
        self.y -= amount
        self._precompute()

    def bkz(self, amount):
        '''move cam bk along the z axis'''
        self.z -= amount
        self._precompute()

    def fdxy(self, amount): ##Not tested
        '''move the cam fd along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = cos(self.thetaz)
        yrat = sin(self.thetaz)
        self.x += amount*xrat
        self.y += amount*yrat
        self._precompute()

    def fdyz(self, amount): ##Not tested
        '''move the cam fd along the y and z axis in the direction the camera
is facing, keeping the x-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def fdzx(self, amount): ##Not tested
        '''move the cam fd along the z and x axis in the direction the camera
is facing, keeping the y-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x += amount*xrat
        self.z += amount*zrat
        self._precompute()

    def bkxy(self, amount): ##Not tested
        '''move the cam bk along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = cos(self.thetaz)
        yrat = sin(self.thetaz)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self._precompute()

    def bkyz(self, amount): ##Not tested
        '''move the cam bk along the y and z axis in the direction the camera
is facing, keeping the x-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def bkzx(self, amount): ##Not tested
        '''move the cam bk along the z and x axis in the direction the camera
is facing, keeping the y-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def rt(self, amount):
        '''move the cam rt along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = sin(self.thetax + 90)
        zrat = cos(self.thetax + 90)
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def lt(self, amount):
        '''move the cam lt along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = sin(self.thetax - 90)
        zrat = cos(self.thetax - 90)
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def up(self, amount):
        '''move the cam location up (increase z value)'''
        self.z += amount
        self._precompute()

    def dn(self, amount):
        '''move the cam location dn (decrease z value)'''
        self.z -= amount
        self._precompute()

    def tp(self, to):
        '''teleport camera location'''
        self.x, self.y, self.z = to
        self._precompute()

    def seth(self, to):
        '''set heading to a tuple (thetax, thetaz)'''
        self.thetax, self.thetaz = to
        self._precompute()

    def fd(self, amount): ##Not tested
        '''fd according to heading, moving all axis'''
        xrat = cos(self.thetaz)*sin(self.thetax)
        yrat = sin(self.thetaz)*sin(self.thetax)
        zrat = cos(self.thetax)
        self.x += amount*xrat
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def bk(self, amount): ##Not tested
        '''bk according to heading, moving all axis'''
        xrat = cos(self.thetaz)*sin(self.thetax)
        yrat = sin(self.thetaz)*sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self.z -= amount*zrat
        self._precompute()

    def __repr__(self):
        '''__repr__ for cam'''
        return f'<(py3d._camera at {self.pos}, facing: ({self.thetax}, {self.thetaz}), field of vision (fov): {self.fov}, render distance: {self.renderdistance}>'

    def __iter__(self):
        '''__iter__ for _camera'''
        if self.shape: return self.shape.__iter__()
        return ().__iter__()

class figure3d(object):
    '''3d figure for a space, built of figure2d3ds
Polygons do not need to be perfectly closed, but it is recommended
to avoid small bugs'''
    def __new__(cls, *polygons):
        '''__new__ for figure3d'''
        #for polygon in polygons:
        #    print(polygon.color)
        self = super(figure3d, cls).__new__(cls)
        npolygons = []
        #print(polygons)
        for polygon in polygons:
            #print('>>'+str(polygon))
            if type(polygon) is not figure2d3d:
                #print('')
                polygon=figure2d3d(*polygon)
            npolygons.append(polygon)
            #print(polygon.color)
        self.polygons=tuple(npolygons)
        xsum, ysum, zsum = 0, 0, 0
        lnth = 0
        for polygon in self.polygons:
            for point in polygon.points:
                lnth += 1
                xsum += point.x
                ysum += point.y
                zsum += point.z
        self.pos = Point3d(xsum/lnth, ysum/lnth, zsum/lnth)
        return self

    def __iter__(self):
        '''iterates through its faces'''
        return self.polygons.__iter__()

class figure2d(object):
    '''Polygon, 2d figure'''
    def __new__(cls, *points, color ='black', outline = None):
        '''__new__ for figure2d'''
        self = super(figure2d, cls).__new__(cls)
        if outline is None: outline = color
        self.color = color
        self.outline = outline
        #print(points)
        npoints=[]
        for point in points:
            npoint=tuple(point)
            #print(npoint)
            pnt2ds=Point2d(*npoint)
            npoints.append(pnt2ds)
        self.points=tuple(npoints)
        xsum, ysum = 0,0
        lnth = len(self.points)
        for point in self.points:
            xsum += point.x
            ysum += point.y
        self.averagepoint = Point2d(xsum/lnth, ysum/lnth)
        return self

    def project_to_canvas(self, ncanvas):
        '''project it to a canvas'''
        arglist = []
        #print(self.color)
        
        for point in self: arglist.extend((point.x, point.y))
        ncanvas.create_polygon(*arglist, fill = self.color, outline = self.outline)

    def __iter__(self):
        '''iterate through points'''
        return self.points.__iter__()

class figure2d3d(object):
    '''2d figures with 3d points.
These points technically do not need to be in the same plane,
but can be 'folded' into a third dimension, though this does cause some
wierd overlaying at certain angles.'''
    def __new__(cls, *points, color = 'black', outline = None):
        '''__new__ for figure2d3d'''
        self = super(figure2d3d, cls).__new__(cls)
        #print(color)
        npoints=[]
        if outline is None: outline = color
        self.color = color
        self.outline = outline
        #print(self.color)
        #print(points)
        for point in points:
            npoint=tuple(point)
            #print(npoint)
            pnt3ds=Point3d(*npoint)
            npoints.append(pnt3ds)
        self.points=tuple(npoints)
        xsum, ysum, zsum = 0, 0, 0
        lnth = len(self.points)
        for point in self.points:
            xsum += point.x
            ysum += point.y
            zsum += point.z
        self.pos = Point3d(xsum/lnth, ysum/lnth, zsum/lnth)
        return self

    def __iter__(self):
        '''iter through its 3d points'''
        return self.points.__iter__()

class line_segment3d(object):
    '''A line segment through 3 dimensions, not implimented'''
    def __new__(cls, a, b):
        self = super(line_segment3d, cls).__new__(cls)
        a, b = tuple(a), tuple(b)
        self.pointa=Point3d(*a)
        self.pointb=Point3d(*b)
        return self

    def __iter__(self):
        return (self.pointa, self.pointb).__iter__()

'''
create_polygon(self, *args, **kw)
Create polygon with coordinates x1,y1,...,xn,yn.
'''

class line_segment2d(object):
    '''a line segment through 2 dimensions, not implimented'''
    def __new__(self, a, b):
        self = super(line_segment2d, cls).__new__(cls)
        a, b = tuple(a), tuple(b)
        self.pointa=Point2d(*a)
        self.pointb=Point2d(*b)
        return self

    def __iter__(self):
        (self.pointa, self.pointb).__iter__()

def rescale(point, to):
    '''rescales points to window from the 3d projection'''
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

    return Point2d(x, y)

def _main():
    '''this acts as a mini-driver.'''
    from usefulpy.gui.__init__ import Frame
    import time
    global canv, area, cam, cube
    canv = Frame(width = 800, height =800).addCanvas(width = 800, height =800)
    area = space()
    cubefigs = (
        figure2d3d((-1, -1, -1),(-1, 1, -1), (-1, 1, 1), (-1, -1, 1), color = 'blue'),
        figure2d3d((-1,-1,-1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), color = 'red'),
        figure2d3d((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), color = 'blue'),
        figure2d3d((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), color = 'green'),
        figure2d3d((-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), color = 'red'),
        figure2d3d((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1), color = 'black'))
    #for fig in cubefigs:
    #    print('>>', fig.color)
    cube = figure3d(*cubefigs)
    area.addfigure(cube)
    cam = area.addcamera('cam', fov=10, thetax=120, thetaz=140)
    #print(area.space)
    area.setview('cam')
    area.view_in_canvas(canv)
    for x in range(360):
        cam.tiltright(1)
        time.sleep(0.05)

if __name__ == '__main__':
    import tkinter
    _main()


    



