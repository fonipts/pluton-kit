__version__ = "1.0.0a0"

def setup(set_prefix=True):
    """
    Configure the settings (this happens as a side effect of accessing the
    first setting), configure logging and populate the app registry.
    Set the thread-local urlresolvers script prefix if `set_prefix` is True.
    """
    import plutonkit.config
    import plutonkit.command
    import plutonkit.core

