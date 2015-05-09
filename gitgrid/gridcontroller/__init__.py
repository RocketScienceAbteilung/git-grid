from __future__ import division
import threading
import time
import numpy


class GridControllerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.quit = False

    def run(self):
        self.i = 0
        while True:
            if self.quit:
                return

            # TODO: Put repeating logic here.
            # Put reusable subtasks in their own methods/files/modules

            # All data meant for the application should be saved in an
            # attribute of this class.

            # All mode-sets, calls and other interactions from application
            # should be declared as methods of this object.

            time.sleep(0.001)


class grid(numpy.ndarray):
    def __new__(cls, *args, **kwargs):
        return numpy.ndarray.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self._observers = {
            'change': [],
        }

    def __setitem__(self, *args):
        super(grid, self).__setitem__(*args)
        self.trigger('change', *args)

    def trigger(self, key, *args):
        for i in self._observers[key]:
            i(*args)

    def on(self, key, callback):
        self._observers[key].append(callback)

    def off(self, key):
        del self._observers[key][:]


class lights(grid):
    def __new__(cls, shape=None, *args, **kwargs):
        return numpy.ndarray.__new__(
            cls,
            shape=shape + (3,),
            dtype=float,
            *args,
            **kwargs
        )


class buttons(grid):
    def __new__(cls, shape=None, *args, **kwargs):
        return numpy.ndarray.__new__(
            cls,
            shape=shape,
            dtype=object,
            *args,
            **kwargs
        )


class GridController(object):
    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output

        self.prev_lights = self.lights.copy()
        numpy.copyto(self.prev_lights, self.lights)

        self.lights.on('change', self.iter_changed)
        self.input.callback = self.button_pressed
        self.run_scheduler = True

        self.actions = {
            'up': None,
            'down': None,
            'left': None,
            'right': None,
            'tab1': None,
            'tab2': None,
            'tab3': None,
            'tab4': None,
        }

    def button_pressed(self, message):
        # See if button was an action
        action = self.on_action(message)
        try:
            if action and self.actions[action]:
                return self.actions[action](action, message)
        except KeyError:
            pass

        # Button was not an action but on grid
        button = self.on_tap(message)
        if button:
            row, col = button

            if self.buttons[row, col]:
                return self.buttons[row, col](row, col, message)

    def iter_changed(self, *args):
        """
        Find all changed values and iterate over those.
        Does not update the grid when you only change one value

        """
        # Searches for any changed value but only gives the x, y coordinates
        # of a 3D tensor (3rd dimension are RGB values)
        ch = numpy.where(numpy.any(self.lights != self.prev_lights, axis=2))
        for (x, y), value in zip(zip(*ch), self.lights[ch]):
            self.update(x, y, value)

        # update prev_lights to be in sync with lights again
        numpy.copyto(self.prev_lights, self.lights)

    def update(self, x, y, value):
        """
        Overload this method with your device-specific logic.

        """
        pass

    def on_action(self, message):
        """
        Overload this method with your device-specific logic.

        """
        pass

    def on_tap(self, message):
        """
        Overload this method with your device-specific logic.

        """
        pass

    def loop(self):
        while True:
            time.sleep(0.1)


def create(name, *args):
    if name.lower() in ("push"):
        from . import push
        return push.Push(*args)
    elif name.lower() in ("launchpad", "launchpad mini", "lmp"):
        from . import launchpad
        return launchpad.Launchpad(*args)
    elif name.lower() in ("launchpads", "launchpad s", "lp", "lps"):
        from . import launchpad
        return launchpad.LaunchpadS(*args)
    elif name.lower() in ("matplotlib", "mpl"):
        from . import mpl
        return mpl.Matplotlib(*args)
    else:
        raise ValueError("Gridcontroller %s not found" % name)
