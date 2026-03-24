def bubble_sort(arr):
    """Sort a list using Bubble Sort.
    
    Args:
        arr: List of comparable items.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If arr is not a list or contains non-comparable items.
    """
    try:
        if not isinstance(arr, list):
            raise TypeError("Input must be a list.")
        if len(arr) == 0:
            return arr
        
        arr_copy = arr.copy()
        n = len(arr_copy)
        for i in range(n):
            for j in range(0, n - i - 1):
                try:
                    if arr_copy[j] > arr_copy[j + 1]:
                        arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                except TypeError:
                    raise TypeError("List contains items that cannot be compared.")
        return arr_copy
    except TypeError as e:
        raise TypeError(f"Bubble sort error: {str(e)}")


def selection_sort(arr):
    """Sort a list using Selection Sort.
    
    Args:
        arr: List of comparable items.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If arr is not a list or contains non-comparable items.
    """
    try:
        if not isinstance(arr, list):
            raise TypeError("Input must be a list.")
        if len(arr) == 0:
            return arr
        
        arr_copy = arr.copy()
        n = len(arr_copy)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                try:
                    if arr_copy[j] < arr_copy[min_index]:
                        min_index = j
                except TypeError:
                    raise TypeError("List contains items that cannot be compared.")
            arr_copy[i], arr_copy[min_index] = arr_copy[min_index], arr_copy[i]
        return arr_copy
    except TypeError as e:
        raise TypeError(f"Selection sort error: {str(e)}")


def insertion_sort(arr):
    """Sort a list using Insertion Sort.
    
    Args:
        arr: List of comparable items.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If arr is not a list or contains non-comparable items.
    """
    try:
        if not isinstance(arr, list):
            raise TypeError("Input must be a list.")
        if len(arr) == 0:
            return arr
        
        arr_copy = arr.copy()
        for i in range(1, len(arr_copy)):
            key = arr_copy[i]
            j = i - 1
            while j >= 0:
                try:
                    if arr_copy[j] > key:
                        arr_copy[j + 1] = arr_copy[j]
                        j -= 1
                    else:
                        break
                except TypeError:
                    raise TypeError("List contains items that cannot be compared.")
            arr_copy[j + 1] = key
        return arr_copy
    except TypeError as e:
        raise TypeError(f"Insertion sort error: {str(e)}")
