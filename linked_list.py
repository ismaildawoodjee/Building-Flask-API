"""Separate file for data structures"""


class Node:
    """Node class to hold data and point to the next node."""

    def __init__(self, data=None, next_=None):
        self.data = data
        self.next_ = next_

    def __repr__(self):
        return f"[{self.data}]"


class LinkedList:
    """LinkedList wrapper to keep track of the head and tail nodes."""

    def __init__(self):
        self.head = None
        self.tail = None

    def to_list(self):
        """Convert linked list to a normal Python list."""
        alist = []
        if self.head is None:
            return alist
        
        # traverse through linked list
        node = self.head
        while node:
            alist.append(node.data)
            node = node.next_
        
        return alist

    def __repr__(self):
        nodes = []
        node = self.head

        while node:
            if node is self.head:
                nodes.append(f"[Head: {node.data}]")
            elif node.next_ is None:
                nodes.append(f"[Tail: {node.data}]")
            else:
                nodes.append(f"[{node.data}]")
            node = node.next_

        return '-> '.join(nodes)

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f"{str(node.data)} -> "
            node = node.next_

        ll_string += "None"
        print(ll_string)

    def insert_beginning(self, data):
        """New node at beginning contains data, its next node is the head"""
        if self.head is None:
            self.head = Node(data, None)
            self.tail = self.head
        else:
            new = Node(data, self.head)
            self.head = new

    def insert_at_end(self, data):
        """New node inserted at the end of linked list"""
        if self.head is None:
            self.insert_beginning(data)
            return

        self.tail.next_ = Node(data, None)
        self.tail = self.tail.next_
