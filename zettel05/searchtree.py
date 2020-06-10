import pytest

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

    def __getitem__(self, key):          # implements 'value = tree[key]'
        return _tree_find(self._root, key)._value

    def __setitem__(self, key, value):   # implements 'tree[key] = value'
        self._root = self._tree_insert(self._root, key, value)
        self._size += 1         #TODO only increase size when key is new

    def __delitem__(self, key):          # implements 'del tree[key] '
        self._tree_remove(self._root, key)
        self._size -= 1

    @staticmethod
    def _tree_find(node, key):           # internal implementation
        if node is None:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return _tree_find(node._left, key)
        else:
            return _tree_find(node._right, key)

    @staticmethod
    def _tree_insert(node, key, value):
        # not a static method anymore bc we need to access self._size
        if node is None:
            a = SearchTree.Node(key, value)
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
    def _tree_replacment(node):
        # Walk to the smallest key on the right side
        node = node._right
        while node._left is not None:
            node = node._left
        return node

    @staticmethod
    def _tree_remove(node, key):         # internal implementation
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
                repl = SearchTree._tree_replacment(node)
                node._key = repl._key
                node._value = repl._value
                node._right = SearchTree._tree_remove(node._right, repl._key)

        return node

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
        print(nested_list)
        depth_list = SearchTree._get_depth_list(nested_list)
        parent_dict = SearchTree._get_parent_key_dict(nested_list)

        padding = {elem[0]: 0 for level in depth_list for elem in level}
        for elem in depth_list[-1]:
            padding[elem[0]] = 1

        last_parent_key = None
        for level in depth_list[:0:-1]:
            for elem in level:
                parent_key = parent_dict[elem[0]]
                padding[parent_key] += padding[elem[0]] + ((len(str(elem))) // 2 + 1 if last_parent_key == parent_key else 0)
                last_parent_key = parent_key

        outstring = 'Binary search tree:\n'
        for level in depth_list:
            outstring += ''.join(' ' * padding[elem[0]] + str(elem) + ' ' * padding[elem[0]] for elem in level) + '\n'
        return outstring


def test_search_tree():
    t = SearchTree()
    assert len(t) == 0

def main():
    a = SearchTree()
    a[50] = 'a'
    a[20] = 'b'
    a[70] = 'c'
    a[15] = 'd'
    a[30] = 'e'
    a[60] = 'f'
    a[80] = 'g'
    a[10] = 'h'
    a[55] = 'i'
    a[65] = 'j'
    a[25] = 'k'
    a[35] = 'l'
    print(a)
    del a[30]
    print(a)

if __name__ == '__main__':
    main()
