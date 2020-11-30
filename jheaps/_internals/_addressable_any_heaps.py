from .. import backend
from ..types import (
    AddressableHeapHandle,
    AddressableHeap,
)
from ._wrappers import _HandleWrapper


class _IdMap():
    """Helper class which maintains a bidirectional mapping between long values
    and hashable objects.
    """
    def __init__(self):
        self._map = dict()
        self._inverse = dict()
        self._next_id = int()

    def next_id(self):
        id = self._next_id
        self._next_id += 1
        return id

    def put(self, id, value): 
        self._map[id] = value
        if value is not None:
            self._inverse[value] = id

    def update(self, id, value):
        self._map[id] = value
        if value is None:
            self._inverse.pop(value, None)
        else:
            self._inverse[value] = id

    def get(self, id):
        return self._map[id]

    def get_inverse(self, value):
        return self._inverse[value]

    def delete(self, id):
        value = self._map.pop(id)
        if value is not None:
            del self._inverse[value]

    def clear(self):
        self._map.clear()
        self._inverse.clear()


class _BaseAnyAddressableHeapHandle(_HandleWrapper, AddressableHeapHandle):
    """A handle on an element in a heap. This handle supports any object as value.
    """
    def __init__(self, handle, id_map: _IdMap, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._id_map = id_map

    @property
    def value(self):
        id = backend.jheaps_AHeapHandle_get_value(self._handle)
        return self._id_map.get(id)

    @value.setter
    def value(self, v):
        id = backend.jheaps_AHeapHandle_get_value(self._handle)
        self._id_map.update(id, v)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)

    def __del__(self):
        # Custom deletion to allow getter/setters to still function until 
        # garbage collected
        id = backend.jheaps_AHeapHandle_get_value(self._handle)
        self._id_map.delete(id)
        super().__del__()

    def __repr__(self):
        return "_BaseAnyAddressableHeapHandle(%r)" % self._handle


class _DoubleAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports double keys
    and any hashable value.
    """
    def __init__(self, handle, id_map: _IdMap, **kwargs):
        super().__init__(handle, id_map, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_D_get_key(self._handle)

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_D_decrease_key(self._handle, key)

    def __repr__(self):
        return "_DoubleAnyAddressableHeapHandle(%r)" % self._handle


class _LongAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports long keys 
    and any hashable value.
    """
    def __init__(self, handle, id_map: _IdMap, **kwargs):
        super().__init__(handle, id_map, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_L_get_key(self._handle)

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key)

    def __repr__(self):
        return "_LongAnyAddressableHeapHandle(%r)" % self._handle


class _BaseAnyAddressableHeap(_HandleWrapper): 
    """A Heap with any hashable values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._id_map = _IdMap()

    def clear(self):
        backend.jheaps_AHeap_clear(self._handle)
        self._id_map.clear()

    def __len__(self):
        return backend.jheaps_AHeap_size(self._handle)

    def is_empty(self):
        return backend.jheaps_AHeap_isempty(self._handle)

    def __repr__(self):
        return "_BaseAnyHeap(%r)" % self._handle


class _DoubleAnyAddressableHeap(_BaseAnyAddressableHeap): 
    """A Heap with floating point keys and any hashable values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value):
        id = self._id_map.next_id()
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, id)
        self._id_map.put(id, value)
        return _DoubleAnyAddressableHeapHandle(res, self._id_map)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res, self._id_map)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res, self._id_map)

    def __repr__(self):
        return "_DoubleAnyAddressableHeap(%r)" % self._handle


class _LongAnyAddressableHeap(_BaseAnyAddressableHeap): 
    """A Heap with long keys and any hashable values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value):
        id = self._id_map.next_id()
        res = backend.jheaps_AHeap_L_insert_key_value(self._handle, key, id)
        self._id_map.put(id, value)
        return _LongAnyAddressableHeapHandle(res, self._id_map)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _LongAnyAddressableHeapHandle(res, self._id_map)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _LongAnyAddressableHeapHandle(res, self._id_map)

    def __repr__(self):
        return "_LongAnyAddressableHeap(%r)" % self._handle

