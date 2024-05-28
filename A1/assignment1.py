# Name: Harpreet Sahota
# OSU Email: sahotaha@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A1 - Python Fundamentals Review
# Due Date: 10/23/23
# Description: Python fundamentals practice


import random
from static_array import *


# ------------------- PROBLEM 1 - MIN_MAX -----------------------------------


def min_max(arr: StaticArray) -> tuple[int, int]:
    """
    Return tuple with min and max value of the input array
    """
    minimum = maximum = arr.get(0)

    for i in range(1, arr.length()):
        num = arr.get(i)
        if num < minimum:
            minimum = num
        elif num > maximum:
            maximum = num
    return minimum, maximum


# ------------------- PROBLEM 2 - FIZZ_BUZZ ---------------------------------

def fizz_buzz(arr: StaticArray) -> StaticArray:
    """
    Receives array of integers and replaces wtih 'fizz' if number is divisible by 3 and 'buzz' if divisible by 5. If
    multiple of 3 and 5, replace integer with 'fizzbuzz'. If neither, no change occurs to that element.
    """
    result_arry = StaticArray(arr.length())  # new static array to avoid modifying original static array

    for i in range(arr.length()):
        num = arr.get(i)

        if num % 3 == 0 and num % 5 == 0:
            result_arry.set(i, 'fizzbuzz')
        elif num % 3 == 0:
            result_arry.set(i, 'fizz')
        elif num % 5 == 0:
            result_arry.set(i, 'buzz')
        else:
            result_arry.set(i, num)
    return result_arry


# ------------------- PROBLEM 3 - REVERSE -----------------------------------

def reverse(arr: StaticArray) -> None:
    """
    Receives the StaticArray and reverses the order modifying original array without creating a new array
    """
    starting = 0
    ending = arr.length() - 1

    while starting < ending:
        arr[starting], arr[ending] = arr[ending], arr[starting]
        starting += 1
        ending -= 1


# ------------------- PROBLEM 4 - ROTATE ------------------------------------

def rotate(arr: StaticArray, steps: int) -> StaticArray:
    """
    Receives 2 parameters (StaticArray and Integer value) creating a new StaticArray with elements of original
    array but position shifts right by integer value if positive and left by integer value if negative.
    """

    length = arr.length()  # length of array
    allowed_steps = steps % length  # steps allowed that are in the range of 0 - length, right/left

    new_order = StaticArray(length)  # create new array, same length as original

    for i in range(length):
        new_pos = (i + allowed_steps) % length  # new position after the steps are done
        new_order.set(new_pos, arr.get(i))  # places in the new index
    return new_order


# ------------------- PROBLEM 5 - SA_RANGE ----------------------------------

def sa_range(start: int, end: int) -> StaticArray:
    """
    Receives start and end integers and returns StaticArray of all consecutive integers between those two
    """

    numbers = abs(end - start) + 1  # calculate numbers between start-end
    new_arry = StaticArray(numbers)
    step = 1 if start <= end else -1  # increase or decrease consecutive integers

    for i in range(numbers):
        new_arry.set(i, start)
        start += step
    return new_arry


# ------------------- PROBLEM 6 - IS_SORTED ---------------------------------

def is_sorted(arr: StaticArray) -> int:
    """
    Receive StaticArray and return integer either:
         1 - if array is sorted in ascending order
        -1 - if list is sorted in descending order
         0 - if neither
    """
    a_array = arr.length()
    ascend = descend = False

    for i in range(1, a_array):
        if arr.get(i) < arr.get(i - 1):  # if descending return True
            descend = True
        elif arr.get(i) > arr.get(i - 1):  # if ascending return True
            ascend = True
        elif arr.get(i) == arr.get(i - 1):  # if i and i+1 is same return 0
            return 0

    if ascend and descend:
        return 0
    elif descend:
        return -1
    elif ascend or a_array <= 1:
        return 1
    return 0


# ------------------- PROBLEM 7 - FIND_MODE -----------------------------------

def find_mode(arr: StaticArray) -> tuple[object, int]:
    """
    Receive a sorted StaticArray in either non-descending or non-ascending order and return the mode and frequency.
    If there are two modes, return the first mode that appears in array.
    """

    mode = None  # initial value is set to none
    max_count = 0  # initial value of the count for the mode set to 0

    for i in range(arr.length()):
        current_value = arr.get(i)  # current value in array
        current_count = 1  # initial count will start at 1

        # if the current_value repeats in array, increase count by 1 for each occurrence
        for j in range(i + 1, arr.length()):
            if arr.get(j) == current_value:
                current_count += 1

        if current_count > max_count or (current_count == max_count and mode is None):
            max_count = current_count
            mode = current_value

    return mode, max_count


