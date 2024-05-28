# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2 Dynamic Array and ADT Implementation
# Due Date: 10/30/23
# Description: Implement various methods of Dynamic array and Bag ADT


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Utilize append from Dynamic Array to add to the bag
        """
        # use Dynamic Array append method to add to bag
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Remove one element from bag that matches provided value returning True if removed else False
        """
        # Use Dynamic Array remove_at_index to remove elements that match value
        for i in range(self._da.length()):
            if self._da.get_at_index(i) == value:
                self._da.remove_at_index(i)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Return number of elements in bag matching provided value.
        """
        # Use Dynamic Array filter method to iterate and perform the 'filter_func' to count same_element
        same_element = self._da.filter(lambda x: x == value)
        count = same_element.length()
        return count

    def clear(self) -> None:
        """
        Removes all elements from the bag to an empty bag
        """
        # reassign an empty dynamic array to empty bag
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        Compare 2 bag contents returning True if bags contain same NUMBER of elements and SAME ELEMENTS.
        Empty bags are considered True.
        """
        # if length of the two bags is not the same, return false
        if self._da.length() != second_bag._da.length():
            return False

        # loop iteration to count same values and compare returning false if they don't match
        for i in range(self._da.length()):
            positions = self._da.get_at_index(i)

            if self.count(positions) != second_bag.count(positions):
                return False
        return True



    def __iter__(self):
        """
        Enables bag to iterate across itself.
        Initialize a variable to track iterators progress through bag contents
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns next item in the bag based on current location of iterator
        """
        try:
            value = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1
        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
