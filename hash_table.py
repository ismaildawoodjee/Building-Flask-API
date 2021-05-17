"""File for hash table data structure"""


class Node:
    def __init__(self, data=None, next_=None):
        """Convenient to use a linked list node data structure to take
        care of hash collisions, i.e. when two different keys get mapped
        to the same hash value.
        """
        self.data = data
        self.next_ = next_


class Data:
    def __init__(self, key, value):
        """Key-value pair. Keys MUST be unique, but values need not be."""
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, table_size):
        """"""
        self.table_size = table_size
        self.hash_table = [None] * table_size

    def hash_function(self, key):
        """Custom hash function to map a key into an index for O(1) operations.
        Use the modulo operator `%` to ensure that hash_value stays within
        the boundary of the hash table size. The `ord` function maps a single 
        character string into its corresponding ASCII integer. Opposite is `chr`.
        A good hash function will not have a lot of hash collisions.
        """
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value

    def add_key_value(self, key, value):
        """Add key-value data and map the key into an index using the 
        hash function. If the index is not None, then traverse the linked
        list and add the data node.
        """
        hashed_key = self.hash_function(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hashed_key]
            while node.next_:
                node = node.next_

            node.next_ = Node(Data(key, value), None)

    def get_value(self, key):
        """Get the value of a data node using the index, given its key."""
        hashed_key = self.hash_function(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_ is None:
                return node.data.value
            while node.next_:
                if key == node.data.key:
                    return node.data.value
                node = node.next_

            if key == node.data.key:
                return node.data.value
        return None

    def print_table(self):
        """Print the string representation of hash table."""
        print("{")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                ll_string = ""
                node = val
                if node.next_:
                    while node.next_:
                        ll_string += (
                            str(node.data.key) + " : " +
                            str(node.data.value) + " --> "
                        )
                        node = node.next_
                    ll_string += (
                        str(node.data.key) + " : " +
                        str(node.data.value) + " --> None"
                    )
                    print(f"    [{i}] {ll_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")
