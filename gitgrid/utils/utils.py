import argparse
import math
import re
import hashlib


def hash_to_rgb(val):
    return [
        tuple(ord(c)/255. for c in i.decode('hex'))
        for i in re.findall('.{6}', val)
    ]


def string_to_rgb(val):
    return hash_to_rgb(hashlib.sha1(val).hexdigest())


def hash_keys(val):
    return [
        (string_to_rgb(key), value) for (key, value) in val
    ]


def normalize_sum(val, maxlen=7.):
    if not val:
        return val
    maxval = float(max([a + b for _, (a, b) in val]))

    if maxval > maxlen:
        return [
            (f, (math.ceil(a / maxval * maxlen), math.ceil(b / maxval * maxlen)))
            for f, (a, b) in val
        ]
    else:
        return val


def normalize_single(val, maxlen=3.):
    if not val:
        return val
    maxval = float(max([max(a, b) for _, (a, b) in val]))

    if maxval > maxlen:
        return [
            (f, (math.ceil(a / maxval * maxlen), math.ceil(b / maxval * maxlen)))
            for f, (a, b) in val
        ]
    else:
        return val


def controller_args(parser=None, parse=True):
    if parser is None:
        parser = argparse.ArgumentParser()

    parser.add_argument(
        '--controller', '-c',
        default="launchpad",
    )
    parser.add_argument(
        '--input', '-i',
        default=None,
    )
    parser.add_argument(
        '--output', '-o',
        default=None,
    )

    if parse:
        return parser.parse_args()
    else:
        return parser


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
