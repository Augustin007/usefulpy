# minecraft-like 20 by 20 block generation
from usefulpy.gui.py3d import Simple_camera as _c
from usefulpy.gui import Frame as _frame
import cProfile
import pstats

Space = _c.space()
canv = _frame(width=800, height=800).addCanvas(width=800, height=800)
cam = _c.simple_camera(Space, _c.quaternion(), _c.i)
cam.add_canvas(canv)

_c.light_scource = (2*_c.i+_c.j+5*_c.k).normal()


def make_block(x, y, z, color):
    pointa = _c.quaternion(0, x, y, z)
    pointb = _c.quaternion(0, x+1, y+1, z+1)
    return _c.make_rectangular_prism(Space, pointa, pointb, color)


brown = (177, 124, 83)
green = (133, 183, 98)
height = 2
world = []
f = lambda x, y: int(_c._m.cos(abs(complex(x, y)))+_c._m.cos(_c._m.cos(x)+_c._m.sin(y))+2)
count = 0
for x in range(-10, 10):
    for y in range(-10, 10):
        height = f(x, y)
        color = brown
        for z in range(height):
            count += 1
            if height == z+1:
                color = green
            world.append(make_block(x, y, z, color))

with cProfile.Profile() as pr:
    cam.up(4)
    cam.spin_dn(_c._m.tau/3, smooth=False)


stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()

print(count)
