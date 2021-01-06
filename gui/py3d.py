'''
A frame ish thing that graphs 3d objects on a Python-wrought gui...
hopefully
Also lighting...
hopefully
'''

#Math is useful! I almost forgot it
from usefulpy.mathematics.nmath import *
degrees()

#Not sure how to make this into a frame... in fact, I didn't think this through
#I only worked out the math part in my head, checked it on desmos
# (see https://www.desmos.com/calculator/bnk7wnndk1) and ... opened the .py
# document...
#ooh! Speaking of math... fourier series! I should make something for those too,
#fourier.py, does that go in gui or math, fourier animations are fun.

#The first part is passing a 3d point into a 2d point
#The way this works (yes... this is an excuse to rant about how great math is
#the 'give an impassioned rant' button in 3b1b's website is another great excuse)
# The way this works is that you imagine a 3d vector from a point to an 'eye'
# (a point with a plane in front of it), where this vector intersects with the
#plane is the point is should be graphed at. Math is awesome.

from collections import namedtuple
Point3d = namedtuple('Point3d', ('x', 'y', 'z'))
Point2d = namedtuple('Point2d', ('x', 'y'))

class camera(object):
    def __init__(self, fov = 0.5, x = 0, y= 0, z=0, thetax = 0, thetaz= 0):
        #x, y, z, camera's coordinates
        #theta, rho camera angles
        #fov, distance of pane from point
        self.x = x
        self.y = y
        self.z = z
        
        self.thetax = thetax
        self.thetaz = thetaz
        self.fov = fov
        self._precompute()
    def _precompute(self):
        # stuff its going to use tons of times so I might as well calculate
        # now
        thetax = self.thetax
        thetaz = self.thetaz
        x, y, z = (self.x, self.y, self.z)
        #print(x, y, z)
        self.location = (x, y, z)
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

    #Rotations
    #rs (rotation section) = self.pre[n]*([d]-self.[d]3)

    def _xr(self, x, y):
        xrs1 = self.pre1*(x-self.x3)
        xrs2 = self.pre2*(y-self.y3)
        return xrs1 + xrs2

    def _yr(self, x, y, z):
        yrs1 = self.pre6*(x-self.x3)
        yrs2 = self.pre5*(y-self.y3)
        yrs3 = self.pre4*(z-self.z3)
        return yrs1 + yrs2 + yrs3

    def _zr(self, x, y, z):
        zrs1 = self.pre8*(x-self.x3)
        zrs2 = self.pre7*(y-self.y3)
        zrs3 = self.pre3*(z-self.z3)
        return zrs1 + zrs2 + zrs3

    def _xr1(self, x, y):
        xrs1 = self.pre1*(x-self.x31)
        xrs2 = self.pre2*(y-self.y31)
        return xrs1 + xrs2

    def _yr1(self, x, y, z):
        yrs1 = self.pre6*(x-self.x31)
        yrs2 = self.pre5*(y-self.y31)
        yrs3 = self.pre4*(z-self.z31)
        return yrs1 + yrs2 + yrs3

    def _zr1(self, x, y, z):
        zrs1 = self.pre8*(x-self.x31)
        zrs2 = self.pre7*(y-self.y31)
        zrs3 = self.pre3*(z-self.z31)
        return zrs1 + zrs2 + zrs3

    def _project_to_x(self, x, y, z):
        xrot = self._xr(x, y)
        zrot = self._zr(x, y, z)
        if zrot > 0: return xrot/zrot #zrot > 0 means object is behind

    def _project_to_y(self, x, y, z):
        yrot = self._yr(x, y, z)
        zrot = self._zr(x, y, z)
        if zrot > 0: return yrot/zrot #zrot > 0 means object is behind

    def _project_to_x1(self, x, y, z):
        xrot = self._xr1(x, y)
        zrot = self._zr1(x, y, z)
        return xrot/zrot

    def _project_to_y1(self, x, y, z):
        yrot = self._yr1(x, y, z)
        zrot = self._zr1(x, y, z)
        return yrot/zrot

    def project(self, point):
        #point arg should be a Point3d object.
        tx, ty, tz = point.x, point.y, point.z
        return Point2d(self._project_to_x(tx, ty, tz), self._project_to_y(tx, ty, tz))

    def project1(self, point):
        tx, ty, tz = point.x, point.y, point.z
        return Point2d(self._project_to_x1(tx, ty, tz), self._project_to_y1(tx, ty, tz))

    def tiltup(self, degrees):
        self.thetax += degrees
        self._precompute()

    def tiltdown(self, degrees):
        self.thetax -= degrees
        self._precompute()

    def tiltleft(self, degrees):
        self.thetaz += degrees
        self._precompute()

    def tiltright(self, degrees):
        self.thetaz -= degrees
        self._precompute()

    def fdx(self, amount):
        self.x += amount
        self._precompute()

    def fdy(self, amount):
        self.y += amount
        self._precompute()

    def fdz(self, amount):
        self.z += amount
        self._precompute()

    def bkx(self, amount):
        self.x -= amount
        self._precompute()

    def bky(self, amount):
        self.y -= amount
        self._precompute()

    def bkz(self, amount):
        self.z -= amount
        self._precompute()

    def fdxy(self, amount): ##Not tested
        xrat = cos(self.thetaz)
        yrat = sin(self.thetaz)
        self.x += amount*xrat
        self.y += amount*yrat
        self._precompute()

    def fdyz(self, amount): ##Not tested
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def fdzx(self, amount): ##Not tested
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x += amount*xrat
        self.z += amount*zrat
        self._precompute()

    def bkxy(self, amount): ##Not tested
        xrat = cos(self.thetaz)
        yrat = sin(self.thetaz)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self._precompute()

    def bkyz(self, amount): ##Not tested
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def bkzx(self, amount): ##Not tested
        xrat = sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.z -= amount*zrat
        self._precompute()

    def fd(self, amount): ##Not tested
        xrat = cos(self.thetaz)*sin(self.thetax)
        yrat = sin(self.thetaz)*sin(self.thetax)
        zrat = cos(self.thetax)
        self.x += amount*xrat
        self.y += amount*yrat
        self.z += amount*zrat
        self._precompute()

    def bk(self, amount): ##Not tested
        xrat = cos(self.thetaz)*sin(self.thetax)
        yrat = sin(self.thetaz)*sin(self.thetax)
        zrat = cos(self.thetax)
        self.x -= amount*xrat
        self.y -= amount*yrat
        self.z -= amount*zrat
        self._precompute()

    def __repr__(self):
        return f'<(py3d.camera at point{self.location} facing({self.thetax}, {self.thetaz})>'

    #def view(figure) #view a 3d figure #will return polygons squished into 2d


#class figure3d (a set of interconnecting 2d figures)
#class figure2d (a set of interconnecting 1d lines)
#class line_segment (a pair of points)
