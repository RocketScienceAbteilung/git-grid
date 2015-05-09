import numpy
import time


class Page(object):
    def __init__(self, controller):
        self.controller = controller
        self.page = 0

    def activate(self):
        self.page = 0
        self.controller.actions['up'] = self.pg_up
        self.controller.actions['down'] = self.pg_down
        self.controller.actions['left'] = self.pg_left
        self.controller.actions['right'] = self.pg_right
        self.controller.actions['ok'] = self.pg_ok
        self.controller.actions['cancel'] = self.pg_cancel

        self.controller.buttons[:, :] = None
        self.controller.lights[:, :] = numpy.array((0, 0, 0))
        self.draw()

    def draw(self):
        self.controller.lights[:, :] = numpy.array((0, 0, 0))

    def pg_up(self, action, message):
        self.page -= 1
        if self.page < 0:
            self.error()
            self.page = 0
        self.draw()

    def pg_down(self, action, message):
        self.page += 1
        self.draw()

    def pg_left(self, action, message):
        pass

    def pg_right(self, action, message):
        pass

    def pg_ok(self, action, message):
        pass

    def pg_cancel(self, action, message):
        pass

    def flash(self, color):
        prevlights = self.controller.lights[:, :, :]
        self.controller.lights[:, :, :] = numpy.array(color)
        time.sleep(0.2)
        self.controller.lights[:, :, :] = prevlights

    def error(self):
        self.flash((1, 0, 0))

    def confirm(self):
        self.flash((0, 1, 0))
