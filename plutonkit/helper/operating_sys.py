import sys


def is_windows():
    return sys.platform in ("win32", "cygwin")
