def sayHello():
    '''
    This function says hello.

    Inputs: None

    '''
    print("Hello")


def insertionSort(arr):
    '''
    Insertion Sort
==============

    Insertion sort is a simple sorting algorithm that works the way we sort playing cards in our hands.

    Algorithm
---------

    Insertion sort iterates, consuming one input element each repetition, and growing a sorted output list.

    At each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list, and inserts it there.
    It repeats until no input elements remain.

    Example 1:
----------

    Input: [1, 2, 3, 4, 5]
    Output: [1, 2, 3, 4, 5]

    Example 2:
----------

    Input: [5, 2, 4, 6, 1, 3]
    Output: [1, 2, 3, 4, 5, 6]


    '''
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
	
def outerFunction():
    '''
    This is a docstring for the outerFunction.
    
    This function contains an innerFunction which is a high quality docstring for the innerFunction.
    
    Parameters:
        None
        
    Returns:
        None

    '''
    def innerFunction():
    '''
    A function that prints "hello"

:return: None

    '''
        print("hello")
    for i in range(5):
        innerFunction()