# ------------------- PROBLEM 8 - REMOVE_DUPLICATES -------------------------

def remove_duplicates(arr: StaticArray) -> StaticArray:
    """
    Receives a sorted array and function returns new StaticArray with duplicates removed
    """

    if arr.length() <= 1:  # if only 1 element, return array
        return arr

    no_duplicates = StaticArray(arr.length())  # Create array for no duplicates
    no_duplicates.set(0, arr.get(0))  # set the first index
    no_d_index = 1  # separate index for duplicate

    for i in range(1, arr.length()):
        current_num = arr.get(i)  # current num
        prev_num = arr.get(i - 1)  # previous num

        if current_num != prev_num:  # if current num different, add to array
            no_duplicates.set(no_d_index, current_num)
            no_d_index += 1

    new_arry = StaticArray(no_d_index)  # create new array after duplicates removed
    for i in range(no_d_index):
        new_arry.set(i, no_duplicates.get(i))  # add each element to this array

    return new_arry


# ------------------- PROBLEM 9 - COUNT_SORT --------------------------------

def count_sort(arr: StaticArray) -> StaticArray:
    """
    Return a new StaticArray with same content of array received and return in non-ascending order.
    """
    # set the min and max bounds for array
    min_num = 10 ** 9
    max_num = -10 ** 9

    # finding the min and max in the input array
    for i in range(arr.length()):
        current_value = arr[i]
        if current_value < min_num:
            min_num = current_value
        if current_value > max_num:
            max_num = current_value

    range_arry = max_num - min_num + 1  # determine range size between max and min
    count_array = StaticArray(range_arry)  # set new array to keep count

    # determine the count of each value in array occurring
    for i in range(range_arry):
        count_array[i] = 0

    for i in range(arr.length()):
        current_value = arr[i]
        count_array[current_value - min_num] += 1

    # set the results array and initialize index to 0 to keep track of position
    results_array = StaticArray(arr.length())
    position = 0

    # loop through the array and assign in the results array
    for i in range(range_arry - 1, -1, -1):
        for m in range(count_array[i]):
            results_array[position] = i + min_num
            position += 1
    return results_array


# ------------------- PROBLEM 10 - SORTED SQUARES ---------------------------

