# The Last Slice - Team Management Tool

A Python-based CLI tool for managing team members with JSON data storage, interactive greetings, name analysis, sorting algorithms, and CSV export.

## CLI Usage

| Command | Description |
|---------|-------------|
| `--show-team` | Display all team members |
| `--display-list` | Show numbered list of members |
| `--count` | Show total number of members |
| `--add-member NAME GITHUB` | Add a new team member |
| `--search-member QUERY` | Search for a member |
| `--greet NAME` | Greet a team member |
| `--export-csv [FILENAME]` | Export team members to CSV file |

## Examples

```bash
# Show all team members
python src/main.py --show-team

# Add a new member
python src/main.py --add-member "John Doe" "johndoe"

# Search for a member
python src/main.py --search-member "John"

# Get member count
python src/main.py --count

# Export team to CSV
python src/main.py --export-csv

# Export with custom filename
python src/main.py --export-csv my_team.csv
```

## Running Tests

```bash

pip install pytest

pytest tests/ -v

```

## Project Structure

```text

The-Last-Slice-python/
├── .github/workflows/
│ └── ci.yml
├── data/
│ └── team_data.json
├── docs/
│ └── README.md
├── src/
│   ├── main.py
│   ├── sorting_functions.py
│   ├── team.py
│   └── utils.py
└── tests/
│   ├── test_functions.py
│   └── test_team.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Modules

The project is organized into four main modules, each with a specific responsibility.

### src/main.py
**Purpose:** Command-line interface (CLI) entry point.

This module handles user input, parses command-line arguments, and orchestrates the program flow.

**Key Functions:**
| Function | Description |
|----------|-------------|
| `parse_args()` | Configures and returns command-line argument parser using argparse |
| `main()` | Main program controller - loads data, processes arguments, calls team functions |

---

### src/team.py
**Purpose:** Core team management operations.

This module contains all data manipulation logic, JSON storage, and team member operations.

**Key Functions:**
| Function | Description | Returns |
|----------|-------------|---------|
| `load_team_data(file_path)` | Load team data from JSON file | dict |
| `save_team_data(file_path, team_data)` | Save team data to JSON file | None |
| `add_member(members, name, github)` | Add new member with duplicate validation | (bool, str) |
| `search_member(members, query)` | Search members by name or GitHub username | list |
| `display_member_list(members)` | Print numbered list of members | None |
| `get_team_member_count(members)` | Return number of team members | int |
| `display_team_summary(team_name, members, github)` | Show formatted team summary | None |
| `format_greeting(team_name)` | Create welcome message | str |
| `say_hello(members)` | Interactive greeting with menu | str |
| `count_name_lengths(members)` | Analyze and display name lengths | None |
| `export_to_csv(members, filename)` | Export team members to CSV file | (bool, str) |

---

### src/utils.py
**Purpose:** Console interaction utilities.

This module provides reusable helper functions for user interaction.

**Key Functions:**
| Function | Description |
|----------|-------------|
| `choose_from_list(options, title, prompt, cancelled_msg, invalid_msg)` | Displays a numbered menu and returns user's choice, with error handling |


---

### src/sorting_functions.py
**Purpose:** Sorting algorithm implementations.

This module provides classic sorting algorithms for data manipulation.

**Key Functions:**
| Function | Description | Time Complexity |
|----------|-------------|-----------------|
| `bubble_sort(arr)` | Bubble sort algorithm | O(n²) |
| `selection_sort(arr)` | Selection sort algorithm | O(n²) |
| `insertion_sort(arr)` | Insertion sort algorithm | O(n²) |
