# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Part 1 - BST Tree Implementation
# Due Date: 11/20/2023
# Description: Implementation of BST class methods


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a new value to the tree.
        If duplicate value, the new value is added to the right subtree of that node.
        O(n) runtime.
        """

        # first value given becomes the root node if none
        if self._root is None:
            self._root = BSTNode(value)
            return

        # assign the root the variable cur_root
        cur = self._root

        while True:                                    # while True loop
            if value < cur.value:                      # if value less than cur_root value
                if cur.left is None:                   # if left child is empty
                    cur.left = BSTNode(value)          # left updates to the new value
                    return
                else:
                    cur = cur.left                     # move to left child
            elif value > cur.value:                    # if value is greater than cur value, update in right
                if cur.right is None:
                    cur.right = BSTNode(value)
                    return
                else:
                    cur = cur.right
            else:                                       # duplicate value goes to the right subtree of that node
                if cur.right is None:
                    cur.right = BSTNode(value)
                    return
                else:
                    cur = cur.right

    def remove(self, value: object) -> bool:
        """
        Remove provided value from the tree returning TRUE if successful, else FALSE.
        Removing node with 2 subtrees, replace it with the leftmost child of the right subtree.
        Removing node with 1 subtree, replace with the new root node of the subtree.
        O(N) runtime.
        """
        cur_node = self._root                                   # cur node starts with self._root
        parent_node = None                                      # removed node's child will be assigned as parent

        while cur_node is not None and cur_node.value != value:
            if value > cur_node.value:                          # target value > cur node value, go to right child
                parent_node = cur_node                          # update cur node as new parent node
                cur_node = cur_node.right
            elif value < cur_node.value:
                parent_node = cur_node
                cur_node = cur_node.left                        # target value < cur node value, go to left child

        if cur_node is None:                                    # value is not found
            return False

        if cur_node.left is None and cur_node.right is None:    # remove_no_subtrees
            self._remove_no_subtrees(parent_node, cur_node)
        elif cur_node.left is None or cur_node.right is None:   # remove_one_subtree
            self._remove_one_subtree(parent_node, cur_node)
        else:
            self._remove_two_subtrees(parent_node, cur_node)    # remove_two_subtrees
        return True

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        If there are no subtrees, remove the root node
        """
        # if node being removed has no left-right child, remove and update references
        if remove_parent is None:
            self._root = None
        elif remove_parent.right == remove_node:
            remove_parent.right = None
        else:
            remove_parent.left = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        If removed node has 1 subtree (left or right), replace deleted node with root node of subtree
        """
        # remove node that has a left or right subtree (only)
        if remove_parent is None:                           # if removed node is root since root has no parent
            if remove_node.right:
                self._root = remove_node.right              # update to the right subtree node value
            else:
                self._root = remove_node.left               # updates to left subtree if no right

        elif remove_node == remove_parent.left:             # removed node is left child of parent
            if remove_node.right:
                remove_parent.left = remove_node.right      # update parent's left child to right subtree
            else:
                remove_parent.left = remove_node.left       # update parent's left child to left subtree

        else:
            if remove_node.right:
                remove_parent.right = remove_node.right     # update parent's right child to right subtree
            else:
                remove_parent.right = remove_node.left      # update parent's right child to left subtree

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removing node with 2 subtrees. Replace the leftmost child of the right subtree as the new Root node.
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)
        min_node_parent = remove_node                       # parent of min node as remove node
        min_node = remove_node.right                        # min node as right child of remove node

        if remove_node.left and remove_node.right is not None:  # check if there are left and right subtrees
            while min_node.left is not None:                    # find leftmost child in right subtree
                min_node_parent = min_node
                min_node = min_node.left

        remove_node.value = min_node.value          # find min value on right subtree and update

        if min_node_parent == remove_node:          # If the minimum node is the right child of the removed node
            remove_node.right = min_node.right
        else:
            min_node_parent.left = min_node.right  # Update the parent's left to the right subtree of the min node

    def contains(self, value: object) -> bool:
        """
        Return TRUE if value exists in the Tree, else FALSE.
        Empty tree returns FALSE.
        O(n) runtime.
        """
        curr_node = self._root

        # while loop occurs until entire tree is traversed or value exists
        while curr_node is not None:
            if value == curr_node.value:              # value is found
                return True
            elif value < curr_node.value:
                curr_node = curr_node.left      # traverse left if value is less than curr_node
            else:
                curr_node = curr_node.right     # traverse right if value is more than cur_node
        return False                            # while loop did not find the value

    def inorder_traversal(self) -> Queue:
        """
        Inorder Traversal of the tree or Sorted Order.
        Returns Queue of values for visited nodes in order visited.
        If empty tree, method returns empty Queue.
        O(n) runtime.
        """
        # enqueue the inorder traversal nodes to result
        result = Queue()

        # recursive call
        def inorder(root):
            if root is None:            # if empty, return empty
                return
            inorder(root.left)          # traverse left
            result.enqueue(root.value)  # append nodes to result
            inorder(root.right)         # traverse right
        inorder(self._root)
        return result

    def find_min(self) -> object:
        """
        Return the lowest value in the tree.
        If empty tree, return None.
        O(n) runtime.
        """
        cur = self._root

        # if root is empty, return None
        if cur is None:
            return None

        # search min value in left child leaf node
        while cur.left is not None:
            cur = cur.left
        return cur.value

    def find_max(self) -> object:
        """
        Return highest value in tree.
        If empty tree, return None.
        O(n) runtime.
        """
        cur = self._root

        # if root is empty, return None
        if cur is None:
            return None

        # max value in right child in leaf node
        while cur.right is not None:
            cur = cur.right
        return cur.value

    def is_empty(self) -> bool:
        """
        Return True if empty, else False - O(1) runtime.
        """
        return self._root is None   # return True if root is None, else False

    def make_empty(self) -> None:
        """
        Remove all nodes from the tree - O(1) runtime.
        """
        self._root = None   # set the root to None and removes all


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