def sorted_squares(arr: StaticArray) -> StaticArray:
    """
    Return a new StaticArray with squares of the values from original array sorted in non-descending order
    """
    # assign arr length and StaticArray (new array) length to variables
    length = arr.length()
    squares_array = StaticArray(length)

    neg_pointer = 0  # keep track of last negative element
    non_neg_pointer = 0  # locate first non-negative element
    result_pointer = 0  # keep track of position where squared values will be inserted

    while non_neg_pointer < length and arr.get(non_neg_pointer) < 0:
        non_neg_pointer += 1

    neg_pointer = non_neg_pointer - 1

    # merge together the positive & negative squares
    while neg_pointer >= 0 and non_neg_pointer < length:
        neg_value = arr.get(neg_pointer)
        non_neg_value = arr.get(non_neg_pointer)

        # calculates square if negative and if positive
        neg_square = neg_value ** 2
        non_neg_square = non_neg_value * non_neg_value

        # compares square value and adds smaller to the results array first
        if neg_square < non_neg_square:
            squares_array.set(result_pointer, neg_square)
            neg_pointer -= 1
        else:
            squares_array.set(result_pointer, non_neg_square)
            non_neg_pointer += 1
        result_pointer += 1

    # loop to add negative values to the square array
    while neg_pointer >= 0:
        squares_array.set(result_pointer, arr.get(neg_pointer) ** 2)
        neg_pointer -= 1
        result_pointer += 1

    # loop to add positive values to the square array
    while non_neg_pointer < length:
        squares_array.set(result_pointer, arr.get(non_neg_pointer) ** 2)
        non_neg_pointer += 1
        result_pointer += 1

    return squares_array


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# min_max example 1')
    arr = StaticArray(5)
    for i, value in enumerate([7, 8, 6, -5, 4]):
        arr[i] = value
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]: 3}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 2')
    arr = StaticArray(1)
    arr[0] = 100
    print(arr)
    result = min_max(arr)
    if result:
        print(f"Min: {result[0]}, Max: {result[1]}")
    else:
        print("min_max() not yet implemented")

    print('\n# min_max example 3')
    test_cases = (
        [3, 3, 3],
        [-10, -30, -5, 0, -10],
        [25, 50, 0, 10],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        result = min_max(arr)
        if result:
            print(f"Min: {result[0]: 3}, Max: {result[1]}")
        else:
            print("min_max() not yet implemented")

    print('\n# fizz_buzz example 1')
    source = [_ for _ in range(-5, 20, 4)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(fizz_buzz(arr))
    print(arr)

    print('\n# reverse example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    reverse(arr)
    print(arr)
    reverse(arr)
    print(arr)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr.set(i, value)
    print(arr)
    for steps in [1, 2, 0, -1, -2, 28, -100, 2 ** 28, -2 ** 31]:
        space = " " if steps >= 0 else ""
        print(f"{rotate(arr, steps)} {space}{steps}")
    print(arr)

    print('\n# rotate example 2')
    array_size = 1_000_000
    source = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(source))
    for i, value in enumerate(source):
        arr[i] = value
    print(f'Started rotating large array of {array_size} elements')
    rotate(arr, 3 ** 14)
    rotate(arr, -3 ** 15)
    print(f'Finished rotating large array of {array_size} elements')

    print('\n# sa_range example 1')
    cases = [
        (1, 3), (-1, 2), (0, 0), (0, -3),
        (-95, -89), (-89, -95)]
    for start, end in cases:
        print(f"Start: {start: 4}, End: {end: 4}, {sa_range(start, end)}")

    print('\n# is_sorted example 1')
    test_cases = (
        [-100, -8, 0, 2, 3, 10, 20, 100],
        ['A', 'B', 'Z', 'a', 'z'],
        ['Z', 'T', 'K', 'A', '5'],
        [1, 3, -10, 20, -30, 0],
        [-10, 0, 0, 10, 20, 30],
        [100, 90, 0, -90, -200],
        ['apple']
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        result = is_sorted(arr)
        space = "  " if result and result >= 0 else " "
        print(f"Result:{space}{result}, {arr}")

    print('\n# find_mode example 1')
    test_cases = (
        [1, 20, 30, 40, 500, 500, 500],
        [2, 2, 2, 2, 1, 1, 1, 1],
        ["zebra", "sloth", "otter", "otter", "moose", "koala"],
        ["Albania", "Belgium", "Chile", "Denmark", "Egypt", "Fiji"]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value

        result = find_mode(arr)
        if result:
            print(f"{arr}\nMode: {result[0]}, Frequency: {result[1]}\n")
        else:
            print("find_mode() not yet implemented\n")

    print('# remove_duplicates example 1')
    test_cases = (
        [1], [1, 2], [1, 1, 2], [1, 20, 30, 40, 500, 500, 500],
        [5, 5, 5, 4, 4, 3, 2, 1, 1], [1, 1, 1, 1, 2, 2, 2, 2]
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        print(arr)
        print(remove_duplicates(arr))
    print(arr)

    print('\n# count_sort example 1')
    test_cases = (
        [1, 2, 4, 3, 5], [5, 4, 3, 2, 1], [0, -5, -3, -4, -2, -1, 0],
        [-3, -2, -1, 0, 1, 2, 3], [1, 2, 3, 4, 3, 2, 1, 5, 5, 2, 3, 1],
        [10100, 10721, 10320, 10998], [-100320, -100450, -100999, -100001],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(case):
            arr[i] = value
        before = arr if len(case) < 50 else 'Started sorting large array'
        print(f"Before: {before}")
        result = count_sort(arr)
        after = result if len(case) < 50 else 'Finished sorting large array'
        print(f"After : {after}")

    print('\n# count_sort example 2')
    array_size = 5_000_000
    min_val = random.randint(-1_000_000_000, 1_000_000_000 - 998)
    max_val = min_val + 998
    case = [random.randint(min_val, max_val) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(case):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = count_sort(arr)
    print(f'Finished sorting large array of {array_size} elements')

    print('\n# sorted_squares example 1')
    test_cases = (
        [1, 2, 3, 4, 5],
        [-5, -4, -3, -2, -1, 0],
        [-3, -2, -2, 0, 1, 2, 3],
    )
    for case in test_cases:
        arr = StaticArray(len(case))
        for i, value in enumerate(sorted(case)):
            arr[i] = value
        print(arr)
        result = sorted_squares(arr)
        print(result)

    print('\n# sorted_squares example 2')
    array_size = 5_000_000
    case = [random.randint(-10 ** 9, 10 ** 9) for _ in range(array_size)]
    arr = StaticArray(len(case))
    for i, value in enumerate(sorted(case)):
        arr[i] = value
    print(f'Started sorting large array of {array_size} elements')
    result = sorted_squares(arr)
    print(f'Finished sorting large array of {array_size} elements')


class DynamicArray:
    def __init__(self):
        self.data = []
        self.size = 0

    def append(self, value):
        self.data.append(value)
        self.size += 1

    def remove_at_index(self, index):
        if 0 <= index < self.size:
            del self.data[index]
            self.size -= 1

    def magic(self) -> None:
        for i in range(self.size - 1, -1, -1):
            self.append(self.data[i])
            self.remove_at_index(i)