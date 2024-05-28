# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 5 MinHeap Implementation
# Due Date: 11/29/2023
# Description: Implement MinHeap class with Dynamic Array
import math

# import dynamic_array file from A2
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

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Add new object to MinHeap while maintaining heap property - O(log n)
        """

        self._heap.append(node)                 # call Dynamic append method
        new_node = self._heap.length() - 1      # assign new node appended to list

        while new_node > 0:                     # check if it's inbounds
            parent_node = (new_node - 1) // 2   # assign the parent node

            # if new node is less than parent, swap them both
            if self._heap[new_node] < self._heap[parent_node]:
                self._heap[new_node], self._heap[parent_node] = self._heap[parent_node], self._heap[new_node]
                new_node = parent_node          # updates new node to parent
            else:
                return

    def is_empty(self) -> bool:
        """
        Returns True if empty heap else False - O(1)
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        Returns object with minimum key without removal of object from heap.
        Empty heap raises exception - O(1)
        """
        if self.is_empty():                     # raise exception if heap is empty
            raise MinHeapException
        else:
            return self._heap.get_at_index(0)   # returns root of heap as the minimum value

    def remove_min(self) -> object:
        """
        Returns object with min key and removes from heap (Root is the minimum).
        Empty heap raises exception.
        If both children of node have equal value & smaller than node, swap with left child - O(log n)
        """
        if self.is_empty():
            raise MinHeapException

        root_node = self._heap.get_at_index(0)      # root node is the min in the heap
        last_node = self._heap.length() - 1         # assign the last node in the heap

        # last node replaces the root node removing it
        self._heap[0], self._heap[last_node] = self._heap[last_node], self._heap[0]
        self._heap.remove_at_index(last_node)

        # percolate down the heap and rearrange nodes
        _percolate_down(self._heap, 0, self._heap.length())      # call percolate down since outside of class
        return root_node

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives Dynamic Array and builds proper MinHeap overwriting current MinHeap. - O(N).
        """
        heap_size = da.length() // 2 - 1
        self._heap = DynamicArray(da)               # Copy the content of the DynamicArray

        # iterate through heap and call percolate down function
        for i in range(heap_size, -1, -1):
            _percolate_down(self._heap, i, da.length())

    def size(self) -> int:
        """
        Returns number of items currently stored in the heap - O(1)
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap.
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Receives DA and sorts content in non-ascending order using Heapsort algorithm.
    Sort array in place without creating any data structures, returns nothing - O(n log n)
    """
    da_size = da.length()

    # builds the heap
    for i in range((da_size // 2 - 1), -1, -1):
        _percolate_down(da, i, da_size)

    k = da_size - 1                                     # k is set to the last element
    last_node = da.length()                             # assign the last node in the heap

    # iterate until k reaches beginning of array
    for last_node in range(da_size - 1, 0, -1):
        da[0], da[last_node] = da[last_node], da[0]     # swap first and last element
        k -= 1                                          # decrement K by 1
        last_node -= 1
        _percolate_down(da, 0, last_node+1)      # last node +1 as decrement occurs in initial


def _percolate_down(da: DynamicArray, parent: int, k: int) -> None:
    """
    Percolate down the tree.
    """

    while True:                                                             # variables assigned
        left_child = (2 * parent) + 1
        right_child = (2 * parent) + 2
        min_node = parent

        if left_child < k and da[left_child] < da[min_node]:      # compares left_child to min
            min_node = left_child
        if right_child < k and da[right_child] < da[min_node]:    # compares right_child to min
            min_node = right_child

        if min_node != parent:                                              # if min is not parent, swap and update
            da[parent], da[min_node] = da[min_node], da[parent]             # parent swaps with min child
            parent = min_node
        else:                                                               # no change needed
            return


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
