from gl import Render, color
from obj import Obj, Texture
import ops as op
from shaders import *

import random

r = Render(1000,1000)

r.active_texture = Texture('./models/grass.bmp')
r.active_texture2 = Texture('./models/grass.bmp')

r.active_shader = sombreadoCool

luz = (1,0,1)
r.light = op.divide(luz , op.norm(luz))

r.loadModel('./models/earth.obj', (500,500,0), (1,1,1))

r.glFinish('output.bmp')





