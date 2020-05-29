from DequeArray import DequeArray
import copy
import doctest
import pytest

###############################################################################

# Fixtures

def n_elem_DequeArray(n):
    a = DequeArray()
    for i in range(n):
        a.push("test-elem " + str(i))
    return a

@pytest.fixture
def empty_DequeArray():
    return n_elem_DequeArray(0)

@pytest.fixture
def one_elem_DequeArray():
    return n_elem_DequeArray(1)

@pytest.fixture
def two_elem_DequeArray():
    return n_elem_DequeArray(2)

@pytest.fixture
def at_capacity_DequeArray():
    a = n_elem_DequeArray(8)
    assert a.size() == a.capacity()
    return a

@pytest.fixture
def big_DequeArray():
    return n_elem_DequeArray(2000)

all_fixtures = ['empty_DequeArray',    'one_elem_DequeArray',
                'two_elem_DequeArray', 'at_capacity_DequeArray',
                'big_DequeArray']

# fixture that is parametrized as all other fixtures
@pytest.fixture(params=all_fixtures)
def allfixt(request):
    return request.getfixturevalue(request.param)


################################################################################

# Tests

def test_empty_container_has_size_zero(empty_DequeArray):
    assert empty_DequeArray.size() == 0

def test_size_lt_eq_capacity(allfixt):
    assert allfixt.size() <= allfixt.capacity()

def test_push(allfixt):
    array_copy = copy.deepcopy(allfixt)

    # (i)
    pre_size = allfixt.size()
    new_elem = "Testelem"
    allfixt.push(new_elem)
    assert allfixt.size() == pre_size + 1

    # (ii)
    assert allfixt.last() == new_elem

    # (iii)
    for old_elem, new_elem in zip(array_copy, allfixt):
        assert old_elem == new_elem

    # (iv)
    if array_copy.size() == 0:
        assert allfixt.first() == new_elem
    else:
        assert allfixt.first() == array_copy.first()

    # (v)
    allfixt.pop_last()
    assert allfixt == array_copy

def test_set_elem(allfixt):
    if allfixt.size() == 0:
        return

    # Testing edge-cases and one element in the middle
    for index in [0, allfixt.size() // 2, allfixt.size() - 1]:
        array_copy = copy.deepcopy(allfixt)

        allfixt[index] = "bla" * (index % 5 + 1)

        assert array_copy.size() == allfixt.size()

        for i in [o for o in range(allfixt.size()) if o != index]:
            assert array_copy[i] == allfixt[i]

def test_pop_last(allfixt):
    # (iii)
    if (allfixt.size() == 0):
        with pytest.raises(Exception):
            allfixt.pop_last()
    else:
        array_copy = copy.deepcopy(allfixt)
        allfixt.pop_last()

        # (i)
        assert array_copy.size() - 1 == allfixt.size()

        # (ii)
        for i in range(allfixt.size() - 1):
            assert array_copy[i] == allfixt[i]

def test_pop_first(allfixt):
    # (iii)
    if (allfixt.size() == 0):
        with pytest.raises(Exception):
            allfixt.pop_first()
    else:
        array_copy = copy.deepcopy(allfixt)
        allfixt.pop_first()

        # (i)
        assert array_copy.size() - 1 == allfixt.size()

        # (ii)
        for i in range(allfixt.size() - 1):
            assert array_copy[i + 1] == allfixt[i]

def test_first_last(allfixt):
    if (allfixt.size() == 0):
        return

    # (i)
    assert allfixt.first() == allfixt[0]

    # (ii)
    assert allfixt.last() == allfixt[allfixt.size() - 1]

# Doctest
def test_doctests():
    # import here because doctest requires the entire module and the tests
    # above are written with the DequeArray class in global namespace
    # (from x import y syntax)
    import DequeArray
    doctest.testmod(DequeArray)
