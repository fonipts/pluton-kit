"""Module providing a function printing python version."""

__version__ = "1.0.32a1"

from .built_in.command import PLCommand as Command

__all__ = ["Command"]

def setup():
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    Set the thread-local urlresolvers script prefix if `set_prefix` is True.
    """
