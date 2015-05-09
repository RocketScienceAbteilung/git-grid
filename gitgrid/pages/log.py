import functools
import numpy
from ..utils import git, utils
from . import Page


class Log(Page):
    def draw(self):
        super(Log, self).draw()

        log = git.parse_log(git.get_log(self.page * 8), 8)
        head = git.get_current_commit()
        graph_width = max(git.parse_tree_width(log))

        img = [
            (
                git.parse_tree((h, g), fill=graph_width + 1) +
                utils.hash_to_rgb(h)
            )[:8] for h, g in log
        ]

        self.controller.lights[:len(img), :, :] = numpy.array(img)

        def checkout(a, b, c, name=None):
            if not git.do_checkout(name):
                self.error()
            self.draw()

        for i, (h, _) in enumerate(log):
            self.controller.buttons[i, :] = functools.partial(
                checkout,
                name=h
            )
