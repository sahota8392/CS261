# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Part 2 - AVL Class Implementation
# Due Date: 11/20/2023
# Description: Implementation of AVL class methods


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds new value to the tree while maintaining AVL property.
        Duplicates are not allowed.
        O(log n) runtime.
        """

        add_node = AVLNode(value)           # new node
        cur = self._root                    # cur node
        p_node = None                       # parent node

        if self.contains(value):            # Duplicates not allowed
            return

        while cur is not None:              # while True loop
            p_node = cur
            if value < cur.value:
                cur = cur.left              # move to left subtree
            elif value > cur.value:
                cur = cur.right             # move to right subtree
            else:
                return

        if p_node is None:
            self._root = add_node           # if empty tree, new node is root
        elif value < p_node.value:
            p_node.left = add_node          # insert new node as left child of parent
            add_node.parent = p_node        # parent pointer updates
        else:
            p_node.right = add_node         # insert new node as right child of parent
            add_node.parent = p_node        # parent pointer updates

        # balance the tree again after insertion of new value
        p = add_node.parent
        while p is not None:
            self._rebalance(p)              # rebalance from parent of new node
            p = p.parent                    # move to the next parent

    def remove(self, value: object) -> bool:
        """
        remove the value from AVL tree returning True if value is removed else False - O(log N)
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
            self._remove_two_subtrees(parent_node, cur_node)

        p = parent_node                                         # rebalance AVL after removal
        while p is not None:
            self._rebalance(p)
            p = p.parent
        return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        remove element with 2 subtrees.
        """
        min_node_parent = remove_node                   # parent of min node as remove node
        min_node = remove_node.right                    # min node as right child of remove node

        if remove_node.left and remove_node.right is not None:  # check if there are left and right subtrees
            while min_node.left is not None:            # find leftmost child in right subtree
                min_node_parent = min_node
                min_node = min_node.left

        remove_node.value = min_node.value              # find min value on right subtree and update

        if min_node_parent == remove_node:              # If the minimum node is the right child of the removed node
            min_node_parent.right = min_node.right
        else:
            min_node_parent.left = min_node.right       # Update the parent's left to the right subtree of the min node

        p = min_node                                    # rebalance AVL tree after removal
        while p is not None:
            self._rebalance(p)
            p = p.parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate balance factor for given node
        """
        if node is None:
            return -1
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        GET the height of a node
        """
        # if node is not none, return the height else return -1
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Execute a left rotation of the AVL tree
        """
        new_right_child_root = node.right       # right child of the given node is the new root
        node.right = new_right_child_root.left  # right child of the node updates to be left child of the new root

        if new_right_child_root.left:                   # if left child exists, update parent pointer
            new_right_child_root.left.parent = node

        new_right_child_root.left = node                # update left child of new root to original node
        node.parent = new_right_child_root              # update parent pointer to the new root

        # call the update height to update height
        self._update_height(node)
        self._update_height(new_right_child_root)

        return new_right_child_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Execute a right rotation of the AVL tree
        """
        new_left_child_root = node.left         # left child of given node is the new root node
        node.left = new_left_child_root.right   # left child of node updates to be right child of new root

        if new_left_child_root.right:           # if the right child of the new root exists, update parent pointer
            new_left_child_root.right.parent = node

        new_left_child_root.right = node        # update the right child of the new root to be the original node
        node.parent = new_left_child_root       # update the parent pointer to the new root

        # Call the update height to update height
        self._update_height(node)
        self._update_height(new_left_child_root)

        return new_left_child_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of the AVL tree
        """
        if node is not None:  # Add a check for None
            node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalance AVL tree from given node after insertion or deletion changes are made.
        """
        if self._balance_factor(node) > 1:                      # checks if the AVL tree is right heavy
            rotated_parent = node.parent                        # assign the original parent of the node to a variable

            if self._balance_factor(node.right) < 0:            # check if right subtree is left-heavy
                node.right = self._rotate_right(node.right)     # right rotation on right child
                node.right.parent = node                        # update parent pointer of the right child

            new_subtree_root = self._rotate_left(node)          # left rotation on the node
            if new_subtree_root:
                new_subtree_root.parent = rotated_parent        # update the parent pointer of new subtree root

            if node is self._root:                              # if node is root, update root of tree
                self._root = new_subtree_root
                return

            else:
                # update the parent pointer to the new subtree root
                if new_subtree_root and new_subtree_root.value < rotated_parent.value:
                    rotated_parent.left = new_subtree_root
                elif new_subtree_root:
                    rotated_parent.right = new_subtree_root

        elif self._balance_factor(node) < -1:                   # check if AVL tree is left-heavy
            rotated_parent = node.parent                        # assign the original parent of the node to a variable

            if self._balance_factor(node.left) > 0:             # check if left subtree is right-heavy
                node.left = self._rotate_left(node.left)        # left rotation on the left child
                node.left.parent = node                         # update parent pointer of the left child

            new_subtree_root = self._rotate_right(node)         # right rotation on the node
            if new_subtree_root:
                new_subtree_root.parent = rotated_parent        # update the parent pointer of the new subtree root

            if node is self._root:
                self._root = new_subtree_root                   # if node is root, update root of tree
                return

            else:
                # update the parent pointer to the new subtree root
                if new_subtree_root and new_subtree_root.value < rotated_parent.value:
                    new_subtree_root.parent = rotated_parent
                    rotated_parent.left = new_subtree_root
                elif new_subtree_root:
                    new_subtree_root.parent = rotated_parent
                    rotated_parent.right = new_subtree_root
        else:
            self._update_height(node)                           # if node is already balanced, update height


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
