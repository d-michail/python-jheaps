from .. import backend
from ._wrappers import _HandleWrapper


class _BaseHeap(_HandleWrapper): 
    """A Heap. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def clear(self):
        backend.jheaps_Heap_clear(self._handle)

    def __len__(self):
        return backend.jheaps_Heap_size(self._handle)

    def is_empty(self):
        return backend.jheaps_Heap_isempty(self._handle)

    def __repr__(self):
        return "_BaseHeap(%r)" % self._handle


class _DoubleHeap(_BaseHeap): 
    """A Heap with floating point keys. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key):
        backend.jheaps_Heap_D_insert_key(self._handle, key)

    def find_min(self):
        return backend.jheaps_Heap_D_find_min(self._handle)

    def delete_min(self):
        return backend.jheaps_Heap_D_delete_min(self._handle)

    def __repr__(self):
        return "_DoubleHeap(%r)" % self._handle


class _LongHeap(_BaseHeap): 
    """A Heap with long integer keys. All operations are delegated to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key):
        backend.jheaps_Heap_L_insert_key(self._handle, key)

    def find_min(self):
        return backend.jheaps_Heap_L_find_min(self._handle)

    def delete_min(self):
        return backend.jheaps_Heap_L_delete_min(self._handle)

    def __repr__(self):
        return "_LongHeap(%r)" % self._handle

