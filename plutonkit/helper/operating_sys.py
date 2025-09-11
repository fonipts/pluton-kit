import sys


def is_windows() ->bool:
    return sys.platform in ("win32", "cygwin")
