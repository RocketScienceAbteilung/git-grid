import fileinput
import mido
import collections
import sys
import time
import itertools
import argparse

scrollwheel = 0
buflen = 80
lines = collections.deque([''] * buflen)


def callback(message):
    global scrollwheel, buflen

    if message.type == 'pitchwheel' and message.pitch != 0:
        pitch = (message.pitch + 2. ** 13) / 2. ** 14  # percentage
        scrollwheel = min(buflen - 4, int(buflen * pitch))  # out of bounds
        redraw()
    elif message.type == 'pitchwheel' and message.pitch == 0:
        scrollwheel = 0
        redraw()


try:
    output = mido.open_output('Ableton Push User Port')
    input = mido.open_input('Ableton Push User Port', callback=callback)
except IOError:
    output = mido.open_output('Ableton Push MIDI 2')
    input = mido.open_input('Ableton Push MIDI 2', callback=callback)


def redraw():
    global scrollwheel, buflen, lines

    for i, bufline in enumerate(
        itertools.islice(lines, buflen - 4 - scrollwheel, buflen - scrollwheel)
    ):
        bufline = bufline[:-1].ljust(68)
        bufline = (bufline[:66] + '..') if len(bufline) > 68 else bufline

        data = [71, 127, 21, 24+i, 0, 69, 0] + map(ord, bufline)

        output.send(
            mido.Message('sysex', data=data)
        )


def main(argv=None):
    global scrollwheel, buflen, lines

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--daemonize', '-d',
        action="store_true",
    )
    args = parser.parse_args()

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        lines.append(line)
        lines.popleft()
        redraw()

    if args.daemonize:
        while True:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                sys.exit(0)
