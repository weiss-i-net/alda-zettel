import pytest
import random

class SearchTree:
    class Node:
        def __init__(self, key, value):
            self._key = key
            self._value = value
            self._left = self._right = None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        node = SearchTree._tree_find(self._root, key)
        if node is None:
            raise KeyError(f'__getitem__: Theres no Node with key {key}')
        return node._value

    def __setitem__(self, key, value):
        # This is an inefficient way to determine whether the size has changed,
        # since that information is already available inside self._tree_insert
        # but for the sake of readabilty its done this way
        if SearchTree._tree_find(self._root, key) is None:
            self._size += 1

        self._root = SearchTree._tree_insert(self._root, key, value)

    def __delitem__(self, key):
        self._tree_remove(self._root, key)
        self._size -= 1

    def depth(self):
        return SearchTree._tree_depth(self._root)

    @staticmethod
    def _tree_find(node, key):
        if node is None:
            return None
        if node._key == key:
            return node
        if key < node._key:
            return SearchTree._tree_find(node._left, key)
        else:
            return SearchTree._tree_find(node._right, key)

    @staticmethod
    def _tree_insert(node, key, value):
        if node is None:
            return SearchTree.Node(key, value)
        if node._key == key:
            node._value = value
            return node
        if key < node._key:
            node._left = SearchTree._tree_insert(node._left, key, value)
        else:
            node._right = SearchTree._tree_insert(node._right, key, value)
        return node

    @staticmethod
    def _tree_replacement(node):
        # Walk to the smallest key on the right side
        node = node._right
        while node._left is not None:
            node = node._left
        return node

    @staticmethod
    def _tree_remove(node, key):
        # Walk the tree until node is found or not existant
        if node is None:
            raise KeyError(f'Theres no Node with key {key}, so none can be removed')
        if key < node._key:
            node._left = SearchTree._tree_remove(node._left, key)
        elif key > node._key:
            node._right = SearchTree._tree_remove(node._right, key)

        # Deal with preservering tree after removal
        else:
            # If node is leaf: no problemo
            if node._left is None and node._right is None:
                node = None

            # if node has only one child, replace it with that child
            elif (node._right is None) != (node._left is None):
                node = node._right if node._left is None else node._left

            # if it has 2 childs, find a suitable replacment
            # (in this case smallest decendent of the right child)
            else:
                repl = SearchTree._tree_replacement(node)
                node._key = repl._key
                node._value = repl._value
                node._right = SearchTree._tree_remove(node._right, repl._key)

        return node

    @staticmethod
    def _tree_depth(node):
        if node is None:
            return 0
        else:
            return 1 + max(SearchTree._tree_depth(node._left), SearchTree._tree_depth(node._right))


