from .. import backend
from ..types import (
    HeapType,
)
from ._wrappers import _HandleWrapper


class _AddressableHeapHandle(_HandleWrapper):
    """A handle on an element in a heap.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def decreaseKey(self, key):
        res = backend.jheaps_AHeapHandle_D_decrease_key(self._handle, key)

    def __repr__(self):
        return "_AddressableHeapHandle(%r)" % self._handle


class _DoubleAddressableHeap(_HandleWrapper): 
    """A Heap with floating point keys and long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value):
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, value)
        return _AddressableHeapHandle(res)

    def __repr__(self):
        return "_DoubleAddressableHeap(%r)" % self._handle


def _create_double_heap():
    """Create a heap with double keys.

    TODO: kind of heap

    :returns: a heap
    """
    handle = backend.jheaps_heap_create(HeapType.PAIRING)
    return _DoubleAddressableHeap(handle)

