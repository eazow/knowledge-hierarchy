def _slots(names=""):
    """Returns the private version of names for __slots__ on a class."""
    return tuple("__" + name for name in names.split())
