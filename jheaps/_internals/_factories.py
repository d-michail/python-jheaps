from .. import backend

from ..types import (
    HeapType as _HeapType,
)

from ._heaps import (
    _DoubleHeap,
    _LongHeap,
    _AnyHeap,
)

from ._addressable_heaps import (
    _DoubleLongAddressableHeap,
    _LongLongAddressableHeap,
)
from ._addressable_any_heaps import (
    _DoubleAnyAddressableHeap,
    _LongAnyAddressableHeap,
    _AnyLongAddressableHeap,
    _AnyAnyAddressableHeap,
)

from ._utils import (
    _id_comparator,
    _create_wrapped_id_comparator_callback,
)


def _wrap_heap(handle, key_type=float, value_type=int, comparator=None, addressable=True):
    if addressable: 
        if key_type == float:
            if value_type == int: 
                return _DoubleLongAddressableHeap(handle)
            else:
                return _DoubleAnyAddressableHeap(handle)
        elif key_type == int:
            if value_type == int:
                return _LongLongAddressableHeap(handle)
            else:
                return _LongAnyAddressableHeap(handle)
        else:
            if value_type == int:
                return _AnyLongAddressableHeap(handle, comparator=comparator)
            else:
                return _AnyAnyAddressableHeap(handle, comparator=comparator)
    else:
        if key_type == float:
            return _DoubleHeap(handle)
        elif key_type == int:
            return _LongHeap(handle)
        else:
            return _AnyHeap(handle, comparator=comparator)


def _create_and_wrap_heap(heap_type, key_type, value_type, addressable):
    if key_type != int or key_type != float: 
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_heap_comparator_create(heap_type.value, f_ptr)
        return _wrap_heap(handle, key_type, value_type, comparator=f, addressable=addressable)
    else:
        handle = backend.jheaps_heap_create(heap_type.value)
        return _wrap_heap(handle, key_type, value_type, addressable=addressable)


def _create_and_wrap_dary_heap(heap_type, d, key_type, value_type, addressable):

    if key_type != int or key_type != float: 
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_dary_heap_comparator_create(heap_type.value, f_ptr, d)
        return _wrap_heap(handle, key_type, value_type, comparator=f, addressable=addressable)
    else:
        handle = backend.jheaps_dary_heap_create(heap_type.value, d)
        return _wrap_heap(handle, key_type, value_type, addressable=addressable)


def _create_and_wrap_radix_heap(heap_type, min, max, key_type, value_type, addressable):
    if key_type == float: 
        handle = backend.jheaps_double_radix_heap_create(heap_type, min, max)
        return _wrap_heap(handle, key_type, value_type, addressable=addressable)
    elif key_type == int: 
        handle = backend.jheaps_long_radix_heap_create(heap_type, min, max)
        return _wrap_heap(handle, key_type, value_type, addressable=addressable)
    else:
        raise ValueError('Key type can only be float or int')

