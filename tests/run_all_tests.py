"""Comprehensive test runner for all project tests."""

import sys
import os

# Add parent and src directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sorting_functions import bubble_sort, selection_sort, insertion_sort
from team import add_member, search_member, get_team_member_count, format_greeting


def print_section(title):
    """Print a formatted test section header."""
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def test_sorting_functions():
    """Test all sorting algorithm implementations."""
    print_section("SORTING FUNCTIONS TESTS")

    tests_passed = 0
    tests_total = 0

    # Bubble Sort
    tests_total += 1
    try:
        data = [4, 2, 7, 1, 5]
        expected = [1, 2, 4, 5, 7]
        result = bubble_sort(data.copy())
        assert result == expected, f"Expected {expected}, got {result}"
        print("✓ Bubble Sort test passed")
        print(f"  Input: {data}")
        print(f"  Output: {result}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Bubble Sort test failed: {e}")

    print()

    # Selection Sort
    tests_total += 1
    try:
        data = [3, 8, 2, 6, 1]
        expected = [1, 2, 3, 6, 8]
        result = selection_sort(data.copy())
        assert result == expected, f"Expected {expected}, got {result}"
        print("✓ Selection Sort test passed")
        print(f"  Input: {data}")
        print(f"  Output: {result}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Selection Sort test failed: {e}")

    print()

    # Insertion Sort
    tests_total += 1
    try:
        data = [9, 4, 6, 2, 7]
        expected = [2, 4, 6, 7, 9]
        result = insertion_sort(data.copy())
        assert result == expected, f"Expected {expected}, got {result}"
        print("✓ Insertion Sort test passed")
        print(f"  Input: {data}")
        print(f"  Output: {result}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Insertion Sort test failed: {e}")

    print()

    # Edge case: empty list
    tests_total += 1
    try:
        result = bubble_sort([])
        assert result == [], f"Expected empty list, got {result}"
        print("✓ Empty list handling test passed")
        print(f"  Input: []")
        print(f"  Output: {result}")
        print(f"  Description: Correctly handles empty list without crashing")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Empty list handling test failed: {e}")

    print()

    # Edge case: single element
    tests_total += 1
    try:
        result = bubble_sort([42])
        assert result == [42], f"Expected [42], got {result}"
        print("✓ Single element test passed")
        print(f"  Input: [42]")
        print(f"  Output: {result}")
        print(f"  Description: Correctly handles list with single element")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Single element test failed: {e}")

    return tests_passed, tests_total


def test_team_functions():
    """Test team management functions."""
    print_section("TEAM FUNCTIONS TESTS")

    tests_passed = 0
    tests_total = 0

    # Add member - success
    tests_total += 1
    try:
        members = []
        added, message = add_member(members, "Henrique", "henrique111")
        assert added is True, "Should return True on successful add"
        assert len(members) == 1, "Members list should have 1 member"
        assert members[0]["name"] == "Henrique", "Name should match"
        print("✓ Add member success test passed")
        print(f"  Action: Added 'Henrique' with GitHub '@henrique111'")
        print(f"  Members after: {members}")
        print(f"  Status: {message}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Add member success test failed: {e}")

    print()

    # Add member - duplicate detection
    tests_total += 1
    try:
        members = [{"name": "Henrique", "github_username": "henrique111"}]
        added, message = add_member(members, "Henrique", "other_username")
        assert added is False, "Should return False for duplicate name"
        assert len(members) == 1, "Members list should still have 1 member"
        print("✓ Duplicate name detection test passed")
        print(f"  Action: Attempted to add 'Henrique' with different GitHub handle")
        print(f"  Members after: {members}")
        print(f"  Status: {message}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Duplicate name detection test failed: {e}")

    print()

    # Add member - duplicate GitHub username
    tests_total += 1
    try:
        members = [{"name": "Henrique", "github_username": "henrique111"}]
        added, message = add_member(members, "Other Name", "henrique111")
        assert added is False, "Should return False for duplicate GitHub username"
        assert len(members) == 1, "Members list should still have 1 member"
        print("✓ Duplicate GitHub username detection test passed")
        print(f"  Action: Attempted to add different person with '@henrique111'")
        print(f"  Members after: {members}")
        print(f"  Status: {message}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Duplicate GitHub username detection test failed: {e}")

    print()

    # Search member - found
    tests_total += 1
    try:
        members = [
            {"name": "Vitalii", "github_username": "vitalii111"},
            {"name": "Ummay", "github_username": "ummay111"},
        ]
        results = search_member(members, "Vitalii")
        assert len(results) == 1, "Should find 1 member"
        assert results[0]["name"] == "Vitalii", "Should find correct member"
        print("✓ Search member found test passed")
        print(f"  Search term: 'Vitalii'")
        print(f"  Found: {results}")
        print(f"  Total members searched: {len(members)}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Search member found test failed: {e}")

    print()

    # Search member - not found
    tests_total += 1
    try:
        members = [{"name": "Vitalii", "github_username": "vitalii111"}]
        results = search_member(members, "Daniel")
        assert results == [], "Should return empty list when not found"
        print("✓ Search member not found test passed")
        print(f"  Search term: 'Daniel'")
        print(f"  Found: {results}")
        print(f"  Result: No matching members (expected behavior)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Search member not found test failed: {e}")

    print()

    # Get team member count
    tests_total += 1
    try:
        members = [
            {"name": "Alice", "github_username": "alice"},
            {"name": "Bob", "github_username": "bob"},
            {"name": "Charlie", "github_username": "charlie"},
        ]
        count = get_team_member_count(members)
        assert count == 3, f"Expected count 3, got {count}"
        print("✓ Get team member count test passed")
        print(f"  Team members: {[m['name'] for m in members]}")
        print(f"  Total count: {count}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Get team member count test failed: {e}")

    print()

    # Format greeting
    tests_total += 1
    try:
        greeting = format_greeting("The Last Slice")
        assert "The Last Slice" in greeting, "Greeting should include team name"
        assert "Welcome" in greeting, "Greeting should contain welcome message"
        print("✓ Format greeting test passed")
        print(f"  Team name: 'The Last Slice'")
        print(f"  Formatted greeting: '{greeting}'")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Format greeting test failed: {e}")

    return tests_passed, tests_total


