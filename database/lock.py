import _thread

from utils import _slots


class _Lock:
    "_Lock(immediate=False, silent=False) -> _Lock"

    __slots__ = _slots("lock verbose")

    def __init__(self, immediate=False, silent=False):
        "Initializes _Lock instance with internal mechanism."
        self.__lock = _thread.allocate_lock()
        self.__verbose = silent
        if immediate:
            self.acquire()

    ########################################################################

    def acquire(self, wait=True):
        "Acquires lock with an optional wait."
        return self.__lock.acquire(wait)

    def release(self, exc_type=None, exc_value=None, traceback=None):
        "Release lock if locked or possibly throws error."
        try:
            self.__lock.release()
        except _thread.error:
            if self.__verbose:
                raise

    ########################################################################

    __enter__ = acquire

    __exit__ = release

    ########################################################################

    @property
    def locked(self):
        "Returns whether or not lock is currently locked."
        return self.__lock.locked()