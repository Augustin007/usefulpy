'''
File: py3d.py
Version: 
Author: Austin Garcia

Bringing 3d to tkinter.
A tkinter canvas that graphs 3d objects on a Python-wrought gui ...

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
   though changes with orientation. (this is for an axis, for example: see
   newaxis in the desmos)
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
 2.2
  Version 2.2.1:
   Heavy testing and debugging in movement... no more upside-down/backward/
   inverted movement when trying to navigate a 3d space. Also nicer loading.
  Version 2.2.2:
   make rectangle function... pseudo-shades the rectangles
   this is a placeholder for the actual shading abilities.

'''
import time
__version__ = '2.2.2'
from usefulpy.mathematics.nmath import *
import usefulpy.validation as _validation
degrees()
import tkinter
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
        #camera shape does not work.
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
        self._update(canvas)

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
        #Shape does not work yet.

        #Note... may want to add limits for angular movement

        #x, y, z, camera's coordinates
        #theta, rho camera angles
        #fov, distance of pane from point 'field of vision'

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.universe = universe
        #This is the space that the camera exists in

        self.thetax = float(thetax)
        self.thetaz = float(thetaz)
        self.renderdistance = float(renderdistance)
        self.fov = float(fov)
        self.is_visible = bool(visible)
        self.shape = shape
        self.runningCanvases = []
        #self.objects = []  #for project1
        self.spnspeed = 0.0025
        self.movspeed = 0.01
        self._precompute() #computations

    #def addobject(self, obj): #These will use project1.
    #    self.objects.append(obj)

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
        if zrot > 0: return Point2d(xrot/zrot, -yrot/zrot)

    def _project1(self, x, y, z):
        '''projection of 3d point to 2d (ignores position and fov)'''
        xrot = self._xr1(x, y)
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        if zrot > 0: return Point2d(xrot/zrot, -yrot/zrot)

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

    def _fdx(self, amount):
        '''move cam fd along the x axis'''
        self.x += amount
        self._precompute()

    def _fdy(self, amount):
        '''move cam fd along the y axis'''
        self.y += amount
        self._precompute()

    def _fdz(self, amount):
        '''move cam fd along the z axis'''
        self.z += amount
        self._precompute()

    def _bkx(self, amount):
        '''move cam bk along the x axis'''
        self.x -= amount
        self._precompute()

    def _bky(self, amount):
        '''move cam bk along the y axis'''
        self.y -= amount
        self._precompute()

    def _bkz(self, amount):
        '''move cam bk along the z axis'''
        self.z -= amount
        self._precompute()

    def _fdxy(self, amount):
        '''move the cam fd along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = sin((-self.thetaz)%360)
        yrat = cos((-self.thetaz)%360)
        self.x += amount*xrat
        self.y += amount*yrat
        self._precompute()

    def _fdyz(self, amount): ##Not tested
        '''move the cam fd along the y and z axis in the direction the camera
is facing, keeping the x-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def _fdzx(self, amount): ##Not tested
        '''move the cam fd along the z and x axis in the direction the camera
is facing, keeping the y-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x += amount*xrat
        self.z += amount*zrat
        self._precompute()

    def _bkxy(self, amount):
        '''move the cam bk along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = sin((-self.thetaz)%360)
        yrat = cos((-self.thetaz)%360)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self._precompute()

    def _bkyz(self, amount): ##Not tested
        '''move the cam bk along the y and z axis in the direction the camera
is facing, keeping the x-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def _bkzx(self, amount): ##Not tested
        '''move the cam bk along the z and x axis in the direction the camera
