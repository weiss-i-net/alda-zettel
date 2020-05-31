import copy
import doctest

class DequeArray:

    def __init__(self):
        """Initializes an empty array

        >>> a = DequeArray()
        """

        self._size = 0
        self._capacity = 1
        self._data = [None]

        # data-index of element with circular index of 0
        self._start = 0

    @classmethod
    def from_list(cls, init_list):
        """Initializes DequeArray with a copy of the elements of an iterable.

        >>> a = DequeArray.from_list([1, 2, 3])
        >>> print(a)
        [1, 2, 3]
        """
        # Instantiate empty DequeArray
        obj = cls()
        obj._size = obj._capacity = len(init_list)

        # Allocate memory for ini_list elements
        obj._data = [None]*obj._capacity

        # Copy the elements
        for data_index, init_elem in enumerate(init_list):
            obj._data[data_index] = copy.deepcopy(init_elem)
        return obj

    # For accessing the elements of _data as a circular buffer
    def _set(self, index, value):
        self._data[(self._start + index) % self._capacity] = value

    def _get(self, index):
        return self._data[(self._start + index) % self._capacity]

    def size(self):
        """Return the amount of elements in the DequeArray.

        >>> array = DequeArray()
        >>> array.push('Test')
        >>> array.size()
        1
        """
        return self._size

    # To allow len(DequeArray)
    def __len__(self):
        """Return the size of the array

        >>> array = DequeArray()
        >>> array.push(93729)
        >>> len(array)
        1
        """
        return self._size

    def capacity(self):
        """Return the current capacity of the DequeArray.

        The capacity doubles when the array is full and a new element is
        pushed.

        >>> array = DequeArray()
        >>> for i in range(10):
        ...     array.push('test')
        >>> array.capacity()
        16
        """

        return self._capacity

    def push(self, item):
        """Append 'item' to the end of the array.

        If the array is full, it is moved to a new location with double
        capacity.

        >>> array = DequeArray()
        >>> array.push(True)
        >>> array.push(978987)
        >>> array.push('Test')
        >>> array.last()
        'Test'
        >>> array.capacity()
        4
        """

        # If capacity is reached create a new array and copy _data
        if self._capacity == self._size:
            self._capacity *= 2

            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._get(i)

            self._data = new_data

            # The new copy has its circular buffer starting at 0 again
            self._start = 0

        # Insert item at the end
        self._set(self._size, item)
        self._size += 1

    def pop_first(self):
        """Remove and return the first element.

        If the array is empty raise an exception.

        >>> array = DequeArray()
        >>> array.push('Test')
        >>> array.pop_first()
        'Test'
        >>> array.size()
        0
        >>> array.pop_last()
        Traceback (most recent call last):
        RuntimeError: array is empty
        """

        if self._size == 0:
            raise RuntimeError('array is empty')

        first_elem = self._get(0)
        self._start = (self._start + 1) % self._size
        self._size -= 1
        return first_elem

    def pop_last(self):
        """Remove and return the first element.

        If the array is empty raise an exception.

        >>> array = DequeArray()
        >>> array.push('Test')
        >>> array.pop_last()
        'Test'
        >>> array.size()
        0
        >>> array.pop_last()
        Traceback (most recent call last):
        RuntimeError: array is empty
        """

        if self._size == 0:
            raise RuntimeError('array is empty')

        self._size -= 1
        return self._get(self._size)

    def __getitem__(self, index):
        """Return item at index with bound-checking.

        >>> array = DequeArray()
        >>> array.push('test')
        >>> array[0]
        'test'
        >>> array[100]
        Traceback (most recent call last):
        RuntimeError: index out of range
        """

        if index < 0 or index >= self._size:
            raise RuntimeError('index out of range')
        return self._get(index)

    def __setitem__(self, index, v):      # __setitem__ implements c[index] = v
        """Set item at index to v with bound-checking

        >>> array = DequeArray()
        >>> array.push('test')
        >>> array[0] = 10
        >>> array[0]
        10
        >>> array[100] = 10
        Traceback (most recent call last):
        RuntimeError: index out of range
        """

        if index < 0 or index >= self._size:
            raise RuntimeError('index out of range')
        self._set(index, v)

    def first(self):
        """Return the first element.

        >>> a = DequeArray()
        >>> a.first()
        Traceback (most recent call last):
        RuntimeError: array is empty
        >>> a.push('Test')
        >>> a.push('abc')
        >>> a.first()
        'Test'
        """
        if self._size == 0:
            raise RuntimeError('array is empty')
        return self._get(0)

    def last(self):
        """Return last element.

        >>> a = DequeArray()
        >>> a.last()
        Traceback (most recent call last):
        RuntimeError: array is empty
        >>> a.push('abc')
        >>> a.push('Test')
        >>> a.last()
        'Test'
        """
        if self._size == 0:
            raise RuntimeError('array is empty')
        return self._get(self._size - 1)

    def __ne__(self, other):
        """Return True, if the size or any of the elements differ.

        >>> a = DequeArray()
        >>> a.push('A')
        >>> b = DequeArray()
        >>> b.push('A')
        >>> b != a
        False
        >>> b.push('B')
        >>> b != a
        True
        >>> a.push('C')
        >>> b != a
        True
        """
        if self._size != other._size:
            return True
        for i in range(self._size):
            if other[i] != self[i]:
                return True
        return False

    def __eq__(self, other):
        """Return True, if the size and all of the elements are the same.

        Defined in Terms of __ne__ instead of the other way around, so __ne__
        can return early if e.g. the size is diffrent

        >>> a = DequeArray()
        >>> a.push('A')
        >>> b = DequeArray()
        >>> b.push('A')
        >>> b == a
        True
        >>> b.push('B')
        >>> b == a
        False
        >>> a.push('C')
        >>> b == a
        False
        """

        return not (self != other)

    # Iterator methods
    def __iter__(self):
        """Allows iteration over the array.

        See __next__().
        """
        # -1 so the index after the first __next__ call is 0
        self._iter_index = -1
        return self

    def __next__(self):
        """Allows iteration over the array.

        >>> a = DequeArray()
        >>> a.push('A')
        >>> a.push('B')
        >>> for elem in a:
        ...     print(elem)
        A
        B
        """

        self._iter_index += 1
        if self._iter_index == self._size:
            raise StopIteration
        return self._get(self._iter_index)

    # To allow print(DequeArray)
    def __str__(self):
        """Return string representation of the DequeArray.

        Uses python list formating.

        >>> a = DequeArray()
        >>> a.push('A')
        >>> a.push('B')
        >>> print(a)
        [A, B]
        """
        repr_string = "["
        for elem in self:
            repr_string += str(elem) + ", "
        return repr_string[:-2] + "]"

class SlowDequeArray(DequeArray):
    def push(self, elem):
        """Append 'item' to the end of the array.

        If the array is full, it is moved to a new location with 1 more slot.

        >>> array = SlowDequeArray()
        >>> array.push(True)
        >>> array.push(978987)
        >>> array.push('Test')
        >>> array.last()
        'Test'
        >>> array.capacity()
        3
        """
        # If capacity is reached create a new array and copy _data
        if self._capacity == self._size:
            # Size is only increased by 1 instead of doubled
            self._capacity += 1

            new_data = [None] * self._capacity
            for i in range(self._size):
                new_data[i] = self._get(i)

            self._data = new_data

            # The new copy has its circular buffer starting at 0 again
            self._start = 0

        # Insert elem at the end
        self._set(self._size, elem)
        self._size += 1

if __name__ == '__main__':
    doctest.testmod()
