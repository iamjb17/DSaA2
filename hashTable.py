# Data Structures and Algorithms 2

# Hash Table - A type of data structures that sends data through a hash function and that hash function returns
# a value that is the location/index that the data will be located. Hash functions typically use the Modulo
# operator. This hash function will take a size and create an array(or other data structure) of that size to store
# the data. Collisions are what happens if to 2 elements have the same return from the hash function. One way to
# handle this is through, the usage of linked list or another data structure that will hold the next value in line,
# in order.

# The objective of this application is to deliver 40 packages that are variable distances apart, and to deliver
# those packages within 140 miles. So the purpose of this hash table implementation will be to ___. But most
# importantly it will sort the internal data by distances from current location.


# The structure that will hold the key and value. also points to the next node if collision happened
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def getValue(self):
        return self.value

    def getKey(self):
        return self.key

    def getNext(self):
        return self.next

    def __repr__(self):
        key: str = self.getKey()
        value: int = self.getValue()
        next_elem = self.getNext()
        elem = (key, value, next_elem)

        return elem.__str__()


class HashTableIterator:
    def __init__(self, hashtable):
        self._hashtable = hashtable
        self._index = 0

    def __next__(self):
        if self._index < self._hashtable.size:
            result = (self._hashtable.buckets[self._index])
            self._index += 1
            return result
        raise StopIteration


# The structure of the hash table, takes an initial size. Creates a list with size of initial capacity
class HashTable:
    def __init__(self, init_capacity=int):
        self.init_capacity = init_capacity
        self.size = 0
        self.buckets = [None] * init_capacity

    def hash_function(self, key):
        sum_from_hash = 0
        # for each letter in the key, sum_from_hash = sum_from_hash + (index of the letter + length of key to the power
        # the unicode point of that letter -> sum_from_hash = sum_from_hash mod capacity of the hash table.
        sum_from_hash = hash(key) % self.init_capacity
        # for index, curr in enumerate(key):
        #     sum_from_hash += (index + len(key) ** ord(curr))
        #     sum_from_hash = sum_from_hash % self.init_capacity
        return sum_from_hash

    # adds a new key:value to the table. if collision happens appends to the elements next
    def insert(self, key, value):
        self.size += 1
        index = self.hash_function(key)
        node = self.buckets[index]
        if node is None:
            self.buckets[index] = Node(key, value)
            return
        prev = node
        # Traverse the nodes, keeping track of the previous node
        while node is not None:
            # print("node not none")
            # print(node)
            prev = node
            node = node.next
        prev.next = Node(key, value)

    #
    def find(self, key):
        index = self.hash_function(key)
        node = self.buckets[index]
        while node is not None and node.key != key:
            node = node.next
        if node is None:
            return None
        else:
            return node

    #
    def remove(self, key):
        index = self.hash_function(key)
        node = self.buckets[index]
        prev = None
        while node is not None and node.key != key:
            prev = node
            node = node.next
        if node is None:
            return None
        else:
            self.size -= 1
            result = node.value
            if prev is None:
                self.buckets[index] = node.next
            else:
                prev.next = prev.next.next
            return result

    def __iter__(self):
        return HashTableIterator(self)
