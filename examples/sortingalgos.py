def bubble_sort(array):
    '''
        Bubble sort implementation.

        Parameters
        ----------
        array : list
            The array to be sorted.

        Returns
        -------
        list
            The sorted array.

        Examples
        --------
        >>> bubble_sort([3, 2, 1])
        [1, 2, 3]
        
    '''
    n = len(array)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                already_sorted = False
        if already_sorted:
            break
    return array


def insertion_sort(array):
    '''
        Insertion sort implementation.

        Parameters
        ----------
        array : list
            The array to be sorted.

        Returns
        -------
        list
            The sorted array.

        Examples
        --------
        >>> insertion_sort([3, 2, 1])
        [1, 2, 3]
        
    '''
    for i in range(1, len(array)):
        key_item = array[i]
        j = i - 1

        while j >= 0 and array[j] > key_item:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key_item
    return array


def merge(left, right):
    '''
        Merge sort implementation.

        Parameters
        ----------
        left : list
            The left part of the array to be sorted.
        right : list
            The right part of the array to be sorted.

        Returns
        -------
        list
            The sorted array.

        Examples
        --------
        >>> merge([1, 2, 3], [4, 5, 6])
        [1, 2, 3, 4, 5, 6]
        
    '''
    if len(left) == 0:
        return right
    if len(right) == 0:
        return left
    
    result = []
    index_left = index_right = 0
    while len(result) < len(left) + len(right):
        if left[index_left] <= right[index_right]:
            result.append(left[index_left])
            index_left += 1
        else:
            result.append(right[index_right])
            index_right += 1

        if index_right == len(right):
            result += left[index_left:]
            break

        if index_left == len(left):
            result += right[index_right:]
            break
    return result