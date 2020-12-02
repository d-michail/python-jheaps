from .. import backend

from ..types import (
    HeapType as _HeapType,
)

from ._heaps import (
    _DoubleHeap,
    _LongHeap,
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


def _create_heap(key_type, type: _HeapType):
    """Create a heap.

    :returns: a heap
    """
    handle = backend.jheaps_heap_create(type.value)
    if key_type == float: 
        return _DoubleHeap(handle)
    elif key_type == int:
        return _LongHeap(handle)
    
    raise ValueError("Invalid key type")


def _create_addressable_heap(type: _HeapType, key_type=float, value_type=int):
    """Create an addressable heap.

    :returns: a heap
    """
    handle = backend.jheaps_heap_create(type.value)
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
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_heap_comparator_create(type.value, f_ptr)

        if value_type == int:
            return _AnyLongAddressableHeap(handle, comparator=f)
        else:
            return _AnyAnyAddressableHeap(handle, comparator=f)    
