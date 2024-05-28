# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Part 1 Singly Linked List
# Due Date: 11/06/23
# Description: Implementation of a singly linked list data structure


from SLNode import *
# from timethis import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Adds new node beginning of list after front sentinel - O(1)
        """
        new_node = SLNode(value)            # new node variable set to imported SLNode value
        new_node.next = self._head.next     # new_node's next = current head's next node
        self._head.next = new_node          # head's next is new_node

    def insert_back(self, value: object) -> None:
        """
        Adds new node end of the list (append) - O(N)
        """
        new_node = SLNode(value)
        cur = self._head                    # current node we look at, start point

        # iterate through nodes starting at head updating cur, when next node is None, insert the value
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Add new value at given index of linked list.
        If given index is invalid, raise an exception - O(N).
        """
        # index is less than 0 or greater than length of nodes, raise Exception
        if index < 0 or index > self.length():
            raise SLLException()

        new_node = SLNode(value)                # new node holds new value to insert
        cur_node = self._head
        cur_index = 0

        # if index given is 0, call insert_front
        if index == 0:
            self.insert_front(value)

        # iterate until cur_index equals index given, then we insert new value
        while cur_index < index:
            cur_node = cur_node.next
            cur_index += 1
            if cur_index == index:
                new_node.next = cur_node.next
                cur_node.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Deletes node from linked list at given index - O(N)
        """
        # index is less than 0 or greater than length of nodes, raise Exception
        if index < 0 or index >= self.length():
            raise SLLException()

        cur_index = -1
        cur_node = self._head

        # iterate until cur_index equals index, then last node updates to current after skipping index given
        while cur_index < index:
            cur_index += 1
            last_node = cur_node                # last_node stores previous node
            cur_node = cur_node.next
            if cur_index == index:
                last_node.next = cur_node.next

    def remove(self, value: object) -> bool:
        """
        Traverse list from start to end and remove the first node matching given value returning True if removed - O(N)
        """
        cur_index = 1
        cur_node = self._head

        while cur_index <= self.length():
            cur_index += 1
            last_node = cur_node
            cur_node = cur_node.next            # cur_node updates to next node

            if cur_node.value == value:         # if the current node value matches to value given
                last_node.next = cur_node.next
                return True
        return False

    def count(self, value: object) -> int:
        """
        Counts number of elements that match provided value and returns that number - O(N)
        """
        cur_node = self._head
        count = 0

        # iterates until we finish the linked list
        while cur_node is not None:
            if cur_node.value == value:         # count increments if value matches to value in list
                count += 1
            cur_node = cur_node.next
        return count

    def find(self, value: object) -> bool:
        """
        Returns Boolean value based on if the provided value exists in the list - O(N)
        """
        cur_node = self._head

        # iterate through entire linked list until value matches or list empties
        while cur_node is not None:
            if cur_node.value == value:
                return True
            cur_node = cur_node.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        returns new LinkedList with requested number of nodes from original list.
        Starts with node located at requested start index, if indexes are invalid, raises exception - O(N)
        """
        # create end_index variable
        end_index = start_index + size

        # Check for invalid indices and size.
        if start_index < 0 or start_index >= self.length() or end_index > self.length() or size < 0:
            raise SLLException()

        # create variables
        new_list = LinkedList()
        cur_node = self._head.next
        cur_index = 0

        # Iterate through while we haven't reached end of list and size is greater than 0
        while cur_node is not None and size > 0:
            if cur_index >= start_index:
                new_list.insert_back(cur_node.value)        # call the insert_back to insert value
                size -= 1                                   # size decrements
            cur_index += 1
            cur_node = cur_node.next                        # current node updates to next
        return new_list


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
