import numpy
import argparse
import time
import mido
import colorsys
import gitgrid.gridcontroller
import gitgrid.utils.utils

args = gitgrid.utils.utils.controller_args()
tmp = gitgrid.gridcontroller.create(args.controller, args.input, args.output)


def toggle(x, y, Message):
    curr = tmp.lights[x, y, :] / 255.
    hsv = list(colorsys.rgb_to_hsv(*curr))
    hsv[0] += 0.1
    tmp.lights[x, y, :] = numpy.array(colorsys.hsv_to_rgb(*hsv)) * 255.


def foo(action, message):
    print action


tmp.lights[:, :] = numpy.array([1, 0, 0])
tmp.buttons[:, :] = toggle

tmp.actions = {
    'up': foo,
    'down': foo,
    'left': foo,
    'right': foo,
    'tab1': foo,
    'tab2': foo,
    'tab3': foo,
    'tab4': foo,
    'ok': foo,
    'cancel': foo,
}

tmp.loop()
