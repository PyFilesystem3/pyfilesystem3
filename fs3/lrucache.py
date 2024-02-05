"""Least Recently Used cache mapping.
"""

import typing

from collections import OrderedDict

_K = typing.TypeVar("_K")
_V = typing.TypeVar("_V")


class LRUCache(OrderedDict, typing.Generic[_K, _V]):
    """A dictionary-like container that stores a given maximum items.

    If an additional item is added when the LRUCache is full, the least
    recently used key is discarded to make room for the new item.

    """

    def __init__(self, cache_size):
        # type: (int) -> None
        """Create a new LRUCache with the given size."""
        self.cache_size = cache_size
        super().__init__()

    def __setitem__(self, key, value):
        # type: (_K, _V) -> None
        """Store a new views, potentially discarding an old value."""
        if key not in self:
            if len(self) >= self.cache_size:
                self.popitem(last=False)
        OrderedDict.__setitem__(self, key, value)

    def __getitem__(self, key):
        # type: (_K) -> _V
        """Get the item, but also makes it most recent."""
        _super = typing.cast(OrderedDict, super())
        value = _super.__getitem__(key)
        _super.__delitem__(key)
        _super.__setitem__(key, value)
        return value