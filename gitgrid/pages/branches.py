import functools
import numpy
from ..utils import git, utils
from . import Page


class Branches(Page):
    def draw(self):
        super(Branches, self).draw()

        branches = git.get_branches(self.page * 8)
        head = git.get_current_branch()
        files = git.get_between(branches)
        files = utils.normalize_single(files)

        if not files and self.page > 0:
            self.page -= 1
            self.error()
            self.draw()
            return

        center = 3
        for i, (fn, (a, b)) in enumerate(files):
            start = center - a
            end = center + b

            if fn == head:
                self.controller.lights[i, center] = numpy.array([1, 1, 1])
                self.controller.lights[i, center+1] = numpy.array([0, 0, 0])
            else:
                self.controller.lights[i, center] = utils.string_to_rgb(fn)[0]
                if git.get_can_merge_ff(fn):
                    self.controller.lights[i, -1] = numpy.array([0, 1, 0])
                elif git.get_can_merge(fn):
                    self.controller.lights[i, -1] = numpy.array([1, 1, 0])
                else:
                    self.controller.lights[i, -1] = numpy.array([1, 0, 0])
            self.controller.lights[i, start:center] = numpy.array([1, 0, 0])
            self.controller.lights[i, center+1:end+1] = numpy.array([0, 1, 0])

        def new_branch(*args):
            if not git.do_new_branch():
                self.error()
            self.draw()

        def checkout(a, b, c, name=None):
            if not git.do_checkout(name):
                self.error()
            self.draw()

        def merge(a, b, c, name=None):
            if not git.do_merge(name):
                self.error()
            self.draw()

        for i, (fn, _) in enumerate(files):
            self.controller.buttons[i, center] = functools.partial(
                checkout,
                name=fn
            )
            self.controller.buttons[i, -1] = functools.partial(
                merge,
                name=fn
            )

        self.controller.buttons[len(files), center] = new_branch
