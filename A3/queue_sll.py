# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Part 5 Queue ADT
# Due Date: 11/06/23
# Description: Implementation of Queue ADT of Singly Linked Nodes


from SLNode import SLNode


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None
        self._tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Adds new value to end of queue (append) - O(1)
        """
        # self._head is same if we do size; but if it's empty what happens?

        new_node = SLNode(value)            # new node to store value given

        if self._head is None:              # empty queue, head & tail updated to point to new node
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node          # current tail's next node points to the new node
            self._tail = new_node               # current tail is new node

    def dequeue(self) -> object:
        """
        Remove and return the value from beginning of queue.
        Empty queue raises exception - O(1)
        """
        # empty queue will raise an exception
        if self.size() == 0:
            raise QueueException

        pop_value = self._head.value        # assign self._head value to new variable
        self._head = self._head.next        # update self._head to next element
        return pop_value

    def front(self) -> object:
        """
        Returns value of front element in queue without removal.
        Empty queue raises exception - O(1)
        """
        if self.is_empty():
            raise QueueException

        # return value of first element in queue without any change
        first_element = self._head.value
        return first_element


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)

    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))

    print('\n#front example 1')
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)

