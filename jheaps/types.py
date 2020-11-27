from abc import ABC, abstractmethod
from collections.abc import Mapping

from .backend import HeapType

class AddressableHeapHandle(ABC):
    """Interface for an addressable heap handle."""

    @abstractmethod
    def get_key(self):
        """Get the key
        """
        pass

    @abstractmethod
    def get_value(self):
        """Get the value
        :rtype: long integer
        """
        pass



class AddressableHeap(ABC):
    """Interface for an addressable heap."""

    @abstractmethod
    def find_min(self):
        """Return a handle for the minimum element.

        :rtype: :class:`.AddressableHeapHandle`
        """
        pass


