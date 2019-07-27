from collections import namedtuple
from collections import OrderedDict
import functools
import time


CacheItem = namedtuple("CacheItem", ["data", "expiry"])
CacheItem.__doc__ = """A single item in the cache.

data
    The contents of this cache entry.
expiry : float
    The time in seconds (unix timestamp) at which this entry expires.
"""


class _Cache(object):
    """
    A Least Recently Used cache with Time to Live support.
    
    WARNING: This class is only intended to be used internally
    by FuncCache in its current state, as it is missing a number
    of dictionary-like features.
    
    Behaves similarly to a dictionary but without support for
    all dictionary functionality. 
    
    This class's methods are not intended to be called
    directly. Objects instantiated from this class should
    instead be treated like dictionaries, using the [] operator.
    
    Attributes
    ----------
    size : int
        The maximum number of entries allowed in the cache.
    expiry : float
        The number of seconds for which a cache entry is valid.
    """

    def __init__(self, size, expiry, *args, **kwargs):
        self.size   = size
        self.expiry = expiry
        self.cache  = OrderedDict()

    def _has_expired(self, key):
        """Returns true if the item has expired."""

        return self.cache[key].expiry < time.monotonic()

    def __setitem__(self, key, value):
        """Adds item to cache or update existing value."""

        # Update expiration time and move to the end.
        self.cache[key] = CacheItem(value,
                                    time.monotonic() + self.expiry)
        self.cache.move_to_end(key)
        # If cache is now too big, remove the oldest item.
        if len(self.cache) > self.size:
            self.cache.popitem(last = False)

    def __getitem__(self, key):
        """Retrieves existing cache item."""

        if not self._has_expired(key):
        # Update expiration time and move to the end.
            self.cache[key] = CacheItem(self.cache[key].data,
                                        time.monotonic() + self.expiry)
            self.cache.move_to_end(key)
            return self.cache[key].data
        else:
            raise KeyError("Item has expired from cache.")

    def __contains__(self, key):
        """Checks whether the cache contains a given item."""

        if key in self.cache and not self._has_expired(key):
            return True
        else:
            return False


class FuncCache(object):
    """
    A function cache decorator.
    
    Class-based decorator which behaves similarly to Python
    functools' lru_cache decorator, but also supports expiring
    entries automatically based on a time-to-live value.
    
    Use like any decorator:
    @FuncCache(size = 10, expiry = 2.5)
    def ExampleFunction(example_param, another_param):
        ...
    
    Attributes
    ----------
    size : int
        The maximum number of entries allowed in the cache.
    expiry : float
        The number of seconds for which a cache entry is valid.
    """

    def __init__(self, size = 1000, expiry = 5.0):
        self.cache = _Cache(size, expiry)

    def __call__(self, func):
        @functools.wraps(func)
        def decofunc(*args, **kwargs):
            key = (tuple(args), tuple(sorted(kwargs.items())))
            try:
                return self.cache[key]
            except KeyError:
                value = func(*args, **kwargs)
                self.cache[key] = value
                return value
        return decofunc
