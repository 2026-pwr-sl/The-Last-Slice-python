# The Last Slice - Team Management Tool

A Python-based CLI tool for managing team members with JSON data storage.

## CLI Usage

| Command | Description |
|---------|-------------|
| `--show-team` | Display all team members |
| `--display-list` | Show numbered list of members |
| `--count` | Show total number of members |
| `--add-member NAME GITHUB` | Add a new team member |
| `--search-member QUERY` | Search for a member |
| `--greet NAME` | Greet a team member |

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
```

## Running Tests

```bash

# pip install pytest

# pytest tests/ -v

```

## Project Structure

```text

# The-Last-Slice-python/

# ├── src/

# │   ├── main.py

# │   ├── team.py

# │   └── utils.py

# ├── data/

# │   └── team\_data.json

# └── tests/

# &#x20;   └── test\_functions.py

# ```

