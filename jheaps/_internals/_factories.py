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
    _DoubleLongMergeableAddressableHeap,
    _LongLongAddressableHeap,
    _LongLongMergeableAddressableHeap,
)

from ._addressable_any_heaps import (
    _DoubleAnyAddressableHeap,
    _DoubleAnyMergeableAddressableHeap,
    _LongAnyAddressableHeap,
    _LongAnyMergeableAddressableHeap,
    _AnyLongAddressableHeap,
    _AnyLongMergeableAddressableHeap,
    _AnyAnyAddressableHeap,
    _AnyAnyMergeableAddressableHeap,
)

from ._utils import (
    _id_comparator,
    _create_wrapped_id_comparator_callback,
)


def _wrap_heap(
    handle,
    key_type=float,
    value_type=int,
    comparator=None,
    addressable=True,
    mergeable=False,
):
    if addressable:
        if mergeable:
            if key_type == float:
                if value_type == int:
                    return _DoubleLongMergeableAddressableHeap(handle)
                else:
                    return _DoubleAnyMergeableAddressableHeap(handle)
            elif key_type == int:
                if value_type == int:
                    return _LongLongMergeableAddressableHeap(handle)
                else:
                    return _LongAnyMergeableAddressableHeap(handle)
            else:
                if value_type == int:
                    return _AnyLongMergeableAddressableHeap(
                        handle, comparator=comparator
                    )
                else:
                    return _AnyAnyMergeableAddressableHeap(
                        handle, comparator=comparator
                    )
        else:
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


def _create_and_wrap_heap(heap_type, key_type, value_type, addressable, mergeable):
    if key_type != int and key_type != float:
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_heap_comparator_create(heap_type.value, f_ptr)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            comparator=f,
            addressable=addressable,
            mergeable=mergeable,
        )
    else:
        handle = backend.jheaps_heap_create(heap_type.value)
        return _wrap_heap(
            handle, key_type, value_type, addressable=addressable, mergeable=mergeable
        )


def _create_and_wrap_dary_heap(
    heap_type, d, key_type, value_type, addressable, mergeable
):
    if key_type != int and key_type != float:
        f_ptr, f = _create_wrapped_id_comparator_callback(_id_comparator)
        handle = backend.jheaps_dary_heap_comparator_create(heap_type.value, f_ptr, d)
        return _wrap_heap(
            handle,
            key_type,
            value_type,
            comparator=f,
            addressable=addressable,
            mergeable=mergeable,
        )
    else:
        handle = backend.jheaps_dary_heap_create(heap_type.value, d)
        return _wrap_heap(
            handle, key_type, value_type, addressable=addressable, mergeable=mergeable
        )


def _create_and_wrap_radix_heap(
    heap_type, min, max, key_type, value_type, addressable, mergeable
):
    if key_type == float:
        handle = backend.jheaps_double_radix_heap_create(heap_type, min, max)
        return _wrap_heap(
            handle, key_type, value_type, addressable=addressable, mergeable=mergeable
        )
    elif key_type == int:
        handle = backend.jheaps_long_radix_heap_create(heap_type, min, max)
        return _wrap_heap(
            handle, key_type, value_type, addressable=addressable, mergeable=mergeable
        )
    else:
        raise ValueError("Key type can only be float or int")
