'''
A Binary Search Tree node. 
'''
class TreeNode:

    '''
    Calculates the Height of a given node.
    '''
    @staticmethod
    def calculateHeight(node):
        if node.left == None and node.right == None:
            return 1
        elif node.left == None:
            return 1 + TreeNode.calculateHeight(node.right)
        elif node.right == None:
            return 1 + TreeNode.calculateHeight(node.left)
        else:
            return 1 + max(TreeNode.calculateHeight(node.left), TreeNode.calculateHeight(node.right))

    '''
    Gets the Left most TreeNode in the tree rooted at 'node'
    '''
    @staticmethod
    def getLeftMost(node):
        if node == None:
            return None
        elif node.left == None:
            return node
        else:
            return TreeNode.getLeftMost(node)

    '''
    Gets the Right most TreeNode in the tree rooted at 'node'
    '''
    @staticmethod
    def getRightMost(node):
        if node == None:
            return None
        elif node.right == None:
            return node
        else:
            return TreeNode.getRightMost(node)

    '''
    Gets the TreeNode containing the given data from the tree
    rooted at 'node'

    Returns the TreeNode if found, None otherwise.
    '''
    @staticmethod
    def getChildNode(data, node):
        if node == None:
            return None
        elif data == node.data:
            return node
        elif data < node.data:
            return TreeNode.getChildNode(data, node.left)
        else:
            return TreeNode.getChildNode(data, node.right)

    '''
    Creates an in-order list of the tree rooted at 'node'
    '''
    @staticmethod
    def listify(node, retList):
        if node == None:
            return retList
        if not node.left == None:
            retList = TreeNode.listify(node.left, retList)
        retList.append(node.data)
        if not node.right == None:
            retList = TreeNode.listify(node.right, retList)
        return retList
    
    '''
    Creates a TreeNode object with the given data.
    Optional parameters:
        left <TreeNode> The immediate left child
        right <TreeNode> The immediate right child
    '''
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
    def defaultAddFunc(data):
        return data

    '''
    Rotation method used to ensure self-balancing.

    Case: Left-Left Rotation
    '''
    @staticmethod
    def leftRotation(root):
        if root == None:
            return None
        else:
            newRoot = root.right
            root.right = newRoot.left
            newRoot.left = root
            return newRoot

    '''
    Rotation method used to ensure self-balancing.

    Case: Right-Right Rotation
    '''
    @staticmethod
    def rightRotation(root):
        if root == None:
            return None
        else:
            newRoot = root.left
            root.left = newRoot.right
            newRoot.right = root
            return newRoot

    '''
    Rotation method used to ensure self-balancing.

    Case: Left-Right Rotation
    '''
    @staticmethod
    def leftRightRotation(root):
        if root == None:
            return None
        else:
            root.left = AvlTree.leftRotation(root.left)
            return AvlTree.rightRotation(root)

    '''
    Rotation method used to ensure self-balancing.

    Case: Right-Left Rotation
    '''
    @staticmethod
    def rightLeftRotation(root):
        if root == None:
            return None
        else:
            root.right = AvlTree.rightRotation(root.right)
            return AvlTree.leftRotation(root)

    '''
    Calculates the Balance Factor to determine if 
    the tree at the given root needs to be balanced.
    '''
    @staticmethod
    def calculateBalanceFactor(root):
        if root == None:
            return 0
        else:
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
                if balanceFactor > 0:
                    if AvlTree.calculateBalanceFactor(root.left) > 0:
                        # right rotation
                        return AvlTree.rightRotation(root)
                    else:
                        # left-right rotation
                        return AvlTree.leftRightRotation(root)
                else:
                    if AvlTree.calculateBalanceFactor(root.right) < 0:
                        # left rotation
                        return AvlTree.leftRotation(root)
                    else:
                        # right-left rotation
                        return AvlTree.rightLeftRotation(root)
            else:
                # Already Balanced
                return root

    '''
    Recurisve helper method for insertion
    '''
    @staticmethod
    def insertRecursive(data, root, clash=None, addFunc=None):
        if data < root.data:
            if root.left == None:
                # Base Case
                if addFunc == None:
                    root.left = TreeNode(addFunc(data))
                else:
                    root.left = TreeNode(data)
                return root
            else:
                root.left = AvlTree.insertRecursive(data, root.left, clash, addFunc)
                return AvlTree.balance(root)
        elif data > root.data:
            if root.right == None:
                # Base Case
                if addFunc == None:
                    root.right = TreeNode(addFunc(data))
                else:
                    root.right = TreeNode(data)
                return root
            else:
                root.right = AvlTree.insertRecursive(data, root.right, clash, addFunc)
                return AvlTree.balance(root)
        else:
            # insert Recursive with data == root.data
            if clash == None:
                return root
            else:
                return clash(data, root)
    
    '''
    Recurisve helper method for removal
    '''
    @staticmethod
    def removeRecursive(data, root):
        if root == None:
            return None
        elif data == root.data:
            # found case to remove
            if root.left == None and root.right == None:
                return None
            elif root.left == None:
                # root.right is a TreeNode
                return root.right
            elif root.right == None:
                # root.left is a TreeNode
                return root.left
            else:
                # root.left and root.right are TreeNodes
                node = TreeNode.getLeftMost(root.right)
                root.data = node.data
                root.right = AvlTree.removeRecursive(data, root.right)
                return AvlTree.balance(root)
        elif data < root.data:
            root.left = AvlTree.removeRecursive(data, root.left)
            return AvlTree.balance(root)
        else:
            root.right = AvlTree.removeRecursive(data, root.right)
            return AvlTree.balance(root)

    '''
    Creates a new AvlTree self-balancing tree.
    Every node is considered to have UNIQUE data.

    The optional clashFunc parameter is a provided method to 
    handle clashes where the desired data to insert already 
    exists in the tree.

    By Default, clashFunc does nothing and does not modify the 
    tree if the data to insert already exists in the tree.

    Any given classFunc function must have the form:
        <TreeNode> clashFunc(<any> data, <TreeNode> node)
    Otherwise the insertion method would break.
    '''
    def __init__(self, clashFunc=None, addFunc=None):
        self.root = None
        if clashFunc == None:
            self.clash = AvlTree.defaultClash
        else:
            self.clash = clashFunc
        if addFunc == None:
            self.addFunc = AvlTree.defaultAddFunc
        else:
            self.addFunc = addFunc

    '''
        Adds a new node with the given data to the Tree. 
    '''
    def insert(self, data):
        if self.root == None:
            self.root = TreeNode(data)
        else:
            self.root = AvlTree.insertRecursive(data, self.root, self.clash, self.addFunc)

    '''
    Removes a node with the given data from the Tree
    '''
    def remove(self, data):
        if self.root == None:
            return None
        else:
            self.root = AvlTree.removeRecursive(data, self.root)
        
    '''
    Alias for the insert method
    '''
    def add(self, data):
        self.insert(data)

    '''
    Finds a node in the Tree with the given data
    '''
    def search(self, data):
        return TreeNode.getChildNode(data, self.root)

    '''
    Override for the 'in' keyword. True if search finds a
    node for the given data, false otherwise.
    '''
    def __contains__(self, data):
        if self.search(data) == None:
            return False
        else:
            return True

    '''
    Creates an ordered list from smallest to largests
    '''
    def generateList(self):
        return TreeNode.listify(self.root, [])

    '''
    Generates a set object from the Tree.
    '''
    def generateSet(self):
        return set(self.generateList())
