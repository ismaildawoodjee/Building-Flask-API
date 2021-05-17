

class Node:
    def __init__(self, data=None, left=None, right=None):
        """A data node for a binary search tree. Instead of pointing
        to the next node like in a linked list, the BST node points to
        the left and right nodes.
        """
        self.data = data
        self.left = left
        self.right = right


class BinarySearchTree:
    def __init__(self):
        """Initialize the root of the BST."""
        self.root = None

    def _insert_recursive(self, data, node):
        """Private method for inserting new data. In a BST, if the data
        is less than the root node, it is inserted on the left and vice
        versa. If data is equal to the root node, do nothing.
        """
        if data["id"] < node.data["id"]:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)
        elif data["id"] > node.data["id"]:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)
        else:
            # BST should not have any duplicate data, so just do nothing
            return

    def insert(self, data):
        """Insert data into a new Node of the BST. This calls the 
        `insert_recursive` private method to check where to insert the
        new data.
        """
        if self.root is None:
            self.root = Node(data)
        else:
            # `_insert_recursive` is a private method, and should not be
            # used by anyone/anything except the `insert` method
            self._insert_recursive(data, self.root)

    def _search_recursive(self, blog_post_id, node):
        """Private method for `search`."""
        if blog_post_id == node.data["id"]:
            return node.data
        if blog_post_id < node.data["id"] and node.left is not None:
            if blog_post_id == node.left.data["id"]:
                return node.left.data
            return self._search_recursive(blog_post_id, node.left)

        if blog_post_id > node.data["id"] and node.right is not None:
            if blog_post_id == node.right.data["id"]:
                return node.right.data
            return self._search_recursive(blog_post_id, node.right)

    def search(self, blog_post_id):
        """Search for a specific blog post using blog post ID."""
        blog_post_id = int(blog_post_id)
        if self.root is None:
            return False
        return self._search_recursive(blog_post_id, self.root)
