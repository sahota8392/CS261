# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Part 2 Dynamic Array
# Due Date: 11/06/23
# Description: Implementation of Stack ADT utilizing Dynamic Array

# import dynamic_array file from A2
from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adds new element to the top of the stack - O(1) amortized
        """
        # call Dynamic Array 'insert_at_index' to insert value with length of list to stack on top
        self._da.insert_at_index(self._da.length(), value)

    def pop(self) -> object:
        """
        Removes top element from stack and returns that value.
        Raise exception for an empty stack - O(1) amortized
        """
        # if dynamic array is empty, raises exception
        if self._da.is_empty():
            raise StackException

        # assign index of top element to X and get value of X
        x = self._da.length() - 1
        top_element = self._da.get_at_index(x)

        # removes the top element in stack
        self._da.remove_at_index(self._da.length() - 1)
        return top_element

    def top(self) -> object:
        """
        Return value of top element of stack without removal.
        If empty stack, raise an exception - O(1)
        """
        # if empty stack, exception is raised
        if self._da.is_empty():
            raise StackException

        # return the top element in stack without any changes
        x = self._da.length() - 1
        top_element = self._da.get_at_index(x)
        return top_element


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)
