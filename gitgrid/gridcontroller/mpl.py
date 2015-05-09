import mido
import matplotlib.pyplot as plt
from . import GridController, lights, buttons


class mockinput(object):
    def __init__(self, *args):
        self.callback = None


class Matplotlib(GridController):
    def __init__(self, input=None, output=None):
        input = mockinput()
        output = mockinput()

        self.lights = lights((8, 8))
        self.buttons = buttons((8, 8))

        self.plot = plt.imshow(self.lights, interpolation='nearest')
        cid = self.plot.figure.canvas.mpl_connect('button_press_event', self.button_pressed)
        cid = self.plot.figure.canvas.mpl_connect('key_press_event', self.button_pressed)
        plt.draw()

        super(Matplotlib, self).__init__(input, output)
        self.run_scheduler = False

    def iter_changed(self, *args):
        self.plot.set_data(self.lights)
        plt.draw()
        super(Matplotlib, self).iter_changed(*args)

    def on_action(self, event):
        if not hasattr(event, 'key'):
            return

        if event.key == 'enter':
            return 'ok'
        elif event.key in ('backspace', 'escape'):
            return 'cancel'
        elif event.key in ('up', 'down', 'left', 'right'):
            return event.key
        elif event.key in ('1', '2', '3', '4'):
            return 'tab' + event.key
        else:
            return

    def on_tap(self, event):
        return round(event.ydata), round(event.xdata)

    def loop(self):
        plt.show()