###############################################################################
#          Attempt to print the tree, not part of the excercise               #
###############################################################################

    @staticmethod
    def _get_nested_tree_list(node):
        if node is None:
            return
        tree_list = [node._key, node._value]
        tree_list.append(SearchTree._get_nested_tree_list(node._left))
        tree_list.append(SearchTree._get_nested_tree_list(node._right))
        return tree_list

    @staticmethod
    def _get_depth_list(nested_list):
        depth_list = []
        def append_level(curr_elem, curr_depth):
            if curr_elem is None:
                return
            if len(depth_list) <= curr_depth:
                depth_list.append([])
            depth_list[curr_depth].append((curr_elem[0], curr_elem[1]))
            append_level(curr_elem[2], curr_depth + 1)
            append_level(curr_elem[3], curr_depth + 1)
        append_level(nested_list, 0)
        return depth_list

    @staticmethod
    def _get_parent_key_dict(nested_list):
        parent_dict = {}
        def append_childs(curr_elem):
            for child in (curr_elem[2], curr_elem[3]):
                if child is not None:
                    parent_dict[child[0]] = curr_elem[0]
                    append_childs(child)

        append_childs(nested_list)
        return parent_dict

    def __str__(self):
        nested_list = SearchTree._get_nested_tree_list(self._root)
        depth_list = SearchTree._get_depth_list(nested_list)
        parent_dict = SearchTree._get_parent_key_dict(nested_list)

        padding = {elem[0]: 0 for level in depth_list for elem in level}
        for elem in depth_list[-1]:
            padding[elem[0]] = 1

        last_parent_key = None
        for level in depth_list[:0:-1]:
            for elem in level:
                parent_key = parent_dict[elem[0]]
                padding[parent_key] += padding[elem[0]] + (len(str(elem)) // 2 + 1 if last_parent_key == parent_key else 0)
                last_parent_key = parent_key

        outstring = 'Binary search tree:\n'
        for level in depth_list:
            outstring += ''.join(' ' * padding[elem[0]] + str(elem) + ' ' * padding[elem[0]] for elem in level) + '\n'
        return outstring

###############################################################################

# Aufgabe 1 c)
#
# If we are try to get a tree with minimum depth, we must try to insert the element to
# make the tree a  balanced tree.  We could make the list first sorted in ascending order. After that, we could
# choose the element in the middle as our root and insert it. After that we could make the remaining part,
# left and right, to be a sublist. And the middle element of each sublist would be our left child and right child.
# After some iterations, we could get a balanced tree.

###############################################################################
#                                  Testing                                    #
###############################################################################


# Fixtures

@pytest.fixture
def empty():
    return SearchTree()

@pytest.fixture
def one_elem():
    a = SearchTree()
    a[0] = 'Elem 0'
    return a

@pytest.fixture
def sorted_0_99():
    a = SearchTree()
    for i in range(100):
        a[i] = 'Elem ' + str(i)
    return a

@pytest.fixture(params=range(5))
def random_permutations_0_99():
    a = SearchTree()
    permu = list(range(100))
    random.shuffle(permu)
    for i in permu:
        a[i] = 'Elem ' + str(i)
    return a

@pytest.fixture()
def alotta_random_elems():
    a = SearchTree()
    for i in range(100000):
        num = random.randint(-10000, 10000)
        a[num] = 'Elem ' + str(num)
    return a

def get_balanced_tree(depth):
    a = SearchTree()
    for exp in range(depth, -1, -1):
        for i in range(2**exp, 2**depth, 2**exp):
            # elems get overwritten here, thats fine since they dont change their position in the tree
            a[i] = ' Elem ' + str(i)
    return a

@pytest.fixture
def balanced_tree_127():
    return get_balanced_tree(7)


# Tests

def test_len(empty, one_elem, sorted_0_99, random_permutations_0_99, alotta_random_elems, balanced_tree_127):
    assert len(empty) == 0
    assert len(one_elem) == 1
    assert len(sorted_0_99) == 100
    assert len(random_permutations_0_99) == 100
    assert 0 < len(alotta_random_elems) <= 20000
    assert len(balanced_tree_127) == 127

def test_getitem_(empty, one_elem, sorted_0_99, random_permutations_0_99):
    with pytest.raises(KeyError):
        empty[0]
    with pytest.raises(KeyError):
        one_elem[1]
    with pytest.raises(KeyError):
        sorted_0_99[100]
    with pytest.raises(KeyError):
        random_permutations_0_99[100]

    assert one_elem[0] == 'Elem 0'
    for i in range(100):
        assert sorted_0_99[i] == 'Elem ' + str(i)
        assert random_permutations_0_99[i] == 'Elem ' + str(i)

def test_setitem_(empty, one_elem, sorted_0_99, random_permutations_0_99, alotta_random_elems):
    empty[0] = 'setitem 0'
    assert empty[0] == 'setitem 0'
    assert len(empty) == 1

    one_elem[0] = 'setitem 0'
    assert one_elem[0] == 'setitem 0'
    assert len(one_elem) == 1

    one_elem[1] = 'setitem 1'
    assert one_elem[1] == 'setitem 1'
    assert len(one_elem) == 2

    for i in range(100):
        sorted_0_99[i] = random_permutations_0_99[i] = 'setitem ' + str(i)
        assert sorted_0_99[i] == random_permutations_0_99[i] == 'setitem ' + str(i)
    assert len(random_permutations_0_99) == len(sorted_0_99) == 100

    sorted_0_99[100] = random_permutations_0_99[100] = 'setitem 100'
    assert sorted_0_99[100] == random_permutations_0_99[100] == 'setitem 100'
    assert len(random_permutations_0_99) == len(sorted_0_99) == 101

    alotta_len = len(alotta_random_elems)
    alotta_random_elems[0] = 'setitem 0'
    assert alotta_random_elems[0] == 'setitem 0'
    assert len(alotta_random_elems) == alotta_len or len(alotta_random_elems) == alotta_len + 1

    alotta_len = len(alotta_random_elems)
    alotta_random_elems[10001] = 'setitem 10001'
    assert alotta_random_elems[10001] == 'setitem 10001'
    assert len(alotta_random_elems) == alotta_len + 1

def test_delitem_(empty, one_elem, sorted_0_99, random_permutations_0_99, balanced_tree_127):
    with pytest.raises(KeyError):
        del empty[0]

    with pytest.raises(KeyError):
        del one_elem[1]
    del one_elem[0]
    assert len(one_elem) == 0

    with pytest.raises(KeyError):
        del sorted_0_99[-1]
    with pytest.raises(KeyError):
        del random_permutations_0_99[-1]
    for i in range(100):
        del sorted_0_99[i], random_permutations_0_99[i]
        assert len(sorted_0_99) == len(random_permutations_0_99) == 99 - i

    del balanced_tree_127[64]
    assert balanced_tree_127._root._key == 65

def test_depth(empty, one_elem, sorted_0_99, balanced_tree_127):
    assert empty.depth() == 0
    assert one_elem.depth() == 1
    assert sorted_0_99.depth() == 100
    assert balanced_tree_127.depth() == 7

    balanced_tree_127[128] = 'Elem 128'
    assert balanced_tree_127.depth() == 8
