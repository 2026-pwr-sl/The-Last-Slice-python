"""Team-related data operations and formatting."""

import json

from utils import choose_from_list

GREETINGS = [
    "Hello",
    "Hi",
    "Hey",
    "Greetings",
    "Salutations",
    "Dzien dobry",
    "Hola",
    "Bonjour",
    "Ciao",
]


def load_team_data(file_path):
    """Load team data from a JSON file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        Tuple of (team_data, error_message). Returns (None, error_msg) on failure.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            team_data = json.load(file)
            
        # Validate required fields
        if "team_name" not in team_data or "members" not in team_data:
            return None, "Error: Data file is missing required fields ('team_name' or 'members')."
        
        if not isinstance(team_data["members"], list):
            return None, "Error: 'members' field must be a list."
        
        return team_data, None
        
    except FileNotFoundError:
        return None, f"Error: Data file not found at {file_path}. Please check the file path."
    except json.JSONDecodeError as e:
        return None, f"Error: Data file is not valid JSON. Details: {str(e)}"
    except Exception as e:
        return None, f"Error: Failed to load team data. Details: {str(e)}"


def save_team_data(file_path, team_data):
    """Persist team data to a JSON file.
    
    Args:
        file_path: Path to save the JSON file.
        team_data: Dictionary containing team information.
        
    Returns:
        Tuple of (success, message). Returns (False, error_msg) on failure.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(team_data, file, indent=2)
        return True, "Team data saved successfully."
    except IOError as e:
        return False, f"Error: Failed to write to file. Details: {str(e)}"
    except Exception as e:
        return False, f"Error: Failed to save team data. Details: {str(e)}"


def add_member(members, name, github_username):
    """Add a member dictionary to the list if it does not already exist.
    
    Args:
        members: List of member dictionaries.
        name: Member's name.
        github_username: Member's GitHub username.
        
    Returns:
        Tuple of (success, message).
    """
    # Validate input
    if not name or not isinstance(name, str):
        return False, "Error: Name must be a non-empty string."
    if not github_username or not isinstance(github_username, str):
        return False, "Error: GitHub username must be a non-empty string."
    
    name = name.strip()
    github_username = github_username.strip()
    
    if not name or not github_username:
        return False, "Error: Name and GitHub username cannot be blank."
    
    # Check for duplicates
    for member in members:
        same_name = member["name"].strip().lower() == name.lower()
        same_github = (
            member["github_username"].strip().lower() == github_username.lower()
        )
        if same_name or same_github:
            return False, "Error: Member already exists (name or GitHub username)."

    members.append(
        {
            "name": name,
            "github_username": github_username,
        }
    )
    return True, "Member added successfully."


def search_member(members, search_term):
    """Return members that match by name or GitHub username.
    
    Args:
        members: List of member dictionaries.
        search_term: Search query string.
        
    Returns:
        List of matching members, or empty list if no matches.
    """
    if not search_term or not isinstance(search_term, str):
        return []
    
    normalized_term = search_term.strip().lower()
    if not normalized_term:
        return []
    
    try:
        return [
            member
            for member in members
            if normalized_term in member["name"].lower()
            or normalized_term in member["github_username"].lower()
        ]
    except (KeyError, AttributeError) as e:
        print(f"Error: Invalid member data structure. Details: {str(e)}")
        return []


def display_member_list(members):
    """Print a numbered list of member dictionaries."""
    if not members:
        print("No team members to display.")
        return

    print("\nTeam Member List:")
    for index, member in enumerate(members, start=1):
        print(f"{index}. {member['name']} ({member['github_username']})")


def get_team_member_count(members):
    """Return the number of team members."""
    return len(members)


def format_greeting(team_name):
    """Return a welcome message for the team."""
    return f"Welcome! This is team {team_name}."


def display_team_summary(team_name, members, github_users):
    """Display team data in a consistent, readable format."""
    print("\nOrganized Team Summary:")
    print(f"Team: {team_name}")
    print("Team Members:")
    for member, github_user in zip(members, github_users):
        print(f"- {member} ({github_user})")


def say_hello(members):
    """Build a greeting message based on user choices."""
    greeting, error = choose_from_list(
        GREETINGS,
        title="Choose a greeting:",
        prompt="Enter the greeting number: ",
        cancelled_message="Greeting selection cancelled.",
        invalid_message="Invalid greeting choice.",
    )
    if error:
        return error

    member, error = choose_from_list(
        members,
        title="Choose the team member to greet:",
        prompt="Enter the member number: ",
        cancelled_message="Team member selection cancelled.",
        invalid_message="Invalid team member choice.",
    )
    if error:
        return error

    return f"{greeting}, {member}!"


def count_name_lengths(members):
    """Display and summarize the length of each team member's name."""
    print("\nNAME LENGTH ANALYZER")
    print("Added by: @sayemeen21-blip")

    total_characters = 0
    for member in members:
        name_length = len(member)
        total_characters += name_length
        print(f" {member}: {name_length} characters")

    average_length = total_characters / len(members)
    print(f" Total characters: {total_characters}")
    print(f" Average name length: {average_length:.1f} characters")
