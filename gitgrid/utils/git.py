import random
import string
import subprocess
import re
import sys
from . import utils, names


def run(cmd, print_cmd=False, print_ret=False):
    if print_cmd:
        print ">>> %s" % cmd
        sys.stdout.flush()
    ret = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    if print_ret:
        print ret
        sys.stdout.flush()
    return ret

#
#
# GETTERS
#
# These functions MAY NEVER modify the repo
#
#


def get_log(start):
    start += 1
    return run(
        "git log --graph --decorate --pretty=oneline "
        "--all | sed -n %d,%dp" % (start, start+15)
    )


def get_diff():
    run("git diff", print_cmd=True, print_ret=True)
    files = run("git diff --numstat").splitlines()

    return [
        (
            i.split('\t')[2],
            [
                float(i.split('\t')[0]),
                float(i.split('\t')[1])
            ]
        )
        for i in files
    ]


def get_branches(exclude=None):
    branches = run(
        "git for-each-ref --format='%(refname:short)' refs/heads/"
    ).splitlines()

    return [i for i in branches if not i == exclude]


def get_current_branch():
    try:
        return run("git symbolic-ref --short -q HEAD").strip()
    except subprocess.CalledProcessError:
        # An error means we are on no branch (detached HEAD)
        return ""


def get_current_commit():
    return run("git rev-parse HEAD").strip()


def get_between(branches):
    return [
        (
            branch,
            map(int, run(
                "git rev-list --left-right --count $HEAD...%s" % branch
            )[:-1].split('\t'))
        ) for branch in branches
    ]


def get_can_merge(branch):
    try:
        run(
            "git format-patch HEAD..%s --stdout | git apply --check -" % branch
        ).strip()
        return True
    except subprocess.CalledProcessError:
        return False


def get_can_merge_ff(branch):
    try:
        base = run("git merge-base HEAD %s" % branch).strip()

        if base == get_current_commit():
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

#
#
# PARSERS/TRANSFORMERS
#
# These functions MAY NEVER shell out to git
#
#


def parse_tree(val, fill=1):
    head = get_current_commit()

    search = {
        '*': (1, 1, 0),
        '|': (0.3, 0.3, 0),
        '\\': (0.3, 0.3, 0),
        '/': (0.3, 0.3, 0),
    }

    if val[0] == head:
        search['*'] = (1, 1, 1)

    ret = [
        search.get(g, (0, 0, 0)) for g in val[1] if g != ' '
    ]

    if len(ret) < fill:
        ret += [(0, 0, 0)] * (fill - len(ret))

    return ret


def parse_log(log, length):
    out = []
    for line in log.splitlines(True):
        m = re.search(r'([\*|\\\/ ]+)\s([0-9a-f]{40})\s(.*)', line)
        if m:
            out.append(
                (
                    m.group(2),
                    m.group(1)
                )
            )
        if len(out) == length:
            break
    return out


def parse_tree_width(val):
    return [
        len(filter(lambda x: x not in " ", g)) for h, g in val
    ]

#
#
# DOERS
#
# These functions modify the repo
#
#


def do_new_branch(name=None):
    if name is None:
        name = 'gitgrid-' + names.handle()

    try:
        run("git checkout -b %s" % name, print_cmd=True)
        return True
    except subprocess.CalledProcessError:
        return False


def do_commit(message=None):
    if message is None:
        name = 'Gitgrid: ' + names.name()

    try:
        run("git commit -am '%s'" % name, print_cmd=True)
        return True
    except subprocess.CalledProcessError:
        return False


def do_resethard():
    try:
        run("git reset --hard HEAD", print_cmd=True)
        return True
    except subprocess.CalledProcessError:
        return False


def do_checkout(name):
    try:
        run("git checkout %s" % name, print_cmd=True)
        return True
    except subprocess.CalledProcessError:
        return False


def do_merge(name):
    try:
        run("git merge %s" % name, print_cmd=True)
        try:
            run("git branch -d %s" % name, print_cmd=True)
        except subprocess.CalledProcessError:
            pass
        return True
    except subprocess.CalledProcessError:
        run("git merge --abort", print_cmd=True)
        return False
