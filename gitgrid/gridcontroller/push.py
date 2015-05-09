import mido
import numpy as np
from . import GridController, lights, buttons


class Push(GridController):

    pad_offset = 36
    color_table = np.array([
        (0, 0, 0),
        (30, 30, 30),
        (127, 127, 127),
        (255, 255, 255),
        (255, 76, 76),
        (255, 0, 0),
        (89, 0, 0),
        (25, 0, 0),
        (255, 189, 108),
        (255, 84, 0),
        (89, 29, 0),
        (39, 27, 0),
        (255, 255, 76),
        (255, 255, 0),
        (89, 89, 0),
        (25, 25, 0),
        (136, 255, 76),
        (84, 255, 0),
        (29, 89, 0),
        (20, 43, 0),
        (76, 255, 76),
        (0, 255, 0),
        (0, 89, 0),
        (0, 25, 0),
        (76, 255, 94),
        (0, 255, 25),
        (0, 89, 13),
        (0, 25, 2),
        (76, 255, 136),
        (0, 255, 85),
        (0, 89, 29),
        (0, 31, 18),
        (76, 255, 183),
        (0, 255, 153),
        (0, 89, 53),
        (0, 25, 18),
        (76, 195, 255),
        (0, 169, 255),
        (0, 65, 82),
        (0, 16, 25),
        (76, 136, 255),
        (0, 85, 255),
        (0, 29, 89),
        (0, 8, 25),
        (76, 76, 255),
        (0, 0, 255),
        (0, 0, 89),
        (0, 0, 25),
        (135, 76, 255),
        (84, 0, 255),
        (25, 0, 100),
        (15, 0, 48),
        (255, 76, 255),
        (255, 0, 255),
        (89, 0, 89),
        (25, 0, 25),
        (255, 76, 135),
        (255, 0, 84),
        (89, 0, 29),
        (34, 0, 19),
        (255, 21, 0),
        (153, 53, 0),
        (121, 81, 0),
        (67, 100, 0),
        (3, 57, 0),
        (0, 87, 53),
        (0, 84, 127),
        (0, 0, 255),
        (0, 69, 79),
        (37, 0, 204),
        (127, 127, 127),
        (32, 32, 32),
        (255, 0, 0),
        (189, 255, 45),
        (175, 237, 6),
        (100, 255, 9),
        (16, 139, 0),
        (0, 255, 135),
        (0, 169, 255),
        (0, 42, 255),
        (63, 0, 255),
        (122, 0, 255),
        (178, 26, 125),
        (64, 33, 0),
        (255, 74, 0),
        (136, 225, 6),
        (114, 255, 21),
        (0, 255, 0),
        (59, 255, 38),
        (89, 255, 113),
        (56, 255, 204),
        (91, 138, 255),
        (49, 81, 198),
        (135, 127, 233),
        (211, 29, 255),
        (255, 0, 93),
        (255, 127, 0),
        (185, 176, 0),
        (144, 255, 0),
        (131, 93, 7),
        (57, 43, 0),
        (20, 76, 16),
        (13, 80, 56),
        (21, 21, 42),
        (22, 32, 90),
        (105, 60, 28),
        (168, 0, 10),
        (222, 81, 61),
        (216, 106, 28),
        (255, 225, 38),
        (158, 225, 47),
        (103, 181, 15),
        (30, 30, 48),
        (220, 255, 107),
        (128, 255, 189),
        (154, 153, 255),
        (142, 102, 255),
        (64, 64, 64),
        (117, 117, 117),
        (224, 255, 255),
        (160, 0, 0),
        (53, 0, 0),
        (26, 208, 0),
        (7, 66, 0),
        (185, 176, 0),
        (63, 49, 0),
        (179, 95, 0),
        (75, 21, 2),
    ])

    def __init__(self, input=None, output=None):
        if input is None:
            try:
                input = mido.open_input(
                    'Ableton Push User Port',
                    callback=True)
            except IOError:
                input = mido.open_input('Ableton Push MIDI 2', callback=True)
        if output is None:
            try:
                output = mido.open_output('Ableton Push User Port')
            except IOError:
                output = mido.open_output('Ableton Push MIDI 2')

        self.lights = lights((8, 8))
        self.buttons = buttons((8, 8))

        super(Push, self).__init__(input, output)

    def color(self, r, g, b):
        value = np.array([r, g, b])
        idx = np.abs(
            np.linalg.norm(self.color_table - value * 255., axis=1)
        ).argmin()
        return idx

    def update(self, x, y, value):
        x = 7 - x
        note = self.pad_offset + y + (x * 8)
        velocity = self.color(*value)

        self.output.send(
            mido.Message('note_on', note=note, velocity=velocity)
        )

    def on_action(self, message):
        lookup = {
            46: 'up',
            47: 'down',
            44: 'left',
            45: 'right',
            106: 'tab1',
            107: 'tab2',
            108: 'tab3',
            109: 'tab4',
        }

        if message.type == 'control_change' and message.value == 127:
            try:
                return lookup[message.control]
            except KeyError:
                return

    def on_tap(self, message):
        if message.type == 'note_on':
            note = message.note - self.pad_offset
            row = note // 8
            col = note % 8
            row = 7 - row
        else:
            return

        return row, col
