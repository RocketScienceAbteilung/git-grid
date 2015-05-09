import fileinput
import mido
import collections
import sys


def main(argv=None):
    try:
        output = mido.open_output('Ableton Push User Port')
    except IOError:
        output = mido.open_output('Ableton Push MIDI 2')

    lines = collections.deque(['', '', '', ''])

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        lines.append(line)
        lines.popleft()

        for i, bufline in enumerate(lines):
            bufline = bufline[:-1].ljust(68)
            bufline = (bufline[:66] + '..') if len(bufline) > 68 else bufline

            data = [71, 127, 21, 24+i, 0, 69, 0] + map(ord, bufline)

            output.send(
                mido.Message('sysex', data=data)
            )
