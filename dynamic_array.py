# Name: Marc Hamilton
# OSU Email: hamimarc@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and ADT Implementation
# Due Date: 4/26/2025
# Description: Creating DynamicArray functionality

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
        Creates a new array to the inputed size and copies all values inside the old array into the new

        :param new_capacity: an integer representing the new size of the array
        """
        if new_capacity <= 0 or new_capacity < self._size:
            return
        # creates new array with the new size
        new_arr = StaticArray(new_capacity)
        for i in range(self._size):
            new_arr.set(i, self.get_at_index(i))
        # sets the data and capacity in the dynamic array equal to the new values
        self._data = new_arr
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        adds a new value to the array (appending it) and if the array is too small doubles the size of the array

        :param value: an object being added to the array
        """
        # doubles the size of the array if it is full
        if self._capacity == self._size:
            self.resize(self._capacity * 2)
        # adds the new value
        self._data.set(self._size, value)
        self._size += 1


    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a new value at a specified index, if the location has a value already shifts it to the right.

        :param index: an integer that represents the location the new value is going
        :param value: an object that represents the item that is being added to the array
        """
        if index < 0 or index > self._size:
            raise DynamicArrayException("Index is not Valid")
        if self._capacity == self._size:
            self.resize(self._capacity * 2)
        # shifts all the values to the right by going right to left and moving the over one
        for i in range(self._size, index, -1):
            self._data.set(i, self.get_at_index(i - 1))
        # adds the new value at the inputed index
        self._data.set(index, value)
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes a value at the inputed index

        :param index: the index associated with the value being removed
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Index is not Valid")
        # checks if the array is less than 1/4 filled and if the capacity is more than 10
        if self._size < self._capacity / 4 and self._capacity > 10:
            new_capacity = max(self._size * 2, 10)
            self.resize(new_capacity)
        # removes the value at the inputted index and shift all other values to the left
        for i in range(index, self._size - 1):
            self._data.set(i, self.get_at_index(i + 1))
        self._size -= 1


    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Creates a new Dynamic array with a set size that copies values from another array till the new one is full

        :param start_index: an integer that represents where the copying will start
        :param size: an integer that represents the size of the new array

        :return: An array containing a slice of the original array
        """
        if start_index < 0 or size < 0 or start_index >= self._size or start_index + size > self._size:
            raise DynamicArrayException("Index is not Valid")

        slice_arr = DynamicArray()
        for i in range(size):
            # adds the values in the slice from the old array to the new one by appending it to the end of the new one
            slice_arr.append(self.get_at_index(start_index + i))
        return slice_arr

    def map(self, map_func) -> "DynamicArray":
        """
        Applies a map function to every element in an array and saves it to a new Dynamic array

        :param map_func: a function that applies some type of math formula to inputed integer

        :return: a new dynamic array with the map function applied to every element.
        """
        map_arr = DynamicArray()
        for i in range(self._size):
            # applies the map function to every element in the original array and appends it to the map_arr
            map_arr.append(map_func(self.get_at_index(i)))
        return map_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Filters through an array and saves values that match the filter to a new Dynamic array

        :param filter_func: a function that checks if an element matches the filter(returns true if it does)

        :return: a new dynamic array with only elements that the filter_func returned true to
        """
        filter_arr = DynamicArray()
        for i in range(self._size):
            # applies the map function to every element in the original array and appends it to the map_arr
            if filter_func(self.get_at_index(i)):
                filter_arr.append((self.get_at_index(i)))
        return filter_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Applied the reduce function to an array and returns the value of the function

        :param reduce_func: represents the function of how all the elements will be combined
        :param initializer: Represents the first integer to be considered in the reduce_func (set to none on default)

        :return: an object that represents the value of all the elements being combined using the reduce_func
        """
        if self._size == 0:
            return initializer
        reduce_result = initializer
        index = 0
        # checks if the there is an initializer
        if initializer is None:
            reduce_result = self.get_at_index(0)
            index = 1
        # applies the reduce function to the array and saves it to the new Dynamic Array
        for i in range(index, self._size):
            reduce_result = reduce_func(reduce_result, self.get_at_index(i))
        return reduce_result


def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    Creates an array of arrays that are filled with subsets of the original array all sorted in non-descending

    :param arr: a dynamic array

    :return: an array of arrays with each array starting when the elements are found to not be in non-descending order
    """
    # checks if the array is empty and ends the function early if it is
    if arr.length() == 0:
        return arr
    chunk_arr = DynamicArray()
    current_chunk = DynamicArray()
    current_chunk.append(arr.get_at_index(0))

    for i in range(1, arr.length()):
        # checks if the two elements are non-descending
        if arr.get_at_index(i) >= arr.get_at_index(i - 1):
            current_chunk.append(arr.get_at_index(i))
        else:
            chunk_arr.append(current_chunk)
            current_chunk = DynamicArray()
            # makes sure the new array starts with the next index and doesn't get removed
            current_chunk.append(arr.get_at_index(i))
    chunk_arr.append(current_chunk)
    return chunk_arr


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds all values that appear the most frequently and returns their value and frequency

    :param arr: a dynamic array that is being examined

    :return: a tuple with the value that appear the most frequently and the number of times they appear in the array
    """
    if arr.length() == 0:
        return DynamicArray(), 0

    mode_arr = DynamicArray()
    max_freq = 1
    current_freq = 1
    current_val = arr.get_at_index(0)

    for i in range(1, arr.length()):
        # looks at the next value to see if they are equal
        next_val = arr.get_at_index(i)
        if next_val == current_val:
            current_freq += 1
        else:
            if current_freq > max_freq:
                max_freq = current_freq
                # creates a new dynamic array to reset the mode
                mode_arr = DynamicArray()
                mode_arr.append(current_val)
            elif current_freq == max_freq:
                # if the values share the same frequency add the new value to the array holding modes
                mode_arr.append(current_val)
            #resets the search for the frequency of the new element
            current_val = next_val
            current_freq = 1
    # one last check to make sure the mode is accurate
    if current_freq > max_freq:
        mode_arr = DynamicArray()
        mode_arr.append(current_val)
        max_freq = current_freq
    elif current_freq == max_freq:
        mode_arr.append(current_val)
    return mode_arr, max_freq



# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize example 1")
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

    print("\n# resize example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index example 1")
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

    print("\n# remove_at_index example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index example 3")
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

    print("\n# remove at index example 4")
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

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode example 1")
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
