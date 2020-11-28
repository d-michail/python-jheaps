from .. import backend
from ..types import (
    HeapType,
    AddressableHeapHandle,
    AddressableHeap,
)
from ._wrappers import _HandleWrapper


class _BaseAddressableHeapHandle(_HandleWrapper, AddressableHeapHandle):
    """A handle on an element in a heap.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def value(self):
        return backend.jheaps_AHeapHandle_get_value(self._handle)

    @value.setter
    def value(self, v):
        backend.jheaps_AHeapHandle_set_value(self._handle, v)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)

    def __repr__(self):
        return "_BaseAddressableHeapHandle(%r)" % self._handle



class _DoubleAddressableHeapHandle(_BaseAddressableHeapHandle):
    """A handle on an element in a heap.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_D_get_key(self._handle)

    def decrease_key(self, key):
        res = backend.jheaps_AHeapHandle_D_decrease_key(self._handle, key)

    def __repr__(self):
        return "_DoubleAddressableHeapHandle(%r)" % self._handle


class _LongAddressableHeapHandle(_BaseAddressableHeapHandle):
    """A handle on an element in a heap.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_L_get_key(self._handle)

    def decrease_key(self, key):
        res = backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key)

    def __repr__(self):
        return "_LongAddressableHeapHandle(%r)" % self._handle


class _BaseAddressableHeap(_HandleWrapper): 
    """A Heap with long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def clear(self):
        backend.jheaps_AHeap_clear(self._handle)

    def __len__(self):
        return backend.jheaps_AHeap_size(self._handle)

    def is_empty(self):
        return backend.jheaps_AHeap_isempty(self._handle)

    def __repr__(self):
        return "_BaseAddressableHeap(%r)" % self._handle


class _DoubleAddressableHeap(_BaseAddressableHeap): 
    """A Heap with floating point keys and long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value=0):
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, value)
        return _DoubleAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _DoubleAddressableHeapHandle(res)

    def __repr__(self):
        return "_DoubleAddressableHeap(%r)" % self._handle


class _LongAddressableHeap(_BaseAddressableHeap): 
    """A Heap with long keys and long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value=0):
        res = backend.jheaps_AHeap_L_insert_key_value(self._handle, key, value)
        return _LongAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _LongAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _LongAddressableHeapHandle(res)

    def __repr__(self):
        return "_LongAddressableHeap(%r)" % self._handle



def _create_double_heap(type=HeapType.PAIRING):
    """Create a heap with double keys.

    TODO: kind of heap

    :returns: a heap
    """
    handle = backend.jheaps_heap_create(type.value)
    return _DoubleAddressableHeap(handle)


def _create_long_heap(type=HeapType.PAIRING):
    """Create a heap with long keys.

    TODO: kind of heap

    :returns: a heap
    """
    handle = backend.jheaps_heap_create(type.value)
    return _LongAddressableHeap(handle)