is facing, keeping the y-location still'''
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def _rt(self, amount):
        '''move the cam rt along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = cos((-self.thetaz)%360)
        yrat = -sin((-self.thetaz)%360)
        self.y += amount*yrat
        self.x += amount*xrat
        self._precompute()

    def _lt(self, amount):
        '''move the cam lt along the x and y axis in the direction the camera
is facing, keeping the z-location still'''
        xrat = -cos((-self.thetaz)%360)
        yrat = sin((-self.thetaz)%360)
        self.y += amount*yrat
        self.x += amount*xrat
        self._precompute()

    def _up(self, amount):
        '''move the cam location up (increase z value)'''
        self.z += amount
        self._precompute()

    def _dn(self, amount):
        '''move the cam location dn (decrease z value)'''
        self.z -= amount
        self._precompute()

    def fdat(self, amount, heading):
        '''fd according to heading argument, moving all axis'''
        xrat = sin((-heading[1])%360)*sin(heading[0])
        yrat = cos((-heading[1])%360)*sin(heading[0])
        zrat = -cos(self.thetax)
        self.x += amount*xrat
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def tp(self, to):
        '''teleport camera location'''
        self.x, self.y, self.z = to
        self._precompute()

    def seth(self, to):
        '''set heading to a tuple (thetax, thetaz)'''
        self.thetax, self.thetaz = to
        self._precompute()

    def _fd(self, amount):
        '''fd according to heading, moving all axis'''
        xrat = sin((-self.thetaz)%360)*sin(self.thetax)
        yrat = cos((-self.thetaz)%360)*sin(self.thetax)
        zrat = -cos(self.thetax)
        self.x += amount*xrat
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def _bk(self, amount):
        '''bk according to heading, moving all axis'''
        xrat = sin((-self.thetaz)%360)*sin(self.thetax)
        yrat = cos((-self.thetaz)%360)*sin(self.thetax)
        zrat = -cos(self.thetax)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self.z -= amount*zrat
        self._precompute()

    def setfov(self, to):
        self.fov = to
        self._precompute()

    def setx(self, to):
        self.x = to
        self._precompute()

    def sety(self, to):
        self.y = to
        self._precompute()

    def setz(self, to):
        self.z = to
        self._precompute()

    def __repr__(self):
        '''__repr__ for cam'''
        return f'<(py3d._camera at {self.pos}, facing: ({self.thetax}, {self.thetaz}), field of vision (fov): {self.fov}, render distance: {self.renderdistance}>'

    def __iter__(self):
        '''__iter__ for _camera'''
        if self.shape: return self.shape.__iter__()
        return ().__iter__()

    def spinrt(self, amount):
        final = amount-int(amount)
        for x in range(int(amount)):
            self.tiltright(1)
            time.sleep(self.spnspeed)
        self.tiltright(final)

    def spinlt(self, amount):
        final = amount-int(amount)
        for x in range(int(amount)):
            self.tiltleft(1)
            time.sleep(self.spnspeed)
        self.tiltleft(final)

    def spinup(self, amount):
        final = amount-int(amount)
        for x in range(int(amount)):
            self.tiltup(1)
            time.sleep(self.spnspeed)
        self.tiltup(final)

    def spindn(self, amount):
        final = amount-int(amount)
        for x in range(int(amount)):
            self.tiltdown(1)
            time.sleep(self.spnspeed)
        self.tiltdown(final)

    def spinto(self, to): return NotImplemented #spin to face an angle
    def spin(self, amount): return NotImplemented #amount is a 2d tuple
    def goto(self, to): return NotImplemented 
    def gotowards(self, towards): return NotImplemented 
    def followpath(self, towards): return NotImplemented 
    def slidefov(self, to): return NotImplemented #slides fov
    def spintoface(self, point): return NotImplemented #spin to face a point
    def _mvfd(self, amount, speed = None):
        if speed == 0: return self._fd(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fd(0.1)
            time.sleep(nspeed)
        self._fd(decimal)
    def fd(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfd(amount, speed)
        return self._fd(amount)

    def _mvbk(self, amount, speed = None):
        if speed == 0: return self._bk(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bk(0.1)
            time.sleep(nspeed)
        self._bk(decimal)
    def bk(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbk(amount, speed)

    def _mvrt(self, amount, speed = None):
        if speed == 0: return self._rt(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._rt(0.1)
            time.sleep(nspeed)
        self._rt(decimal)
    def rt(self, amount, smooth = True, speed = None):
        if smooth: return self._mvrt(amount, speed)
        return self._rt(amount)
    def _mvlt(self, amount, speed = None):
        if speed == 0: return self._lt(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._lt(0.1)
            time.sleep(nspeed)
        self._lt(decimal)
    def lt(self, amount, smooth = True, speed = None):
        if smooth: return self._mvlt(amount, speed)
        return self._lt(amount)
    def _mvup(self, amount, speed = None):
        if speed == 0: return self._up(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._up(0.1)
            time.sleep(nspeed)
        self._up(decimal)
    def up(self, amount, smooth = True, speed = None):
        if smooth: return self._mvup(amount, speed)
        return self._up(amount)
    def _mvdn(self, amount, speed = None):
        if speed == 0: return self._dn(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._dn(0.1)
            time.sleep(nspeed)
        self._dn(decimal)
    def dn(self, amount, smooth = True, speed = None):
        if smooth: return self._mvdn(amount, speed)
        return self._dn(amount)
        return self._bk(amount)
    def _mvfdx(self, amount, speed = None):
        if speed == 0: return self._fdx(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdx(0.1)
            time.sleep(nspeed)
        self._fdx(decimal)
    def fdx(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdx(amount, speed)
        return self._fdx(amount)
    def _mvfdy(self, amount, speed = None):
        if speed == 0: return self._fdy(amount)
    def _mvfdyz(self, amount, speed = None):
        if speed == 0: return self._fdyz(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdyz(0.1)
            time.sleep(nspeed)
        self._fdyz(decimal)
    def fdyz(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdyz(amount, speed)
        return self._fdyz(amount)
    def _mvfdzx(self, amount, speed = None):
        if speed == 0: return self._fdzx(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdzx(0.1)
            time.sleep(nspeed)
        self._fdzx(decimal)
    def fdzx(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdzx(amount, speed)
        return self._fdzx(amount)
    def _mvbkx(self, amount, speed = None):
        if speed == 0: return self._bkx(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bkx(0.1)
            time.sleep(nspeed)
        self._bkx(decimal)
    def bkx(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbkx(amount, speed)
        return self._bkx(amount)
    def _mvbky(self, amount, speed = None):
        if speed == 0: return self._bky(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bky(0.1)
            time.sleep(nspeed)
        self._bky(decimal)
    def bky(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbky(amount, speed)
        return self._bky(amount)
    def _mvbkz(self, amount, speed = None):
        if speed == 0: return self._bkz(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bkz(0.1)
            time.sleep(nspeed)
        self._bkz(decimal)
    def bkz(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbkz(amount, speed)
        return self._bkz(amount)
    def _mvbkxy(self, amount, speed = None):
        if speed == 0: return self._bkxy(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bkxy(0.1)
            time.sleep(nspeed)
        self._bkxy(decimal)
    def bkxy(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbkxy(amount, speed)
        return self._bkxy(amount)
    def _mvbkyz(self, amount, speed = None):
        if speed == 0: return self._bkyz(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bkyz(0.1)
            time.sleep(nspeed)
        self._bkyz(decimal)
    def bkyz(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbkyz(amount, speed)
        return self._bkyz(amount)
    def _mvbkzx(self, amount, speed = None):
        if speed == 0: return self._bkzx(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._bkzx(0.1)
            time.sleep(nspeed)
        self._bkzx(decimal)
    def bkzx(self, amount, smooth = True, speed = None):
        if smooth: return self._mvbkzx(amount, speed)
        return self._bkzx(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdy(0.1)
            time.sleep(nspeed)
        self._fdy(decimal)
    def fdy(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdy(amount, speed)
        return self._fdy(amount)
    def _mvfdz(self, amount, speed = None):
        if speed == 0: return self._fdz(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdz(0.1)
            time.sleep(nspeed)
        self._fdz(decimal)
    def fdz(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdz(amount, speed)
        return self._fdz(amount)
    def _mvfdxy(self, amount, speed = None):
        if speed == 0: return self._fdxy(amount)
        if speed is None: speed = self.movspeed
        nspeed = speed/10
        namount = amount*10
        decimal = namount - int(namount)
        decimal /= 10
        for n in range(int(namount)):
            self._fdxy(0.1)
            time.sleep(nspeed)
        self._fdxy(decimal)
    def fdxy(self, amount, smooth = True, speed = None):
        if smooth: return self._mvfdxy(amount, speed)
        return self._fdxy(amount)
        
        

class figure3d(object):
    '''3d figure for a space, built of figure2d3ds
Polygons do not need to be perfectly closed, but it is recommended
to avoid small bugs'''
    def __new__(cls, *polygons):
        '''__new__ for figure3d'''
        self = super(figure3d, cls).__new__(cls)
        npolygons = []
        for polygon in polygons:
            if type(polygon) is not figure2d3d:
                polygon=figure2d3d(*polygon)
            npolygons.append(polygon)
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
        npoints=[]
        for point in points:
            npoint=tuple(point)
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
        
        if outline is None: outline = color
        self.color = color
        self.outline = outline
        
        npoints=[]
        for point in points:
            npoint=tuple(point)
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
    def __new__(cls, *args, color = 'black'):
        self = super(line_segment3d, cls).__new__(cls)
        self.points = tuple(map(Point3d, args))
        self.color = color
        return self

    def __iter__(self):
        return self.points.__iter__()

class line_segment2d(object):
    '''a line segment through 2 dimensions, not implimented'''
    def __new__(self, *args, color = 'black'):
        self = super(line_segment2d, cls).__new__(cls)
        self.points = tuple(map(Point2d, args))
        self.color = color
        return self

    def __iter__(self):
        return self.points.__iter__()

    def project_to_canvas(self, ncanvas):
        '''project it to a canvas'''
        arglist = []
        
        for point in self: arglist.extend((point.x, point.y))
        ncanvas.create_line(*arglist, fill = self.color)

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

_tstcnv = tkinter.Canvas()
def make_rectangular_prism(point1, point2, *colors):
    assert len(colors)<= 6
    if not colors: colors = ('black')
    if len(colors) == 1:
        try:
            color = colors[0]
            #temporary mini-shading method... wouldn't actually work when
            #lighting is introduced
            tstc = (f'{color}1', f'{color}2', f'{color}3', f'{color}', f'{color}3', f'{color}4')
            for color in tstc:
                _tstcnv.create_polygon(0, 0, 1, 1, fill = color)
            colors = tstc
        except:
            pass
    if len(colors) < 6:
        lnth = len(colors)
        colors = [colors[n%lnth] for n in range(6)]
    zipped_points = tuple(zip(point1, point2))
    x = x1, x2 = zipped_points[0]
    y = y1, y2 = zipped_points[1]
    z = z1, z2 = zipped_points[2]
    rectangular_prism = figure3d(
        figure2d3d((x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2), color = colors[0]),
        figure2d3d((x1, y2, z1), (x1, y2, z2), (x2, y2, z2), (x2, y2, z1), color = colors[1]),
        figure2d3d((x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), color = colors[2]),
        figure2d3d((x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), color = colors[3]),
        figure2d3d((x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), color = colors[4]),
        figure2d3d((x1, y1, z1), (x1, y2, z1), (x2, y2, z1), (x2, y1, z1), color = colors[5])
        )
    return rectangular_prism

def _main():
    '''this acts as a mini-driver.'''
    from usefulpy.gui import Frame
    global canv, area, cam, loadingcube, cube1, cube2, cube3
    canv = Frame(width = 800, height =800).addCanvas(width = 800, height =800)
    area = space()
    
    cubefigs = (
        #I had the colors aranged in four 6*20 tables and had python
        #randomly choose the colors
        figure2d3d((-1, -1, -1),(-1, 1, -1), (-1, 1, 1), (-1, -1, 1), color = 'orange'), #touching chocolate3, green
        figure2d3d((-1,-1,-1), (-1, 1, -1), (1, 1, -1), (1, -1, -1), color = 'DarkGrey'), #bottom
        figure2d3d((-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1), color = 'chocolate3'), #touching orange, brown2
        figure2d3d((-1, 1, -1), (-1, 1, 1), (1, 1, 1), (1, 1, -1), color = 'green'), #touching brown2, orange
        figure2d3d((-1, 1, 1), (1, 1, 1), (1, -1, 1), (-1, -1, 1), color = 'YellowGreen'), #top
        figure2d3d((1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1), color = 'brown2') #touching green, chocolate3
        )
    
    loadingcube = figure3d(*cubefigs)
    #I know it doesn't need to 'load' anything
    #but it looks nice as a loading symbol.
    area.addfigure(loadingcube)
    cam = area.addcamera('cam', fov=10, thetax=60, thetaz=140)

    

    cube1 = make_rectangular_prism((2, 2, -0.5), (3, 3, 0.5), 'CadetBlue')
    cube2 = make_rectangular_prism((-1, -1, -1), (0, 0, 0), 'brown')
    cube3 = make_rectangular_prism((3, 2, 0), (4, 3, 1), 'DarkGoldenrod')
    
    #there should be pyramids, but I haven't made one.
    
    area.setview('cam')
    area.view_in_canvas(canv)
    
    
    for x in range(360):
        cam.tiltright(2)
        cam.tiltup(5)
        time.sleep(0.005)
    
    area.freezecanvas(canv)
    area.space.pop(0)
    cam.setfov(0.2)
    cam.tp((-2, -2, 0))
    cam.seth((90, -45))
    area.addfigure(cube1)
    area.addfigure(cube2)
    area.addfigure(cube3)
    area.unfreezecanvas(canv)
    time.sleep(0.1)

if __name__ == '__main__':
    import tkinter
    _main()


    



