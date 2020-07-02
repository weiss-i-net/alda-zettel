import pytest
import random

class TreapBase:
    class Node:
        def __init__(self, key, value, priority):
            self._key = key
            self._value = value
            self._left = self._right = None
            self._priority = priority

    def __init__(self):
        self._root = None
        self._size = 0
        self._is_dynamic_treap = False

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        node = TreapBase._tree_find(self._root, key, self._is_dynamic_treap)
        if node is None:
            raise KeyError(f'__getitem__: Theres no Node with key {key}')
        return node._value

    def __setitem__(self, key, value):
        # This is an inefficient way to determine whether the size has changed,
        # since that information is already available inside self._tree_insert
        # but for the sake of readabilty its done this way.
        # tree_find is called with is_dynamic_Tree = False since the prio will
        # already be increased in _tree_insert
        if TreapBase._tree_find(self._root, key, False) is None:
            self._size += 1

        self._root = TreapBase._tree_insert(self._root, key, value, self._is_dynamic_treap)

    def __delitem__(self, key):
        self._tree_remove(self._root, key)
        self._size -= 1

    def depth(self):
        return TreapBase._tree_depth(self._root)

    # rotate the right child to the top, search tree is preserved
    @staticmethod
    def _tree_rotate_left(old_root):
        new_root = old_root._right
        old_root._right = new_root._left
        new_root._left = old_root
        return new_root

    # rotate the left child to the top, search tree is preserved
    @staticmethod
    def _tree_rotate_right(old_root):
        new_root = old_root._left
        old_root._left = new_root._right
        new_root._right = old_root
        return new_root

    @staticmethod
    def _fix_local_prio(node):
        if node._left is not None and node._left._priority > node._priority:
            node = TreapBase._tree_rotate_right(node)
        elif node._right is not None and node._right._priority > node._priority:
            node = TreapBase._tree_rotate_left(node)
        TreapBase.print_node(node)

    @staticmethod
    def _tree_find(node, key, is_dynamic_treap):
        if node is None:
            return None
        if node._key == key:
            if is_dynamic_treap:
                node._priority += 1
            return node

        if key < node._key:
            result = TreapBase._tree_find(node._left, key, is_dynamic_treap)
        else:
            result = TreapBase._tree_find(node._right, key, is_dynamic_treap)

        if is_dynamic_treap:
            node = TreapBase._fix_local_prio(node)

        return result

    @staticmethod
    def _tree_insert(node, key, value, is_dynamic_treap):
        if node is None:
            if is_dynamic_treap:
                return TreapBase.Node(key, value, 1)
            return TreapBase.Node(key, value, random.randint(0, 1000))

        if node._key == key:
            node._value = value
            if is_dynamic_treap:
                node._priority += 1
            return node

        if key < node._key:
            node._left = TreapBase._tree_insert(node._left, key, value, is_dynamic_treap)
        else:
            node._right = TreapBase._tree_insert(node._right, key, value, is_dynamic_treap)

        TreapBase.print_node(node)
        node = TreapBase._fix_local_prio(node)
        TreapBase.print_node(node)

        return node

    @staticmethod
    def _tree_replacement(node):
        # Walk to the smallest key on the right side
        node = node._right
        while node._left is not None:
            node = node._left
        return node

    @staticmethod
    def _fix_prio_down(node):
        if node is None:
            return node
        if node._left is not None and node._left._priority > node._priority:
            node = _tree_rotate_right(node)
            node._left = TreapBase._fix_prio(node._left)
        elif node._right is not None and node._right._priority > node._priority:
            node = _tree_rotate_left(node)
            node._right = TreapBase._fix_prio(node._right)
        return node

    @staticmethod
    def _tree_remove(node, key):
        # Walk the tree until node is found or not existant
        if node is None:
            raise KeyError(f'Theres no Node with key {key}, so none can be removed')
        if key < node._key:
            node._left = TreapBase._tree_remove(node._left, key)
        elif key > node._key:
            node._right = TreapBase._tree_remove(node._right, key)

        # Deal with preservering search tree after removal
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
                repl = TreapBase._tree_replacement(node)
                node._key = repl._key
                node._value = repl._value
                node._right = TreapBase._tree_remove(node._right, repl._key)

            # restore prio-condition
            node = TreapBase._fix_prio_down(node)

        return node

    @staticmethod
    def _tree_depth(node):
        if node is None:
            return 0
        else:
            return 1 + max(TreapBase._tree_depth(node._left), TreapBase._tree_depth(node._right))


###############################################################################
#          Attempt to print the tree, not part of the excercise               #
###############################################################################

    @staticmethod
    def _get_nested_tree_list(node):
        if node is None:
            return
        tree_list = [node._key, node._value, node._priority]
        tree_list.append(TreapBase._get_nested_tree_list(node._left))
        tree_list.append(TreapBase._get_nested_tree_list(node._right))
        return tree_list

    @staticmethod
    def _get_depth_list(nested_list):
        depth_list = []
        def append_level(curr_elem, curr_depth):
            if curr_elem is None:
                return
            if len(depth_list) <= curr_depth:
                depth_list.append([])
            depth_list[curr_depth].append((curr_elem[0], curr_elem[1], curr_elem[2]))
            append_level(curr_elem[3], curr_depth + 1)
            append_level(curr_elem[4], curr_depth + 1)
        append_level(nested_list, 0)
        return depth_list

    @staticmethod
    def _get_parent_key_dict(nested_list):
        parent_dict = {}
        def append_childs(curr_elem):
            for child in (curr_elem[3], curr_elem[4]):
                if child is not None:
                    parent_dict[child[0]] = curr_elem[0]
                    append_childs(child)

        append_childs(nested_list)
        return parent_dict

    @staticmethod
    def print_node(node):
        nested_list = TreapBase._get_nested_tree_list(node)
        depth_list  = TreapBase._get_depth_list(nested_list)
        print(nested_list, depth_list)
        parent_dict = TreapBase._get_parent_key_dict(nested_list)

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
        print(outstring)

###############################################################################
class DynamicTreap(TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self._is_dynamic_treap = True

class RandomTreap(TreapBase):
    def __init__(self):
        self._root = None
        self._size = 0
        self._is_dynamic_treap = False

a = DynamicTreap()
a[2] = 2
a[6] = 6
a[1] = 1
print(a)
a[3] = 3
a[5] = 5
a[7] = 7
print(a)
del a[6]
print(a)
print(a[1])
print(a._root._priority)
print(a)
print(a[1])
print(a)
print(a._root._priority)
