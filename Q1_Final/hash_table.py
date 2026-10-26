"""
hash_table.py:
Generic hash table using open addressing with linear probing.
Deleted slots are marked as tombstones so that probe chains are not broken.
"""

class HashTable:
    def __init__(self, size=23):
        self.size = size
        self.keys = [None] * size  # store keys
        self.values = [None] * size  # store values
        # tombstone, initially all False（not a tombstone = before nothing being deleted
        # true = tombstone (slot was deleted)
        self.deleted = [False] * size
        self.count = 0

    def hash_function(self,key):
        return key % self.size

    def insert(self, key, value):
        index = self.find_index(key)

        # 1. key already in the table, then just update its value
        if index is not None:
            self.values[index] = value
            return index, 0

        # 2. table would become too full, then grow first
        if (self.count + 1) / self.size > 0.7:
            self.resize()

        #3. new key, linear probing to the first free slot (empty or tombstone)
        index = self.hash_function(key)
        probes = 0
        while self.keys[index] is not None:
            index = (index + 1) % self.size
            probes += 1
        self.keys[index] = key
        self.values[index] = value
        self.deleted[index] = False # if insert to a current tombstone slot, then remove the tombstone
        self.count += 1
        return index, probes

    def get(self, key):
        index = self.find_index(key)
        if index is None:
            return None
        return self.values[index]

    def delete(self, key):
        index = self.find_index(key)
        if index is None:
            return False
        self.keys[index] = None
        self.values[index] = None
        self.deleted[index] = True
        self.count -=1
        return True

    def display(self):
        print(f"Size: {self.size} | Items: {self.count} | Load factor: {self.load_factor():.2f}\n")
        for i in range(self.size):
            if self.deleted[i]:
                print(f"Slot {i:2}: (Tombstone)")
            elif self.keys[i] is not None:
                print(f"Slot {i:2}: {self.values[i]}")     # value is Medicine，auto call __str__
            else:
                print(f"Slot {i:2}: None")

    def get_all_values(self):
        """Return every stored value(skips empty slots and tombstones)."""
        result = []
        for i in range(self.size):
            if self.keys[i] is not None:
                result.append(self.values[i])
        return result

    # ----helper
    def find_index(self, key):
        """Return the slot index that holds key, or None if key is not in the table"""
        index = self.hash_function(key)
        home = index

        # got something or tombstone, continue find; meet empty slot, stop
        while self.keys[index] is not None or self.deleted[index]:
            if self.keys[index] == key:
                return index
            index = (index + 1) % self.size
            if index == home:
                break
        return None

    def count_probes(self, key):
        """Number of slots inspected when searching for key (used by the experiment).
        Kept separate from find_index so that counting does not slow down timed searches."""
        index = self.hash_function(key)
        probes = 1
        while self.keys[index] is not None or self.deleted[index]:
            if self.keys[index] == key:
                return probes
            index = (index + 1) % self.size
            probes += 1
            if probes > self.size:      # whole table checked
                break
        return probes

    # in case the hash table is full
    def resize(self):
        old_keys = self.keys        # 1. keep the old data
        old_values = self.values
        self.size = next_prime(self.size *2)    # 2. new size
        self.keys = [None] * self.size          # 3. build a new empty table
        self.values = [None] * self.size
        self.deleted = [False] * self.size
        self.count = 0
        for i in range(len(old_keys)):          # 4. re-insert old data one-by-one
            if old_keys[i] is not None:
                self.insert(old_keys[i], old_values[i])

    def load_factor(self):
        return self.count / self.size

# math helper
def next_prime(n):
    while not is_prime(n):
        n+=1
    return n

def is_prime(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True



