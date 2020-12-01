from .. import backend
from ..types import (
    AddressableHeapHandle,
    AddressableHeap,
)
from ._wrappers import _HandleWrapper

from ._utils import (
    _inc_ref,
    _dec_ref,
    _id_to_obj,
)


class _BaseAnyAddressableHeapHandle(_HandleWrapper, AddressableHeapHandle):
    """A handle on an element in a heap. This handle supports any object as value.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)

    @property
    def value(self):
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        return _id_to_obj(value_id)

    @value.setter
    def value(self, v):
        if v is None: 
            raise ValueError('Value cannot be None')

        # clean old value
        old_value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        old_value = _id_to_obj(old_value_id)
        _dec_ref(old_value)

        # set new value
        _inc_ref(v)
        value_id = id(v)
        backend.jheaps_AHeapHandle_set_value(self._handle, value_id)

    def delete(self):
        backend.jheaps_AHeapHandle_delete(self._handle)

    def __del__(self):
        # Custom deletion to allow getter/setters to still function until 
        # garbage collected
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        value = _id_to_obj(value_id)
        _dec_ref(value)
        super().__del__()

    def __repr__(self):
        return "_BaseAnyAddressableHeapHandle(%r)" % self._handle


class _DoubleAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports double keys
    and any hashable value.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle, **kwargs)

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
    def __init__(self, handle, **kwargs):
        super().__init__(handle, **kwargs)

    @property
    def key(self):
        return backend.jheaps_AHeapHandle_L_get_key(self._handle)

    def decrease_key(self, key):
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key)

    def __repr__(self):
        return "_LongAnyAddressableHeapHandle(%r)" % self._handle


class _AnyAnyAddressableHeapHandle(_BaseAnyAddressableHeapHandle):
    """A handle on an element in a heap. This handle supports any hashable key
    and any hashable value.
    """
    def __init__(self, handle, **kwargs):
        super().__init__(handle, **kwargs)

    @property
    def key(self):
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        return _id_to_obj(key_id)

    def decrease_key(self, key):
        # clean old key
        old_key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        old_key = _id_to_obj(old_key_id)
        _dec_ref(old_key)

        # set new key
        _inc_ref(key)
        key_id = id(key)
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key_id)

    def __del__(self):
        # Custom deletion to allow getter/setters to still function until 
        # garbage collected
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        key = _id_to_obj(key_id)
        _dec_ref(key)
        super().__del__()

    def __repr__(self):
        return "_AnyAnyAddressableHeapHandle(%r)" % self._handle


class _BaseAnyAddressableHeap(_HandleWrapper): 
    """A Heap with any hashable values. All operations are delegated
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
        value_id = id(value)
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, value_id)
        return _DoubleAnyAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res)

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
        value_id = id(value)
        res = backend.jheaps_AHeap_L_insert_key_value(self._handle, key, value_id)
        return _LongAnyAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _LongAnyAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        return _LongAnyAddressableHeapHandle(res)

    def __repr__(self):
        return "_LongAnyAddressableHeap(%r)" % self._handle

