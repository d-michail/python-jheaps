from .. import backend
from ..types import (
    AddressableHeapHandle,
    AddressableHeap,
)
from ._wrappers import _HandleWrapper

from ._utils import (
    _inc_ref,
    _inc_ref_by_id,
    _dec_ref,
    _dec_ref_by_id,
    _id_to_obj,
    _id_comparator,
)


class _BaseAnyAddressableHeapHandle(_HandleWrapper, AddressableHeapHandle):
    """A handle on an element in a heap. This handle supports any object as value.
    """
    def __init__(self, handle, key_owner=False, value_owner=False, **kwargs):
        super().__init__(handle=handle, **kwargs)
        self._key_owner = key_owner
        self._value_owner = value_owner

    @property
    def value(self):
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        return _id_to_obj(value_id)

    @value.setter
    def value(self, v):
        if v is None: 
            raise ValueError('Value cannot be None')

        # Decrement value ref-count independently on whether the
        # handle or the heap is the owner 
        self._dec_value_ref()

        backend.jheaps_AHeapHandle_set_value(self._handle, id(v))

        # Increment value ref-count independently on whether the
        # handle or the heap is the owner 
        _inc_ref(v)

    def __del__(self):
        if self._value_owner:
            self._dec_value_ref()
        super().__del__()

    def _dec_value_ref(self):
        """Decrement reference count on value.
        """
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        _dec_ref(_id_to_obj(value_id))

    def __repr__(self):
        return "_BaseAnyAddressableHeapHandle(%r)" % self._handle


class _DoubleAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports double keys
    and any hashable value.
    """
    def __init__(self, handle, value_owner=False, **kwargs):
        super().__init__(handle, False, value_owner, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_D_get_key(self._handle)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)
        # Take ownership due to deletion from the heap
        self._value_owner = True

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_D_decrease_key(self._handle, key)

    def __repr__(self):
        return "_DoubleAnyAddressableHeapHandle(%r)" % self._handle


class _LongAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports long keys 
    and any hashable value.
    """
    def __init__(self, handle, value_owner=False, **kwargs):
        super().__init__(handle, False, value_owner, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_L_get_key(self._handle)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)
        # Take ownership due to deletion from the heap
        self._value_owner = True

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key)

    def __repr__(self):
        return "_LongAnyAddressableHeapHandle(%r)" % self._handle


class _AnyAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports any hashable key
    and any hashable value.
    """
    def __init__(self, handle, key_owner=False, value_owner=False, **kwargs):
        super().__init__(handle, key_owner, value_owner, **kwargs)

    @property
    def key(self):
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        return _id_to_obj(key_id)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)
        # Take ownership due to deletion from the heap
        self._key_owner = True
        self._value_owner = True

    def decrease_key(self, key):
        old_key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, id(key))

        if self._key_owner: 
            raise ValueError('Cannot be key owner to a valid handle')

        _dec_ref_by_id(old_key_id)
        _inc_ref(key)

    def __del__(self):
        if self._key_owner:
            self._dec_key_ref()
        super().__del__()

    def _dec_key_ref(self):
        """Decrement reference count on key.
        """
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        _dec_ref(_id_to_obj(key_id))

    def __repr__(self):
        return "_AnyAnyAddressableHeapHandle(%r)" % self._handle


class _BaseAnyAddressableHeap(_HandleWrapper): 
    """A Heap with any hashable values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

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
        if value is None: 
            raise ValueError('Value cannot be None')
        _inc_ref(value)
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, id(value))
        return _DoubleAnyAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        # pass value ownership to handle
        return _DoubleAnyAddressableHeapHandle(res, value_owner=True)

    def clear(self):
        # Clean one by one in order to decrease reference counts
        while not self.is_empty(): 
            res = backend.jheaps_AHeap_delete_min(self._handle)
            value_id = backend.jheaps_AHeapHandle_get_value(res)
            _dec_ref_by_id(value_id)
            backend.jheaps_handles_destroy(res)

    def __repr__(self):
        return "_DoubleAnyAddressableHeap(%r)" % self._handle


class _LongAnyAddressableHeap(_BaseAnyAddressableHeap): 
    """A Heap with long keys and any hashable values. All operations are delegated
    to the backend.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    def insert(self, key, value):
        if value is None: 
            raise ValueError('Value cannot be None')
        _inc_ref(value)
        res = backend.jheaps_AHeap_L_insert_key_value(self._handle, key, id(value))
        return _LongAnyAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _LongAnyAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        # pass value ownership to handle
        return _LongAnyAddressableHeapHandle(res, value_owner=True)

    def clear(self):
        # Clean one by one in order to decrease reference counts
        while not self.is_empty(): 
            res = backend.jheaps_AHeap_delete_min(self._handle)
            value_id = backend.jheaps_AHeapHandle_get_value(res)
            _dec_ref_by_id(value_id)
            backend.jheaps_handles_destroy(res)

    def __repr__(self):
        return "_LongAnyAddressableHeap(%r)" % self._handle

