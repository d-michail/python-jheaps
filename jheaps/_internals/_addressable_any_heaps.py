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
    def __init__(self, handle, **kwargs):
        super().__init__(handle=handle, **kwargs)
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        _inc_ref_by_id(value_id)

    @property
    def value(self):
        value_id = backend.jheaps_AHeapHandle_get_value(self._handle)
        return _id_to_obj(value_id)

    @value.setter
    def value(self, v):
        if v is None: 
            raise ValueError('Value cannot be None')

        # decrement ref count on old value twice, once for handle
        # and once for heap
        self._dec_value_ref()
        self._dec_value_ref()

        # increment ref count on new value twice, once for handle
        # and once for heap
        _inc_ref(v)
        _inc_ref(v)
        value_id = id(v)
        backend.jheaps_AHeapHandle_set_value(self._handle, value_id)

    def delete(self):
        self._dec_value_ref()
        backend.jheaps_AHeapHandle_delete(self._handle)

    def __del__(self):
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
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        _inc_ref_by_id(key_id)

    @property
    def key(self):
        key_id = backend.jheaps_AHeapHandle_L_get_key(self._handle)
        return _id_to_obj(key_id)

    def decrease_key(self, key):
        # clean old key
        self._dec_key_ref()
        self._dec_key_ref()

        # set new key
        _inc_ref(key)
        _inc_ref(key)
        key_id = id(key)
        backend.jheaps_AHeapHandle_L_decrease_key(self._handle, key_id)

    def __del__(self):
        # Custom deletion to allow getter/setters to still function until 
        # garbage collected
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
        value_id = id(value)
        res = backend.jheaps_AHeap_D_insert_key_value(self._handle, key, value_id)
        return _DoubleAnyAddressableHeapHandle(res)

    def find_min(self):
        res = backend.jheaps_AHeap_find_min(self._handle)
        return _DoubleAnyAddressableHeapHandle(res)

    def delete_min(self):
        res = backend.jheaps_AHeap_delete_min(self._handle)
        handle = _DoubleAnyAddressableHeapHandle(res)
        # Decrease heap reference count, after incrementing by the handle
        value_id = backend.jheaps_AHeapHandle_get_value(res)
        _dec_ref_by_id(value_id)
        return handle

    def clear(self):
        # Clean one by one in order to decrease reference counts
        while not self.is_empty(): 
            res = backend.jheaps_AHeap_delete_min(self._handle)
            value_id = backend.jheaps_AHeapHandle_get_value(res)
            _dec_ref_by_id(value_id)

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
        handle = _LongAnyAddressableHeapHandle(res)
        # Decrease heap reference count, after incrementing by the handle
        value_id = backend.jheaps_AHeapHandle_get_value(res)
        _dec_ref_by_id(value_id)
        return handle

    def clear(self):
        # Clean one by one in order to decrease reference counts
        while not self.is_empty(): 
            res = backend.jheaps_AHeap_delete_min(self._handle)
            value_id = backend.jheaps_AHeapHandle_get_value(res)
            _dec_ref_by_id(value_id)

    def __repr__(self):
        return "_LongAnyAddressableHeap(%r)" % self._handle

