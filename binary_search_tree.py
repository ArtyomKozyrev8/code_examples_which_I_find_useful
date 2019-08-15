# Binary search tree (BST) is a binary tree where the value of each node is larger or equal to the values in all the nodes
# in that node's left subtree and is smaller than the values in all the nodes in that node's right subtree.

My solution without recursion:

import collections

Node = collections.namedtuple('Node', ['left', 'right', 'value'])


def contains(root, value):
    while(root):
        if root.value == value:
            return True
        elif root.value < value:
            if root.right:
                root = root.right
            else:
                return False
        else:
            if root.left:
                root = root.left
            else:
                return False


n5 = Node(value=5, left=None, right=None)
n15 = Node(value=15, left=None, right=None)
n10 = Node(value=10, left=n5, right=n15)
n25 = Node(value=25, left=None, right=None)
n20 = Node(value=20, left=n10, right=n25)


print(contains(n20, 19))


# My solution with recursion:

def contains(root, value):
    if root.value == value:
        return True
    elif root.value < value:
        if root.right:
            return contains(root.right, value)
        else:
            return False
    else:
        if root.left:
            return contains(root.left, value)
        else:
            return False
