### IMPORTS ###
import time
__author__ = 'Austin Garcia'
__version__ = '3.1.1'
__package__ = 'usefulpy.gui.py3d'

from ...mathematics import nmath as _m
from ... import validation as _validation
from .Cam import cam_base
import tkinter

### SPACE ###
class space:
    '''Spaces store information about canvases, cameras, and figures'''
    cam_bases  = [cam_base]
    def __init__(self):
        '''init for space class, a space's data is added separately.'''
        self.space = []
        self.cameras = []
        self._space_updated = True

    def addcamera(self, cam):
        '''Adds a camera to the space'''
        if isinstance(cam, tuple(self.cam_bases)):
            self.cameras.append(cam)
            return
        raise TypeError('Invalid camera type')

    def addfigure(self, figure):
        '''adds a figure to the space'''
        self.space.append(figure)
        return figure

    def setview(self, to):
        '''set a default view for the space'''
        if isinstance(to, tuple(self.cam_bases)):
            if to.universe != self: raise ValueError(f'{to} not in this universe')
            self.view = to
            return
        raise TypeError(f'{to} should be a valid camera type')

    def view_in_canvas(self, at):
        '''view from default view at a canvas 'at' '''
        if self.view is None: raise NameError('self.view is not defined')
        self.view.add_canvas(at)

    def _recieve_update_msg(self, from_):
        for cam in self.cameras:
            if cam is not from_:
                cam._update_msg()
        self._space_updated = False

    def _space_update_msg(self, from_):
        self._space_updated = True

    def _update(self, canv):
        if canv not in self.runningCanvases: raise ValueError
        cam = self.runningCanvases[canv]
        self._view_from(cam, canv)
        canv.update()

    def view_from(self, cam, at):
        '''view from cam at a canvas 'at' '''
        if isinstance(cam, tuple(self.cam_bases)):
            if cam.universe != self: raise ValueError(f'{cam} not in this universe')
            cam.add_canvas(at)
            return
        raise TypeError(f'{cam} should be a valid camera type')

    def remove_fig(self, fig):
        index = self.space.index(fig)
        fig.universe = None
        return self.space.pop(index)

    def __iter__(self):
        '''__iter__ for space... goes through all items in the space.'''
        return self.space.__iter__()
