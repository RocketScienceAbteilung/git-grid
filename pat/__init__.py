import fileinput
import mido


def main(argv=None):
    try:
        output = mido.open_output('Ableton Push User Port')
    except IOError:
        output = mido.open_output('Ableton Push MIDI 2')

    for outline, line in enumerate(fileinput.input()):
        outline = outline % 4

        if len(line.strip()):
            line = line[:-1].ljust(68)
            line = (line[:66] + '..') if len(line) > 68 else line
            data = [71, 127, 21, 24+outline, 0, 69, 0] + map(ord, line)

            output.send(
                mido.Message('sysex', data=data)
            )