def test_error_handling():
    """Test error handling and edge cases."""
    print_section("ERROR HANDLING TESTS")

    tests_passed = 0
    tests_total = 0

    # Invalid input - non-list members
    tests_total += 1
    try:
        result = search_member("not_a_list", "test")
        assert result == [], "Should return empty list for invalid members"
        print("✓ Invalid members list handling test passed")
        print(f"  Input: search_member('not_a_list', 'test')")
        print(f"  Result: {result}")
        print(f"  Description: Gracefully handles non-list members (no crash)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Invalid members list handling test failed: {e}")

    print()

    # Invalid input - empty search term
    tests_total += 1
    try:
        members = [{"name": "Test", "github_username": "test"}]
        result = search_member(members, "   ")
        assert result == [], "Should return empty list for whitespace search term"
        print("✓ Whitespace search term handling test passed")
        print(f"  Input: search_member(members, '   ')")
        print(f"  Result: {result}")
        print(f"  Description: Whitespace-only search terms are rejected")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Whitespace search term handling test failed: {e}")

    print()

    # Invalid input - blank name
    tests_total += 1
    try:
        members = []
        added, message = add_member(members, "   ", "valid_username")
        assert added is False, "Should not add member with blank name"
        print("✓ Blank name rejection test passed")
        print(f"  Input: add_member(members, '   ', 'valid_username')")
        print(f"  Result: {added}")
        print(f"  Status: {message}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Blank name rejection test failed: {e}")

    print()

    # Invalid input - blank GitHub username
    tests_total += 1
    try:
        members = []
        added, message = add_member(members, "Valid Name", "   ")
        assert added is False, "Should not add member with blank username"
        print("✓ Blank GitHub username rejection test passed")
        print(f"  Input: add_member(members, 'Valid Name', '   ')")
        print(f"  Result: {added}")
        print(f"  Status: {message}")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Blank GitHub username rejection test failed: {e}")

    print()

    # Empty member count
    tests_total += 1
    try:
        count = get_team_member_count([])
        assert count == 0, "Empty list should have count 0"
        print("✓ Empty member list count test passed")
        print(f"  Input: get_team_member_count([])")
        print(f"  Result: {count}")
        print(f"  Description: Empty list correctly returns 0")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Empty member list count test failed: {e}")

    print()

    # Non-list member count
    tests_total += 1
    try:
        count = get_team_member_count("not_a_list")
        assert count == 0, "Non-list input should return count 0"
        print("✓ Non-list member count handling test passed")
        print(f"  Input: get_team_member_count('not_a_list')")
        print(f"  Result: {count}")
        print(f"  Description: Invalid input gracefully returns 0 (no crash)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Non-list member count handling test failed: {e}")

    return tests_passed, tests_total


def main():
    """Run all test suites and report results."""
    import time
    
    print("\n" + "=" * 50)
    print("ALL TESTS RUNNER".center(50))
    print("=" * 50)
    print()

    start_time = time.time()

    total_passed = 0
    total_tests = 0

    # Run sorting tests
    passed, total = test_sorting_functions()
    total_passed += passed
    total_tests += total

    # Run team tests
    passed, total = test_team_functions()
    total_passed += passed
    total_tests += total

    # Run error handling tests
    passed, total = test_error_handling()
    total_passed += passed
    total_tests += total

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print summary
    print_section("TEST SUMMARY")
    print(f"Total tests run:  {total_tests}")
    print(f"Tests passed:     {total_passed}")
    print(f"Tests failed:     {total_tests - total_passed}")
    print(f"Success rate:     {(total_passed / total_tests * 100):.1f}%")
    print(f"Execution time:   {elapsed_time:.3f} seconds")
    print()

    if total_passed == total_tests:
        print("✓ All tests passed!")
        print()
        return 0
    else:
        print(f"✗ {total_tests - total_passed} test(s) failed.")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
