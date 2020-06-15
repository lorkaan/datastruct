'''
A Binary Search Tree node.
'''
class TreeNode:

    @staticmethod
    def calculateHeight(node):
        if node.left == None and node.right == None:
            return 0
        elif node.left == None:
            return 1 + node.right.height
        elif node.right == None:
            return 1 + node.left.height
        else:
            return 1 + max(TreeNode.calculateHeight(node.left), TreeNode.calculateHeight(node.right))


    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

'''
Class Representation of a Self-Balancing binary search tree.

AVL Tree Implementation
'''
class AvlTree:

    '''
    Default Clash Resolution where data == root.data

    Must return a TreeNode object.
    '''
    @staticmethod
    def defaultClash(data, root):
        return root

    @staticmethod
    def leftRotation(root):
        newRoot = root.right
        root.right = newRoot.left
        newRoot.left = root
        return newRoot

    @staticmethod
    def rightRotation(root):
        newRoot = root.left
        root.left = newRoot.right
        newRoot.right = root
        return newRoot

    @staticmethod
    def leftRightRotation(root):
        root.left = leftRotation(root.left)
        return rightRotation(root)

    @staticmethod
    def rightLeftRotation(root):
        root.right = rightRotation(root.right)
        return leftRotation(root)

    @staticmethod
    def calculateBalanceFactor(root):
        leftHeight = 0
        rightHeight = 0
        if not root.left == None:
            leftHeight = TreeNode.calculateHeight(root.left)
        if not root.right == None:
            rightHeight = TreeNode.calculateHeight(root.right)
        return leftHeight - rightHeight

    '''
    Self balancing method.
    '''
    @staticmethod
    def balance(root):
        if root == None:
            return True
        else:
            balanceFactor = AvlTree.calculateBalanceFactor(root)
            if abs(balanceFactor) > 1:
                # Unbalanced
                if balanceFactor < 0:
                    if AvlTree.calculateBalanceFactor(root.left) < 0:
                        # right rotation
                        return rightRotation(root)
                    else:
                        # left-right rotation
                        returnn leftRightRotation(root)
                else:
                    if AvlTree.calculateBalanceFactor(root.right) > 0:
                        # left rotation
                        return leftRotation(root)
                    else:
                        # right-left rotation
                        return rightLeftRotation(root)
            else:
                # Already Balanced
                return root


    @staticmethod
    def insertRecursive(data, root, clash=None):
        if data < root.data:
            if root.left == None:
                # Base Case
                root.left = TreeNode(data)
                return root
            else:
                root.left = insertRecursive(data, root.left)
                return AvlTree.balance(root)
        elif data > root.data:
            if root.right == None:
                # Base Case
                root.right = TreeNode(data)
                return root
            else:
                root.right = insertRecursive(data, root.right)
                return AvlTree.balance(root)
        else:
            # insert Recursive with data == root.data
            if clash == None:
                return root
            else:
                return clash(data, root)

    def __init__(self, clashFunc):
        self.root = None
        if clashFunc == None:
            self.clash = AvlTree.defaultClash
        else:
            self.clash = clashFunc

    def insert(self, data):
        if self.root == None:
            self.root = TreeNode(data)
        else:
            self.root = insertRecursive(data, self.root, self.clash)

    def search(self, data, root=self.root):
        if root == None:
            return False
        elif data == root.data:
            return True
        elif data < root.data:
            return self.search(data, root.left)
        else:
            return self.search(data, root.right)
