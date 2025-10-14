
Objective (Arrays and Lists):

To understand the concept of arrays and lists in Python for storing multiple data elements.

To learn how to create, access, modify, and manipulate lists and arrays.

To practice using lists and arrays with loops and functions for efficient data handling.

To explore the difference between lists and arrays and their suitable use cases.Introduction:
Python provides several tools to store and manage multiple data elements efficiently.

Lists are Python’s built-in data structures that can hold multiple items in an ordered sequence.

Arrays (from the array module) are similar to lists but store only homogeneous data types, making them memory-efficient for large numerical data.

Lists in Python:

Lists are mutable, meaning elements can be added, removed, or modified.

Syntax:

fruits = ["Apple", "Banana", "Mango"]
print(fruits[0])       # Apple
fruits.append("Orange") # Add new item
fruits.remove("Banana") # Remove item


Lists can store mixed data types:

my_list = [10, "Python", 3.14, True]


Arrays in Python:

Arrays require the array module and can store only elements of the same type.

Syntax Example:

import array as arr
numbers = arr.array('i', [1, 2, 3, 4, 5])  # 'i' for integer type
numbers.append(6)
print(numbers[2])  # 3


Benefits of arrays:

Efficient memory usage for large datasets

Faster operations on numeric data

Work Done:

Created and manipulated lists:

students = ["Manjot", "Jyoti", "Rahul"]
students.append("Amit")
students.remove("Rahul")
print(students)


Accessed elements using indexing and slicing:

print(students[0])       # Manjot
print(students[1:3])     # ['Jyoti', 'Amit']


Looped through lists using for loop:

for student in students:
    print(student)


Created arrays using the array module and performed operations:

import array as arr
numbers = arr.array('i', [10, 20, 30, 40])
numbers.append(50)
numbers.pop(1)
print(numbers)


Combined functions and lists:

def sum_list(lst):
    total = 0
    for num in lst:
        total += num
    return total

print(sum_list([10, 20, 30]))  # 60


Output:

Lists and arrays correctly stored multiple values and allowed modifications:

['Manjot', 'Jyoti', 'Amit']
Manjot
['Jyoti', 'Amit']


Array operations executed successfully:

array('i', [10, 30, 40, 50])


Functions correctly processed list data:

60


Learning / Observations:

Lists are flexible and can store mixed data types, suitable for general-purpose programming.

Arrays are memory-efficient but require homogeneous data types.

Combining lists/arrays with functions enables modular and reusable code.

Learned how to loop through, modify, and manipulate lists/arrays, which is useful for storing project data like weather readings in our app.

Understanding lists and arrays is essential for data handling in Python projects.
