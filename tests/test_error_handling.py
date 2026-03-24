"""Comprehensive error handling tests for The Last Slice project."""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from team import add_member, search_member
from sorting_functions import bubble_sort, selection_sort, insertion_sort
from utils import choose_from_list


def test_team_module():
    """Test team module error handling."""
    print("=" * 50)
    print("TEAM MODULE TESTS")
    print("=" * 50)
    
    # Test 1: Add member success
    members = []
    added, message = add_member(members, 'Henrique', 'henrique111')
    print(f'✓ Test 1 - Add member success: {"PASS" if added else "FAIL"}')
    
    # Test 2: Add duplicate member
    added, message = add_member(members, 'Henrique', 'henrique111')
    print(f'✓ Test 2 - Duplicate detection: {"PASS" if not added else "FAIL"}')
    print(f'  Message: {message}')
    
    # Test 3: Add member with blank spaces
    added, message = add_member(members, '   ', '   ')
    print(f'✓ Test 3 - Blank input validation: {"PASS" if not added else "FAIL"}')
    print(f'  Message: {message}')
    
    # Test 4: Search member
    results = search_member(members, 'Henrique')
    print(f'✓ Test 4 - Search member: {"PASS" if len(results) == 1 else "FAIL"}')
    
    # Test 5: Search with no results
    results = search_member(members, 'NoOne')
    print(f'✓ Test 5 - No search results: {"PASS" if len(results) == 0 else "FAIL"}')


def test_sorting_functions():
    """Test sorting functions error handling."""
    print("\n" + "=" * 50)
    print("SORTING FUNCTIONS TESTS")
    print("=" * 50)
    
    # Test 1: Valid input
    try:
        result = bubble_sort([5, 2, 8, 1])
        print(f'✓ Test 1 - Bubble sort valid input: {"PASS" if result == [1, 2, 5, 8] else "FAIL"}')
    except Exception as e:
        print(f'✗ Test 1 - FAIL: {e}')
    
    # Test 2: Invalid input (not a list)
    try:
        bubble_sort('not a list')
        print(f'✗ Test 2 - Should have raised TypeError')
    except TypeError as e:
        print(f'✓ Test 2 - Invalid input caught: PASS')
        print(f'  Error: {e}')
    
    # Test 3: Empty list
    try:
        result = bubble_sort([])
        print(f'✓ Test 3 - Empty list: {"PASS" if result == [] else "FAIL"}')
    except Exception as e:
        print(f'✗ Test 3 - FAIL: {e}')
    
    # Test 4: Single element
    try:
        result = bubble_sort([1])
        print(f'✓ Test 4 - Single element: {"PASS" if result == [1] else "FAIL"}')
    except Exception as e:
        print(f'✗ Test 4 - FAIL: {e}')
    
    # Test 5: Selection sort
    try:
        result = selection_sort([3, 1, 4, 1, 5])
        print(f'✓ Test 5 - Selection sort: {"PASS" if result == [1, 1, 3, 4, 5] else "FAIL"}')
    except Exception as e:
        print(f'✗ Test 5 - FAIL: {e}')
    
    # Test 6: Insertion sort
    try:
        result = insertion_sort([3, 1, 4, 1, 5])
        print(f'✓ Test 6 - Insertion sort: {"PASS" if result == [1, 1, 3, 4, 5] else "FAIL"}')
    except Exception as e:
        print(f'✗ Test 6 - FAIL: {e}')


def test_utils():
    """Test utils module error handling."""
    print("\n" + "=" * 50)
    print("UTILS MODULE TESTS")
    print("=" * 50)
    
    # Test 1: Empty options list
    result, error = choose_from_list(
        [],
        "Choose:",
        "Enter choice: ",
        "Cancelled",
        "Invalid"
    )
    print(f'✓ Test 1 - Empty options validation: {"PASS" if result is None else "FAIL"}')
    print(f'  Error: {error}')
    
    # Test 2: Valid options (this will wait for input, so we skip it in automated tests)
    print(f'✓ Test 2 - Valid options: (skipped - requires user input)')


if __name__ == "__main__":
    test_team_module()
    test_sorting_functions()
    test_utils()
    print("\n" + "=" * 50)
    print("ALL ERROR HANDLING TESTS COMPLETED!")
    print("=" * 50)
