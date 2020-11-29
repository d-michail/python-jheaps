import pytest

from random import Random

from jheaps import (
    create_binary
)

def test_double_heap_implicit(): 

    h = create_binary(addressable=False, explicit=False)

    h.insert(5.5)
    h.insert(6.5)
    h.insert(7.5)
    h.insert(8.5)

    h5 = h.find_min()
    assert h5 == 5.5

    assert len(h) == 4

    h.delete_min()
    assert 6.5 == h.find_min()
    assert len(h) == 3

    h.clear()
    assert len(h) == 0


def test_long_heap_implicit(): 

    h = create_binary(key_type=int, addressable=False, explicit=False)

    h.insert(5)
    h.insert(6)
    h.insert(7)
    h.insert(8)

    h5 = h.find_min()
    assert h5 == 5

    assert len(h) == 4

    h.delete_min()
    assert 6 == h.find_min()
    assert len(h) == 3

    h.clear()
    assert len(h) == 0


def test_double_heap_explicit(): 

    h = create_binary(addressable=False, explicit=True)

    h1 = h.insert(5.5, 15)
    assert h1.key == 5.5
    assert h1.value == 15
    h1.value=10
    assert h1.value == 10

    h2 = h.insert(6.5, 20)
    h3 = h.insert(7.5, 20)
    h4 = h.insert(8.5, 20)

    h5 = h.find_min()
    assert h5.key == 5.5
    assert h5.value == 10

    h5.decrease_key(4.5)
    assert h5.key == 4.5
    assert h5.value == 10

    assert len(h) == 4

    h5.delete()
    assert len(h) == 3

    # check that handle is still valid even if 
    # removed 
    assert h5.key == 4.5
    assert h5.value == 10

    # But reusing should throw a value error
    with pytest.raises(ValueError):
        h5.delete()

    h.clear()
    assert len(h) == 0


def test_double_addressable_heap_implicit(): 

    h = create_binary(addressable=True)

    h1 = h.insert(5.5, 15)
    assert h1.key == 5.5
    assert h1.value == 15
    h1.value=10
    assert h1.value == 10

    h2 = h.insert(6.5, 20)
    h3 = h.insert(7.5, 20)
    h4 = h.insert(8.5, 20)

    h5 = h.find_min()
    assert h5.key == 5.5
    assert h5.value == 10

    h5.decrease_key(4.5)
    assert h5.key == 4.5
    assert h5.value == 10

    assert len(h) == 4

    h5.delete()
    assert len(h) == 3

    # check that handle is still valid even if 
    # removed 
    assert h5.key == 4.5
    assert h5.value == 10

    # But reusing should throw a value error
    with pytest.raises(ValueError):
        h5.delete()

    h.clear()
    assert len(h) == 0


def test_sort_with_heap():
    rng = Random(17)

    numbers = []
    for i in range(10000):
        numbers.append(rng.random())

    heap = create_binary(addressable=True)
    for n in numbers: 
        heap.insert(n)

    sorted_numbers = []
    while len(heap) != 0:
        sorted_numbers.append(heap.delete_min().key)

    assert all(sorted_numbers[i] <= sorted_numbers[i+1] for i in range(len(sorted_numbers)-1))

