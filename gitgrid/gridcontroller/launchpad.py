import mido
from . import GridController, lights, buttons


class Launchpad(GridController):
    def __init__(self, input=None, output=None):
        if input is None:
            try:
                input = mido.open_input('Launchpad Mini', callback=True)
            except IOError:
                input = mido.open_input('Launchpad Mini MIDI 1', callback=True)
        if output is None:
            try:
                output = mido.open_output('Launchpad Mini')
            except IOError:
                output = mido.open_output('Launchpad Mini MIDI 1')

        self.lights = lights((8, 8))
        self.buttons = buttons((8, 8))

        super(Launchpad, self).__init__(input, output)

    def color(self, r, g, b):
        return map(lambda x: int(round(x * 3)), [r, g, b])

    def update(self, x, y, value):
        red, green, _ = self.color(*value)
        velocity = 16 * green + red + 8 + 4

        # Catch invalid buttons
        if x == 0 and y == 8:
            return

        # First row is changed with control_change
        if x == -1:
            control = 104 + y
            self.output.send(
                mido.Message(
                    'control_change',
                    control=control,
                    value=velocity
                )
            )
        # All other rows are changed with notes
        else:
            note = x * 16 + y
            self.output.send(
                mido.Message('note_on', note=note, velocity=velocity)
            )

    def on_action(self, message):
        lookup = {
            104: 'up',
            105: 'down',
            106: 'left',
            107: 'right',
            108: 'tab1',
            109: 'tab2',
            110: 'tab3',
            111: 'tab4',
        }

        if message.type == 'control_change' and message.value == 127:
            try:
                return lookup[message.control]
            except KeyError:
                return

    def on_tap(self, message):
        if message.type == 'note_on' and message.velocity == 127:
            row = message.note // 16
            col = message.note % 16
            if col >= 8:
                return
        else:
            return

        return row, col


class LaunchpadS(Launchpad):
    def __init__(self, input=None, output=None):
        if input is None:
            try:
                input = mido.open_input('Launchpad S', callback=True)
            except IOError:
                input = mido.open_input('Launchpad S MIDI 1', callback=True)
        if output is None:
            try:
                output = mido.open_output('Launchpad S')
            except IOError:
                output = mido.open_output('Launchpad S MIDI 1')

        super(LaunchpadS, self).__init__(input, output)
