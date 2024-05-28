# linked list for Get by Value, Get by Index, Add and Remove

class Node:
    """subclass of the linked list class user will never interact with this"""
    def __init__(self, data=None):
        self.data = data            # storing past data point
        self.next = None            # pointer to the next Node initial is None


class LinkedList:
    """linked list class is a  wrapper that wraps over the nodes"""
    def __init__(self):
        # Always have head node available in linkedlist, empty data & just a placeholder pointing to first element
        self.head = Node()

    def append(self, data):
        """add element to the end of the list"""
        new_node = Node(data)                   # new node created of the class node with data passed in
        cur = self.head                         # current node we are looking at, starting point

        # iterate over each one of nodes in list, start at head, when next node is None, that's when we insert
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node                     # once at last element of list, we set our next node to the new node

    def length(self):
        """figures out length of the list"""
        cur = self.head
        total = 0                               # total number of nodes initial at 0

        # iterate till the last element and increment total
        while cur.next is not None:
            total += 1
            cur = cur.next
        return total

    def display(self):
        """display the current contents of the list"""
        elems = []                              # new list to display
        cur_node = self.head
        while cur_node.next is not None:
            cur_node = cur_node.next            # current node set to next node
            elems.append(cur_node.data)         # append the data of current node to elems list
        print(elems)

    def get(self, index):
        """extractor - pull out data point from specific index"""

        # check if index is valid
        if index >= self.length():
            print('Error: Get Index out of range!')
            return

        cur_index = 0                           # current index initial to 0
        cur_node = self.head                    # start at head

        # iteration until cur_index == index given by user
        while True:                             # while index check is True, iterate
            cur_node = cur_node.next
            if cur_index == index:
                return cur_node.data            # if cur_index equals to index input, return that value
            cur_index += 1

    def erase(self, index):
        """erase a node at given index"""
        if index >= self.length():
            print('Error: Erase Index is out of range!')
            return

        cur_index = 0
        cur_node = self.head

        # save current node as 'last node' - need to keep track that after removal, node points to right spot
        while True:
            last_node = cur_node
            cur_node = cur_node.next           # increment cur_node to the next node
            if cur_index == index:
                last_node.next = cur_node.next  # change last_node pointer to current after skipping index given
                return
            cur_index += 1                     # if not at given index, increment further


# CLASS LINKED LIST
my_list = LinkedList()
my_list.display()       # empty list

my_list.append(1)
my_list.append(2)
my_list.append(3)
my_list.append(4)
my_list.display()       # display list of 1,2,3,4 after appending

print('element at 2nd index: %d' % my_list.get(2))      # prints value of 3 (%d is placeholder for integer)

my_list.erase(2)        # remove index 2, value of 3
my_list.display()       # print list without '3'
