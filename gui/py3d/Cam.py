__package__ = 'usefulpy.gui.py3d'
from ...mathematics import nmath as _m
from ...mathematics.quaternion import quaternion, i, j, k
import time
import functools

def cam_shape_method(func):
    @functools.wraps(func)
    def cam_method_wrapper(cam, *args, **kwargs):
        rval = func(cam, *args, **kwargs)
        if cam.shape is not None: exec('cam.shape.{func.__name__}(*args, **kwargs)')
        cam._update()
        return rval
    return cam_method_wrapper

class cam_base:
    #this is base class for a camera
    def __init__(self, universe, position, heading, renderdistance = 12, personal_objects = None):
        if not type(position) is quaternion:
            raise TypeError('argument \'position\' should be a quaternion type')
        if not type(heading) is quaternion:
            raise TypeError('argument \'heading\' should be a quaternion type')
        if position.real:
            raise ValueError('argument \'position\' should not have a real part')        
        if heading.real:
            raise ValueError('argument \'heading\' should not have a real part')
        self.Canvases = []
        self.position = position
        self.heading = heading.normal()
        self.universe = universe
        self.personal_objects = personal_objects
        self.renderdistance = float(renderdistance)
        self.spnspeed = (1, 0.0025) #(radians, seconds) = radians per seconds
        self.movspeed = (0.1, 0.01) #(grid_coordinates, seconds) = grid_coordinates per seconds
        self.is_visible = False
        self.shape = None
        self.running_canvases = []
        self.frozen_canvases = []
        self.is_frozen = False
        self.universe.addcamera(self)
        self._compute
        self.lighting_dict={}

    def freeze(self):
        self.is_frozen = True

    def unfreeze(self):
        self.is_frozen = False
        self._update()
    
    def _compute(self):
        pass

    def _update(self):
        if self.is_frozen: return
        self._update_msg()
        self.universe._recieve_update_msg(self)

    def _update_msg(self):
        if self.is_frozen: return
        self._compute()
        self._update_view()

    def project(self, object):
        pass

    def _update_view(self):
        if self.is_frozen: return
        tempspace = self.universe.space.copy()
        distances = [abs(self.position-fig.pos) for fig in tempspace]
        if not self.running_canvases: return
        for canvas in self.running_canvases:
            canvas.delete('all')
        while tempspace:
            distance = max(distances)
            figindex = distances.index(distance)
            fig = tempspace.pop(figindex)
            distances.pop(figindex)
            if distance < self.renderdistance:
                if fig is not self:
                    self.project(fig)
        ##if self.personal_objects: pass #TODO: Personal objects not yet implimented
        for canvas in self.running_canvases:
            canvas.update()

    def add_canvas(self, canvas):
        state = 'running'
        if hasattr(canvas, 'linked'):
            canvas.linked.pop(canvas)
            state = canvas.state
        self.running_canvases.append(canvas)
        canvas.linked = self
        self._update()
        if state != 'running': self.freezecanvas(canvas)
        

    def freezecanvas(self, canvas):
        '''freezes 3d updates to a canvas'''
        if canvas in self.running_canvases:
            index = self.running_canvases.index(canvas)
            self.frozen_canvases.append(self.running_canvases.pop(index))
            canvas.state = 'frozen'
            return
        raise ValueError(f'canvas {canvas} is not displaying this camera.')

    def unfreezecanvas(self, canvas):
        if canvas in self.frozen_canvases:
            index = self.frozen_canvases.index(canvas)
            self.running_canvases.append(self.frozen_canvases.pop(index))
            self._update()
            canvas.state = 'running'
            return
        raise ValueError(f'canvas {canvas} is not displaying this camera.')

    def pop(self, canvas):
        if canvas in self.running_canvases:
            index = self.running_canvases.index(canvas)
            canvas.delete('all')
            return self.running_canvases.pop(index)
        elif canvas in self.frozen_canvases:
            index = self.frozen_canvases.index(canvas)
            canvas.delete('all')
            return self.frozen_canvases.pop(index)
        raise ValueError(f'canvas {canvas} is not displaying this camera.')

    @cam_shape_method
    def rotate(self, rad, normal, point = None):
        self.heading = self.heading.rotate(rad, normal, quaternion())
        if point is not None:
            self.position = self.position.rotate(rad, normal, point)

    @cam_shape_method
    def shift(self, by):
        self.position = self.position+by

    @cam_shape_method
    def _tilt_up(self, rad):
        a, b, c = self.heading.vtuple()
        θ = _m.atan2(b, a)
        Φ = _m.atan2(c, _m.hypot(a, b))
        Φ += rad
        self.heading = quaternion(0, _m.cos(θ)*_m.cos(Φ), _m.sin(θ)*_m.cos(Φ), _m.sin(Φ))

    @cam_shape_method
    def _tilt_dn(self, rad):
        a, b, c = self.heading.vtuple()
        θ = _m.atan2(b, a)
        Φ = _m.atan2(c, _m.hypot(a, b))
        Φ -= rad
        self.heading = quaternion(0, _m.cos(θ)*_m.cos(Φ), _m.sin(θ)*_m.cos(Φ), _m.sin(Φ))

    @cam_shape_method
    def _tilt_rt(self, rad):
        a, b, c = self.heading.vtuple()
        θ = _m.atan2(b, a)
        Φ = _m.atan2(c, _m.hypot(a, b))
        θ += rad
        self.heading = quaternion(0, _m.cos(θ)*_m.cos(Φ), _m.sin(θ)*_m.cos(Φ), _m.sin(Φ))

    @cam_shape_method
    def _tilt_lt(self, rad):
        a, b, c = self.heading.vtuple()
        θ = _m.atan2(b, a)
        Φ = _m.atan2(c, _m.hypot(a, b))
        θ -= rad
        self.heading = quaternion(0, _m.cos(θ)*_m.cos(Φ), _m.sin(θ)*_m.cos(Φ), _m.sin(Φ))

    @cam_shape_method
    def _fdx(self, m):
        self.position += m*i

    @cam_shape_method
    def _fdy(self, m):
        self.position += m*j

    @cam_shape_method
    def _fdz(self, m):
        self.position += m*k

    @cam_shape_method
    def _bkx(self, m):
        self.position -= m*i

    @cam_shape_method
    def _bky(self, m):
        self.position -= m*j

    @cam_shape_method
    def _bkz(self, m):
        self.position -= m*k

    @cam_shape_method
    def _fdxy(self, m):
        xy_heading = (self.heading - self.heading.k*k).normal()
        self.position += m*xy_heading

    @cam_shape_method
    def _fdyz(self, m):
        yz_heading = (self.heading - self.heading.i*i).normal()
        self.position -= m*yz_heading

    @cam_shape_method
    def _fdzx(self, m):
        zx_heading = (self.heading - self.heading.j*j).normal()
        self.position += m*zx_heading

    @cam_shape_method
    def _bkzx(self, m):
        zx_heading = (self.heading - self.heading.j*j).normal()
        self.position -= m*zx_heading

    @cam_shape_method
    def _bkxy(self, m):
        xy_heading = (self.heading - self.heading.k*k).normal()
        self.position -= m*xy_heading

    @cam_shape_method
    def _bkyz(self, m):
        yz_heading = (self.heading - self.heading.i*i).normal()
        self.position -= m*yz_heading

    @cam_shape_method
    def _rt(self, m):
        xy_heading = (self.heading - self.heading.k*k).normal()
        xy_heading_rt = quaternion(0, -xy_heading.j, xy_heading.i)
        self.position += m*xy_heading_rt

    @cam_shape_method
    def _lt(self, m):
        xy_heading = (self.heading - self.heading.k*k).normal()
        xy_heading_lt = quaternion(0, xy_heading.j, -xy_heading.i)
        self.position += m*xy_heading_lt

    @cam_shape_method
    def _up(self, m):
        self.position += m*k

    @cam_shape_method
    def _dn(self, m):
        self.position -= m*k

    @cam_shape_method
    def tp(self, to):
        self.position = to.v()

    @cam_shape_method
    def seth(self, to):
        self.heading = to.normalize()

    @cam_shape_method
    def _fd(self, m):
        self.position += m*self.heading

    @cam_shape_method
    def _bk(self, m):
        self.position -= m*self.heading

    @cam_shape_method
    def setx(self, to):
        a, b, c = self.position.vtuple()
        self.position = quaternion(0, to, b, c)

    @cam_shape_method
    def sety(self, to):
        a, b, c = self.position.vtuple()
        self.position = quaternion(0, a, to, c)

    @cam_shape_method
    def setz(self, to):
        a, b, c = self.position.vtuple()
        self.position = quaternion(0, a, b, to)

    def _spin_rt(self, m, speed):
        a, b = speed
        spin, final = divmod(m, a)
        for x in range(int(spin)):
            self._tilt_rt(a)
            time.sleep(b)
        self._tilt_rt(final)

    def _spin_lt(self, m, speed):
        a, b = speed
        spin, final = divmod(m, a)
        for x in range(int(spin)):
            self._tilt_lt(a)
            time.sleep(b)
        self._tilt_lt(final)

    def _spin_up(self, m, speed):
        a, b = speed
        spin, final = divmod(m, a)
        for x in range(int(spin)):
            self._tilt_up(a)
            time.sleep(b)
        self._tilt_up(final)

    def _spin_dn(self, m, speed):
        a, b = speed
        spin, final = divmod(m, a)
        for x in range(int(spin)):
            self._tilt_dn(a)
            time.sleep(b)
        self._tilt_dn(final)

    def spin_up(self, m, *, speed = None, smooth = True):
        if not smooth: return self._tilt_up(m)
        if speed is None: speed = self.spnspeed
        return self._spin_up(m, speed)

    def spin_dn(self, m, *, speed = None, smooth = True):
        if not smooth: return self._tilt_dn(m)
        if speed is None: speed = self.spnspeed
        return self._spin_dn(m, speed)

    def spin_rt(self, m, *, speed = None, smooth = True):
        if not smooth: return self._tilt_rt(m)
        if speed is None: speed = self.spnspeed
        return self._spin_rt(m, speed)

    def spin_lt(self, m, *, speed = None, smooth = True):
        if not smooth: return self._tilt_lt(m)
        if speed is None: speed = self.spnspeed
        return self._spin_lt(m, speed)

    ### USE ###
    def __repr__(self):
        '''__repr__ for cam'''
        return f'<py3d._camera at {self.pos}, facing: ({self.thetax}, {self.thetaz}), field of vision (fov): {self.fov}, render distance: {self.renderdistance}>'

    def __iter__(self):
        '''__iter__ for cam'''
        if self.shape: return self.shape.__iter__()
        return ().__iter__()

    def _mvfd(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fd(a)
            time.sleep(b)
        self._fd(fm)

    def _mvdn(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._dn(a)
            time.sleep(b)
        self._dn(fm)

    def _mvfdz(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdz(a)
            time.sleep(b)
        self._fdz(fm)

    def _mvbkxy(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bkxy(a)
            time.sleep(b)
        self._bkxy(fm)

    def _mvbkyz(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bkyz(a)
            time.sleep(b)
        self._bkyz(fm)

    def _mvfdy(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdy(a)
            time.sleep(b)
        self._fdy(fm)

    def _mvfdxy(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdxy(a)
            time.sleep(b)
        self._fdxy(fm)

    def _mvbkz(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bkz(a)
            time.sleep(b)
        self._bkz(fm)

    def _mvfdzx(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdzx(a)
            time.sleep(b)
        self._fdzx(fm)

    def _mvlt(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._lt(a)
            time.sleep(b)
        self._lt(fm)

    def _mvbk(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bk(a)
            time.sleep(b)
        self._bk(fm)

    def _mvbky(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bky(a)
            time.sleep(b)
        self._bky(fm)

    def _mvfdyz(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdyz(a)
            time.sleep(b)
        self._fdyz(fm)
        
    def _mvup(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._up(a)
            time.sleep(b)
        self._up(fm)
        
    def _mvbkzx(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bkzx(a)
            time.sleep(b)
        self._bkzx(fm)
        
    def _mvrt(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._rt(a)
            time.sleep(b)
        self._rt(fm)
        
    def _mvfdx(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._fdx(a)
            time.sleep(b)
        self._fdx(fm)

    def _mvbkx(self, m, speed):
        a, b = speed
        mm, fm = divmod(m, a)
        for x in range(int(mm)):
            self._bkx(a)
            time.sleep(b)
        self._bkx(fm)

    def fd(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fd(m)
        if speed is None: speed = self.movspeed
        return self._mvfd(m, speed)

    def dn(self, m, *, speed = None, smooth = True):
        if not smooth: return self._dn(m)
        if speed is None: speed = self.movspeed
        return self._mvdn(m, speed)
        
    def fdz(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdz(m)
        if speed is None: speed = self.movspeed
        return self._mvfdz(m, speed)
        
    def bkxy(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bkxy(m)
        if speed is None: speed = self.movspeed
        return self._mvbkxy(m, speed)
        
    def bkyz(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bkyz(m)
        if speed is None: speed = self.movspeed
        return self._mvbkyz(m, speed)
        
    def fdy(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdy(m)
        if speed is None: speed = self.movspeed
        return self._mvfdy(m, speed)
        
    def fdxy(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdxy(m)
        if speed is None: speed = self.movspeed
        return self._mvfdxy(m, speed)
        
    def bkz(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bkz(m)
        if speed is None: speed = self.movspeed
        return self._mvbkz(m, speed)
        
    def fdzx(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdzx(m)
        if speed is None: speed = self.movspeed
        return self._mvfdzx(m, speed)
        
    def lt(self, m, *, speed = None, smooth = True):
        if not smooth: return self._lt(m)
        if speed is None: speed = self.movspeed
        return self._mvlt(m, speed)
        
    def bk(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bk(m)
        if speed is None: speed = self.movspeed
        return self._mvbk(m, speed)
        
    def bky(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bky(m)
        if speed is None: speed = self.movspeed
        return self._mvbky(m, speed)
        
    def fdyz(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdyz(m)
        if speed is None: speed = self.movspeed
        return self._mvfdyz(m, speed)
        
    def up(self, m, *, speed = None, smooth = True):
        if not smooth: return self._up(m)
        if speed is None: speed = self.movspeed
        return self._mvup(m, speed)
        
    def bkzx(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bkzx(m)
        if speed is None: speed = self.movspeed
        return self._mvbkzx(m, speed)
        
    def rt(self, m, *, speed = None, smooth = True):
        if not smooth: return self._rt(m)
        if speed is None: speed = self.movspeed
        return self._mvrt(m, speed)
        
    def fdx(self, m, *, speed = None, smooth = True):
        if not smooth: return self._fdx(m)
        if speed is None: speed = self.movspeed
        return self._mvfdx(m, speed)
        
    def bkx(self, m, *, speed = None, smooth = True):
        if not smooth: return self._bkx(m)
        if speed is None: speed = self.movspeed
        return self._mvbkx(m, speed)

    def spinto(self, to): return NotImplemented #spin to face an angle
    def spin(self, amount): return NotImplemented #spin in multiple directions at once
    def goto(self, to): return NotImplemented 
    def gotowards(self, towards): return NotImplemented 
    def followpath(self, towards): return NotImplemented 
    def slidefov(self, to): return NotImplemented #slides fov
    def spintoface(self, point): return NotImplemented #spin to face a point
        
