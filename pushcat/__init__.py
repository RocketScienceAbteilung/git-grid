import sys
import time
import mido
import argparse
import itertools
import threading
import collections


class PushCat(object):  # Like netcat, but for push
    def callback(self, message):
        # pitchweel touch: start scrolling
        if message.type == 'pitchwheel' and message.pitch != 0:
            pitch = (message.pitch + 2. ** 13) / 2. ** 14
            # prevent out of bounds when scrolling all the way up
            self.scrollwheel = min(self.buflen - 4, int(self.buflen * pitch))
            self.redraw()
        # pitchweel release: scroll all the way down again
        elif message.type == 'pitchwheel' and message.pitch == 0:
            self.scrollwheel = 0
            self.redraw()

    def redraw(self):
        self.lock.acquire()

        # Get 4 lines of text, according to current scrollwheel position
        for i, bufline in enumerate(
            itertools.islice(
                self.lines,
                self.buflen - 4 - self.scrollwheel,
                self.buflen - self.scrollwheel
            )
        ):
            # - Remove newline, it prints an a-umlaut on the controller
            # - Add spaces to fill 68 chars because Push only prints stuff if
            #   the sysex cmd is actually long enough
            bufline = bufline[:-1].ljust(68)
            # - Truncate if line is too long
            bufline = (bufline[:66] + '..') if len(bufline) > 68 else bufline

            # - Map to sysex command
            data = [71, 127, 21, 24+i, 0, 69, 0] + map(ord, bufline)

            self.output.send(
                mido.Message('sysex', data=data)
            )
        self.lock.release()

    def __init__(self, daemonize=False, buflen=80):
        self.scrollwheel = 0
        self.buflen = buflen
        self.lines = collections.deque([''] * self.buflen)
        self.lock = threading.Lock()

        try:
            # Ports on MAC OSX
            self.output = mido.open_output('Ableton Push User Port')
            self.input = mido.open_input('Ableton Push User Port',
                                         callback=self.callback)
        except IOError:
            # Ports on Arch Linux
            self.output = mido.open_output('Ableton Push MIDI 2')
            self.input = mido.open_input('Ableton Push MIDI 2',
                                         callback=self.callback)

        while True:
            line = sys.stdin.readline()
            if not line:
                # EOF from STDIN
                break

            # We need to use mutex because concurrent reads and writes on
            # dequeue (scrolling while there is new text coming in from stdin)
            # will issue warnings.
            self.lock.acquire()
            self.lines.append(line)
            self.lines.popleft()
            self.lock.release()
            self.redraw()

        # Do not quit process if running daemonized
        # This enables scrolling for one-show piping to Push
        #
        # e.g. ping www.google.de | pushcat is scrollable as long as ping runs
        # ls | pushcat is not scrollable as ls immediately terminates
        # ls | pushcat -d enables scrolling
        if daemonize:
            while True:
                try:
                    time.sleep(0.1)
                except KeyboardInterrupt:
                    sys.exit(0)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--daemonize', '-d', action="store_true",
    )
    parser.add_argument(
        '--buflen', '-b', type=int, default=80,
    )
    args = parser.parse_args()

    PushCat(args.daemonize, args.buflen)
