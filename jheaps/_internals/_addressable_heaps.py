from .. import backend
from ..types import (
    AddressableHeapHandle,
    AddressableHeap,
)
from ._wrappers import _HandleWrapper


class _BaseLongValueAddressableHeapHandle(_HandleWrapper, AddressableHeapHandle):
    """A handle on an element in a heap. This handle supports long integer values.
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
        return "_BaseLongValueAddressableHeapHandle(%r)" % self._handle


class _DoubleLongAddressableHeapHandle(_BaseLongValueAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports double keys
    and long integer values.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_D_get_key(self._handle)

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_D_decrease_key(self._handle, key)

    def __repr__(self):
        return "_DoubleLongAddressableHeapHandle(%r)" % self._handle


class _LongLongAddressableHeapHandle(_BaseLongValueAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports long keys 
    and long integer values.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_L_get_key(self._handle)

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key)

    def __repr__(self):
        return "_LongLongAddressableHeapHandle(%r)" % self._handle


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


class _DoubleLongAddressableHeap(_BaseAddressableHeap): 
    """A Heap with floating point keys and long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value=0):
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, value)
        return _DoubleLongAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleLongAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _DoubleLongAddressableHeapHandle(res)

    def __repr__(self):
        return "_DoubleLongAddressableHeap(%r)" % self._handle


class _LongLongAddressableHeap(_BaseAddressableHeap): 
    """A Heap with long keys and long values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value=0):
        res = backend.jheaps_AHeap_L_insert_key_value(self._handle, key, value)
        return _LongLongAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _LongLongAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _LongLongAddressableHeapHandle(res)

    def __repr__(self):
        return "_LongLongAddressableHeap(%r)" % self._handle


