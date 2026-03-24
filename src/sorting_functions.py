def bubble_sort(arr):
    """Sort a list using Bubble Sort.
    
    Args:
        arr: List of comparable elements.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If input is not a list or elements are not comparable.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    if len(arr) <= 1:
        return arr
    
    try:
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    except TypeError as e:
        raise TypeError("All elements in the list must be comparable.") from e


def selection_sort(arr):
    """Sort a list using Selection Sort.
    
    Args:
        arr: List of comparable elements.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If input is not a list or elements are not comparable.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    if len(arr) <= 1:
        return arr
    
    try:
        n = len(arr)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
        return arr
    except TypeError as e:
        raise TypeError("All elements in the list must be comparable.") from e


def insertion_sort(arr):
    """Sort a list using Insertion Sort.
    
    Args:
        arr: List of comparable elements.
        
    Returns:
        Sorted list.
        
    Raises:
        TypeError: If input is not a list or elements are not comparable.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    if len(arr) <= 1:
        return arr
    
    try:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
    except TypeError as e:
        raise TypeError("All elements in the list must be comparable.") from e
