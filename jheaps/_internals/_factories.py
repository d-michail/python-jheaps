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


def _create_addressable_heap(type: _HeapType, key_type, value_type):
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
    
    raise ValueError("Invalid key type (only float or int are currently supported)")

