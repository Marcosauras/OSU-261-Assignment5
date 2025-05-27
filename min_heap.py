# Name: Marc Hamilton
# OSU Email: hamimarc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 5: MinHeap Implementation
# Due Date: 5/26/2025
# Description: MinHeap functionality Implementation

from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds a node to the MinHeap and sorts to make sure that the MinHeap follows

        :param node: an object that is being added to the MinHeap
        """
        # adds the new node to the end of the heap
        self._heap.append(node)
        child_index = self._heap.length() - 1

        # checks to make sure we are not at the root
        while child_index > 0:
            parent = (child_index - 1) // 2
            # checks to make sure that the current node is less than it's parents
            if self._heap.get_at_index(child_index) < self._heap.get_at_index(parent):
                # swaps the nodes by saving the old values first and then setting their new index.
                curr_node = self._heap.get_at_index(child_index)
                parent_node = self._heap.get_at_index(parent)
                self._heap.set_at_index(child_index, parent_node)
                self._heap.set_at_index(parent, curr_node)
            # resets the child index to the current parent
            child_index = parent

    def is_empty(self) -> bool:
        """
        Checks if the MinHeap is empty and returns a True or False value

        :return: A boolean that represents if the Minheap is empty, true if it is empty, false if it is not.
        """
        return self._heap.length() == 0

    def get_min(self) -> object:
        """
        grabs the min value in the MinHeap and returns it without editing the MinHeap

        :return: an object that represents the node with the min value in the MinHeap
        """
        if self.is_empty():
            raise MinHeapException("This Heap Is Empty")
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns and removes the min value from the MinHeap

        :returns: An object that represents the node with the min value in the MinHeap
        """
        if self.is_empty():
            raise MinHeapException("This Heap Is Empty")

        min_val = self._heap.get_at_index(0)
        # sets the last element as the new root of the MinHeap
        last_index = self._heap.length() - 1
        last_element = self._heap.get_at_index(last_index)
        self._heap.set_at_index(0, last_element)
        # removes the last element to complete the move
        self._heap.remove_at_index(last_index)
        # resorts the MinHeap by percolating the new root down
        _percolate_down(self._heap, 0, self._heap.length())
        return min_val

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a MinHeap from an unsorted DynamicArray

        :param da: Represents the DynamicArray being added to the heap
        """

        self._heap = DynamicArray()
        # copies DynamicArray into a Heap
        for i in range(da.length()):
            self._heap.append(da.get_at_index(i))
        # finds the last node that is not a leaf
        last_non_leaf = (self._heap.length() - 2) // 2
        for i in range(last_non_leaf, -1, -1):
            _percolate_down(self._heap, i, self._heap.length())

    def size(self) -> int:
        """
        Gives the size of the Heap

        :return: An Integer that represents the size of the Heap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears a MinHeap by creating a blank one and overwriting the old one
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Sorts a DynamicArray in non-ascending order using the heapsort algorithm

    :param da: The DynamicArray being inputted to be sorted using heapsort
    """
    size = da.length()
    # finds the last not leaf node and percolates down
    for i in range((size - 2) // 2, -1, -1):
        _percolate_down(da, i, size)
    # Moves the min element to the end, then restores the heap properties on the reduced heap
    for i in range(size - 1, 0, -1):
        min_val = da.get_at_index(0)
        da.set_at_index(0, da.get_at_index(i))
        da.set_at_index(i, min_val)
        _percolate_down(da, 0, i)


# It's highly recommended that you implement the following optional          #
# helper function for percolating elements down the MinHeap. You can call    #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int, size: int) -> None:
    """
    Percolates down the inputted element at the given parent index

    :param da: Represents a dynamicArray that is having its value percolated down
    :parent int: represent the integer that is the parent being percolated down
    :param size: represents the size of the array
    """
    left = 2 * parent + 1
    right = 2 * parent + 2

    while left < size:
        smallest = parent
        # compares the left and right to find the smallest value
        if da.get_at_index(left) < da.get_at_index(smallest):
            smallest = left

        # Checks if the right is strictly the smallest value out of the left and right
        if right < size and da.get_at_index(right) < da.get_at_index(smallest):
            smallest = right

        # Checks if the heap property has been satisfied
        if smallest == parent:
            parent = size
        else:
            # swaps the nodes by saving the old values first and then setting their new index.
            parent_val = da.get_at_index(parent)
            child_val = da.get_at_index(smallest)
            da.set_at_index(parent, child_val)
            da.set_at_index(smallest, parent_val)
            parent = smallest

        left = 2 * parent + 1
        right = 2 * parent + 2


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
