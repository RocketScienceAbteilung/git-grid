import fileinput


def main(argv=None):
    for line in fileinput.input():
        print line
