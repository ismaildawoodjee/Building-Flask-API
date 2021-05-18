class Node:
    def __init__(self, data=None, next_=None):
        """A queue is a special type of linked list."""
        self.data = data
        self.next_ = next_

class Queue:
    def __init__(self):
        """Specify the head/start and tail/end of the queue."""
        self.head = None
        self.tail = None

    def enqueue(self, data):
        """Add data to the tail of the queue. If both tail and head
        are empty set new Node to head and tail. Otherwise, set the pointer
        of tail to the new Node and the tail itself to be the new Node.
        """
        if self.tail is None and self.head is None:
            self.tail = self.head = Node(data, None)
            return

        self.tail.next_ = Node(data, None)
        self.tail = self.tail.next_
        return

    def dequeue(self):
        """Remove the data from the head of the tail, following the 
        first in first out (FIFO) principle or first come first served.
        """
        if self.head is None:
            return None
        removed = self.head
        self.head = self.head.next_
        
        if self.head is None:
            self.tail = None

        return removed
