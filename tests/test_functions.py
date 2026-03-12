import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sorting_functions import bubble_sort, selection_sort, insertion_sort

def test_bubble_sort():
    data = [4, 2, 7, 1, 5]
    expected = [1, 2, 4, 5, 7]
    assert bubble_sort(data.copy()) == expected, "Bubble Sort failed"
    print("Bubble Sort test passed")

def test_selection_sort():
    data = [3, 8, 2, 6, 1]
    expected = [1, 2, 3, 6, 8]
    assert selection_sort(data.copy()) == expected, "Selection Sort failed"
    print("Selection Sort test passed")

def test_insertion_sort():
    data = [9, 4, 6, 2, 7]
    expected = [2, 4, 6, 7, 9]
    assert insertion_sort(data.copy()) == expected, "Insertion Sort failed"
    print("Insertion Sort test passed")

if __name__ == "__main__":
    test_bubble_sort()
    test_selection_sort()
    test_insertion_sort()