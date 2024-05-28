# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A6 - Separate Chaining HashMap
# Due Date: 12/07/2023
# Description: Part 1 Hash Map Implementation - Chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key:value pair in hash map.
        If given key exists, replace the existing value with the new value.
        If key is not in hash map, add the key:value pair.

        Table must be resized to double its current capacity when current load factor is greater/equal than 1.0
        """
        if self.table_load() >= 1.0:                                # check if table must be resized
            new_capacity = self._next_prime(self._capacity * 2)
            self.resize_table(new_capacity)

        hash_value = self._hash_function(key)                       # hash value
        index = hash_value % self._capacity                         # hash index
        hash_map = self._buckets[index]

        found_key = hash_map.contains(key)                          # assign contain method to find key in the hash map
        if found_key:
            found_key.value = value                                 # existing key found updates to new value
        else:
            hash_map.insert(key, value)                             # key does not exist, inserts the new key:value
            self._size += 1                                         # size increments

    def resize_table(self, new_capacity: int) -> None:
        """
        Change capacity of the hash table.
        If new_capacity is less than 1, method does nothing.
        If new_capacity is 1 or more, it must be prime, else change to next highest prime.
        """
        if new_capacity < 1:                                # method does nothing if new_capacity is less than 1
            return

        if not self._is_prime(new_capacity):                # if new_capacity is not prime, update to next prime
            new_capacity = self._next_prime(new_capacity)

        elements = LinkedList()                             # new linked list
        for i in range(self._capacity):
            if self._buckets[i].length() > 0:
                for elem in self._buckets[i]:               # iterate each elem in cur bucket
                    elements.insert(elem.key, elem.value)   # insert each elem

        self._buckets = DynamicArray()                      # new Dynamic Array
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())              # append each of the index during iteration

        self._capacity = new_capacity                       # Update to new capacity
        self._size = 0                                      # reset size to 0

        for elem in elements:
            self.put(elem.key, elem.value)                  # call put method to rehash and table factor

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        return self._size/self._capacity                # (m/n) -- total size / capacity to insert before resizing

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in the hash table
        """
        empty_counter = 0                                   # initial count 0
        index_counter = 0

        # if in iteration there is empty bucket, increment the counter
        while index_counter != self._capacity:
            cur_val = self._buckets.get_at_index(index_counter)

            if cur_val.length() == 0:
                empty_counter += 1
            index_counter += 1
        return empty_counter

    def get(self, key: str):
        """
        Return value for the given key else return None if key does not exist
        """
        hash_value = self._hash_function(key)               # hash value
        index = hash_value % self._capacity                 # hash index
        hash_map = self._buckets[index]
        current = hash_map._head                            # head of the linked list

        for i in range(hash_map._size):
            if current.key == key:                         # if current == key, return that value
                return current.value
            else:
                current = current.next                      # elif current didn't match key, go next
        return None                                         # Returns None if not found

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map else False.
        """
        hash_value = self._hash_function(key)           # hash value
        index = hash_value % self._capacity             # hash index
        hash_map = self._buckets[index]

        if hash_map.contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes given key and value from hash map.
        If key is not in hash map, method does nothing.
        """
        hash_value = self._hash_function(key)           # hash value
        index = hash_value % self._capacity             # hash index
        hash_map = self._buckets[index]

        if hash_map.remove(key):                        # remove the given key and decrement the size
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns Dynamic Array where each index contains tuple of key:value pair.
        """
        key_value = DynamicArray()

        for i in range(self._capacity):
            for node in self._buckets[i]:
                key_value.append((node.key, node.value))  # adds the key and value pair as tuple to Dynamic Array
        return key_value

    def clear(self) -> None:
        """
        Clears content of hash map, does not change capacity.
        """
        # clear linked list within Dynamic Array
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns tuple in following order:
    1. Dynamic Array comprising mode of given array
    2. Integer for highest frequency of occurrence for mode

    More than 1 value of highest frequency, all included
    O(N) time complexity.
    """
    map = HashMap(da.length() * 2)          # double the capacity
    max_count = 0                           # max count set to 0
    mode_num = DynamicArray()               # modes set to empty

    for i in range(da.length()):
        cur_val = da.get_at_index(i)
        val_count = map.get(cur_val)        # counter for cur_val

        if val_count is not None:
            val_count += 1                  # increment if there is a repeat
            map.put(cur_val, val_count)     # call put method for cur val and it's count
            if val_count > max_count:       # if more than max count, update new max count
                max_count = val_count
        else:
            map.put(cur_val, 1)       # count set to 1
            if max_count < 1:
                max_count = 1

    for i in range(map.get_capacity()):     # iterate through hashmap
        cur_bucket = map._buckets[i]
        if cur_bucket:
            current_node = cur_bucket._head

            while current_node:             # iterate through nodes
                if current_node.value == max_count:
                    mode_num.append(current_node.key)
                current_node = current_node.next
    return mode_num, max_count


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
