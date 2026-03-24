# Error Handling Quick Guide

Goal: program should not crash on incorrect input.

## Where It Is Implemented

- `src/main.py`: wraps CLI flow in try/except, validates loaded data shape, handles file/JSON errors, and shows user-friendly messages.
- `src/team.py`: validates member inputs, duplicate checks, safe search behavior, and handles read/write failures.
- `src/utils.py`: validates list-choice input and handles invalid/empty input and Ctrl+C.
- `src/sorting_functions.py`: validates list input and raises clear TypeError messages for invalid values.

## Run The Error-Handling Checks

Use the dedicated runner:

```powershell
python tests\test_error_handling_runner.py
```

What it checks:

- duplicate member detection
- blank value validation
- search with and without matches
- invalid sorting input (`"not a list"`)
- empty list and normal sorting cases
- invalid options list in utilities

## Expected Result

- Tests print `PASS`/`FAIL` per case.
- Invalid inputs are handled with readable messages.
- No unhandled crash during tested scenarios.
