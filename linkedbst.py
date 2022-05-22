"""
File: linkedbst.py
Author: Ken Lambert
"""
from random import choice, shuffle
import time
import sys
from math import log
import tqdm
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
sys.setrecursionlimit(100000)
# from linkedqueue import LinkedQueue



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node1, level):
            res = ""
            if node1 is not None:
                res += recurse(node1.right, level + 1)
                res += "| " * level
                res += str(node1.data) + "\n"
                res += recurse(node1.left, level + 1)
            return res

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        # lyst = list()
        cur = self._root
        # def part_def():
        stack = LinkedStack()
        all_res = []
        while not stack.isEmpty() or cur is not None:
            if cur is not None:
                stack.add(cur)
                cur = cur.left
            else:
                cur = stack.pop()
                all_res.append(cur.data)
                cur = cur.right
        return all_res

        # def recurse(node):
        #     if node is not None:
        #         recurse(node.left)
        #         lyst.append(node.data)
        #         recurse(node.right)

        # recurse(self._root)
        # return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        cur = self._root
        # if cur is None:
        #     return None
        while True:
            if cur is None:
                return None
            if cur.data == item:
                return cur.data

            if item < cur.data:
                cur = cur.left
            else:
                cur = cur.right

        # def recurse(node):
        #     if node is None:
        #         return None
        #     elif item == node.data:
        #         return node.data
        #     elif item < node.data:
        #         return recurse(node.left)
        #     else:
        #         return recurse(node.right)

        # return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
        else:
            cur = self._root
            while True:
                if item < cur.data:
                    if cur.left is None:
                        cur.left = BSTNode(item)
                        break
                    else:
                        cur = cur.left
                else:
                    if cur.right is None:
                        cur.right = BSTNode(item)
                        break
                    else:
                        cur = cur.right
        self._size += 1
                # print("hoho")
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left is None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right is None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse
        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemremoved = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved is None:
            return None


        if not currentnode.left is None \
                and not currentnode.right is None:
            lift_max_to_top(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                new_child = currentnode.right

                # Case 3: The node has no right child
            else:
                new_child = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return itemremoved

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                olddata = probe.data
                probe.data = new_item
                return olddata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.right is None and top.left is None:
                return 0
            else:
                all_pos = [top.right, top.left]
                return 1 + max(height1(x) for x in all_pos if x is not None)
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        # print(list(self.inorder()))
        return self.height() < 2 * log((len(list(self.inorder())) + 1), 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [i for i in self.inorder() if low <= i <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def func(elem):
            if len(elem) == 0:
                return None
            mid = len(elem) // 2
            node = BSTNode(elem[mid])
            node.left = func(elem[:mid])
            node.right = func(elem[mid + 1:])
            return node

        self._root = func(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for num in self.inorder():
            if num > item:
                return num
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        # allow = 0
        for num in list(self.inorder())[::-1]:
            if num < item:
                return num
            # elif allow == 1:
            #     return num
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        # res_lst = []
        with open(path) as file:
            dictionary = [i.strip() for i in file.readlines()]

        start_time1 = time.time()
        for _ in tqdm.tqdm(range(10000)):
            elem = choice(dictionary)
            dictionary.index(elem)
        print("пошук за допомогою list: ", time.time() - start_time1)

        start_time2 = time.time()
        print(len(dictionary))
        my_tree1 = LinkedBST(dictionary)
        for _ in tqdm.tqdm(range(10000)):
            elem = choice(dictionary)
            # print(_)
            # print(elem)
            my_tree1.find(elem)
        print(my_tree1)
        print("пошук в словнику за абеткою: ", time.time() - start_time2)

        start_time3 = time.time()
        shuffle(dictionary)
        # print(len(dictionary))
        my_tree2 = LinkedBST(dictionary)
        for _ in tqdm.tqdm(range(10000)):
            elem = choice(dictionary)
            my_tree2.find(elem)
        print("пошук в перемішаному словнику: ", time.time() - start_time3)

        start_time4 = time.time()
        my_tree2.rebalance()
        for _ in tqdm.tqdm(range(10000)):
            elem = choice(dictionary)
            my_tree2.find(elem)
        print("пошук слів після балансування дерева: ", time.time() - start_time4)

if __name__ == "__main__":
    LBST = LinkedBST()
    LBST.demo_bst('/mnt/d/labs/2half/all_labs/lab13/first/binary_search_tree/words.txt')
