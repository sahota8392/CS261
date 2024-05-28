# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2 Dynamic Array and ADT Implementation
# Due Date: 10/30/23
# Description: Implement various methods of Dynamic array and Bag ADT


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Internal method to change storage capacity for elements in dynamic array without changing values or order of
        elements.
        """

        # if new_capacity is less than elements in array or not positive, do nothing
        if new_capacity < StaticArray.length(self) or new_capacity <= 0:
            return

        # create a new bigger array
        new_array = StaticArray(new_capacity)

        # copy existing values from old array to new
        for i in range(StaticArray.length(self)):
            new_array[i] = StaticArray.get(self, i)

        self._capacity = new_capacity
        self._data = new_array

    def append(self, value: object) -> None:
        """
        Add new value to end of array and DOUBLE the capacity if it's full
        """
        # if capacity is equal to size, double the capacity & append to end of array
        if StaticArray.length(self) == self._capacity:
            new_capacity = self._capacity * 2
            self.resize(new_capacity)

        self._data[StaticArray.length(self)] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Insert a new value at specified index. If index is invalid, raise exception 'DynamicArrayException' and if
        array is full, double the capacity before adding value.
        """
        # if the index is less than 0 or greater than array, raise the exception
        if index < 0 or index > StaticArray.length(self):
            raise DynamicArrayException

        # if capacity is full, DOUBLE before adding new value
        if StaticArray.length(self) == self._capacity:
            new_capacity = self._capacity * 2
            self.resize(new_capacity)

        # insert value at specified index
        for i in range(StaticArray.length(self) - 1, index - 1, -1):
            self._data[i + 1] = self._data[i]

        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        1) Remove the element at the given index in the dynamic array.
        2) If the index is invalid, an exception is raised.
        3) If the number of elements in the array before removal is less than 1/4 of the current capacity and more
        than 10 elements, reduction occurs
        """
        # if the index is invalid, raise the exception
        if index < 0 or index >= self._size:
            raise DynamicArrayException

        # elements in array less than 1/4 capacity and capacity is greater than 10 elements, then reduction occurs
        if (self._size < self._capacity / 4) and (self._capacity >= 10):
            new_capacity = self._size * 2  # new capacity as twice number of current elements

            if new_capacity < 10:  # confirm capacity doesn't reduce to less than 10 elements
                new_capacity = 10
            self.resize(new_capacity)

        # iteration to remove specified index value and update the new array
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]

        self._data[self._size - 1] = None
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Return new DynamicArray with requested number of elements of original array starting with requested start index.
        If start index or size is invalid or not enough elements from start to end index, return DynamicArrayException
        """

        # create variable end_index
        end_index = start_index + size

        # if conditional for invalid start_index, size or not enough elements from start to end index
        if (start_index < 0) or (start_index >= self._size) or (end_index > self._size) or (size < 0):
            raise DynamicArrayException

        new_array = DynamicArray()

        # slice (starting at start_index and ending at start_index+ size) then append to the new_array
        for i in range(start_index, end_index):
            new_array.append(StaticArray.get(self, i))
        return new_array

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Append all elements from one array to another array, same order in which they are stored in input array
        """
        # iterate through second_da array and use append method to add to end of current array
        for i in range(second_da.length()):
            self.append(second_da[i])

    def map(self, map_func) -> "DynamicArray":
        """
        Creates new dynamic array by iterating through the array with the provided 'map_func' for each element
        """
        # create new dynamic array
        mapped_array = DynamicArray()

        # iterate through dynamic array and apply map func to index then append to new array
        for i in range(self.length()):
            mapping = map_func(self.get_at_index(i))
            mapped_array.append(mapping)
        return mapped_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Create new dynamic array from original array whose elements are true for 'filter_func'
        """
        # create new filtered array
        filtered_array = DynamicArray()

        # iterate through array and filter for those only true, append those elements to new array
        for i in range(self.length()):
            val = self.get_at_index(i)
            filtered = filter_func(val)

            if filtered:
                filtered_array.append(val)
        return filtered_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Apply 'reduce_func' to each element of dynamic array and return the result.
        If the optional parameter is not given, the first value in the array is used in place of it.
        If the dynamic array is empty, method returns value of initializer or None if one wasn't provided.
        """

        if self.length() == 0:                          # if array is empty, initializer is default None
            return initializer
        elif initializer is None:                       # if initializer is none, set it to first index of array
            reduced = self.get_at_index(0)
            start_index = 1                             # start index changes to second element in array
        else:
            reduced = initializer                       # if initializer is provided, start index stays on first element
            start_index = 0

        for i in range(start_index, self.length()):     # iterates through range from start_index to end of array
            position = self.get_at_index(i)             # assign index to variable position
            reduced = reduce_func(reduced, position)    # reduced is updated to return the final value
        return reduced


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives dynamic array in sorted order and return a tuple of the mode and an integer for the frequency.
    If there are 2 modes, return the first mode that appears.
    """
    current_mode = arr[0]
    current_freq = 1
    max_freq = 1
    mode_array = DynamicArray()

    for i in range(1, arr.length()):
        if arr[i] == current_mode:  # When elements are the same
            current_freq += 1
        else:  # When it's different
            if current_freq > max_freq:
                max_freq = current_freq  # Update max frequency
                mode_array = DynamicArray()
                mode_array.append(current_mode)  # Add current mode to mode array
            elif current_freq == max_freq:
                mode_array.append(current_mode)  # Add current mode to mode array

            current_mode = arr[i]  # Move to new element
            current_freq = 1

    if current_freq > max_freq:
        mode_array = DynamicArray()
        mode_array.append(current_mode)  # Add current mode to mode array
        return mode_array, current_freq
    elif current_freq == max_freq:
        mode_array.append(current_mode)  # Add current mode to mode array

    return mode_array, max_freq


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
