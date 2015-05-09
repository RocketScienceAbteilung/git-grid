import functools
import numpy
import time
from ..utils import git, utils
from . import Page


class Diff(Page):
    def draw(self):
        super(Diff, self).draw()

        files = git.get_diff()
        files = utils.normalize_sum(files)

        for i, (fn, (a, b)) in enumerate(files):
            start = 1
            middle = 1 + b
            end = 1 + b + a

            self.controller.lights[i, 0] = utils.string_to_rgb(fn)[0]
            self.controller.lights[i, start:middle] = numpy.array([1, 0, 0])
            self.controller.lights[i, middle:end] = numpy.array([0, 1, 0])

    def pg_cancel(self, action, message):
        if git.do_resethard():
            self.confirm()
        self.draw()

    def pg_ok(self, action, message):
        if git.do_commit():
            self.confirm()
        self.draw()
