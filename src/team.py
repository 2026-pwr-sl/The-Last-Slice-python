"""Team-related data operations and formatting."""

import csv
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
    """Load team data from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            team_data = json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"Team data file not found: {file_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Team data file is not valid JSON: {error.msg}") from error
    except OSError as error:
        raise ValueError(f"Unable to read team data file: {error}") from error

    if not isinstance(team_data, dict):
        raise ValueError("Team data must be a JSON object.")

    team_name = team_data.get("team_name")
    members = team_data.get("members")

    if not isinstance(team_name, str) or not team_name.strip():
        raise ValueError("Invalid team data: 'team_name' must be a non-empty string.")
    if not isinstance(members, list):
        raise ValueError("Invalid team data: 'members' must be a list.")

    for member in members:
        if not isinstance(member, dict):
            raise ValueError("Invalid team data: each member must be an object.")

        name = member.get("name")
        github_username = member.get("github_username")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid team data: member name must be a non-empty string.")
        if not isinstance(github_username, str) or not github_username.strip():
            raise ValueError(
                "Invalid team data: GitHub username must be a non-empty string."
            )

    return team_data


def save_team_data(file_path, team_data):
    """Persist team data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(team_data, file, indent=2)
    except OSError as error:
        raise ValueError(f"Unable to save team data: {error}") from error


def add_member(members, name, github_username):
    """Add a member dictionary to the list if it does not already exist."""
    if not isinstance(members, list):
        return False, "Invalid members list."
    if not isinstance(name, str) or not name.strip():
        return False, "Name cannot be empty."
    if not isinstance(github_username, str) or not github_username.strip():
        return False, "GitHub username cannot be empty."

    for member in members:
        if not isinstance(member, dict):
            continue

        existing_name = str(member.get("name", "")).strip().lower()
        existing_github = str(member.get("github_username", "")).strip().lower()
        same_name = existing_name == name.strip().lower()
        same_github = (
            existing_github == github_username.strip().lower()
        )
        if same_name or same_github:
            return False, "Member already exists (name or GitHub username)."

    members.append(
        {
            "name": name.strip(),
            "github_username": github_username.strip(),
        }
    )
    return True, "Member added successfully."


def search_member(members, search_term):
    """Return members that match by name or GitHub username."""
    if not isinstance(members, list):
        return []
    if not isinstance(search_term, str) or not search_term.strip():
        return []

    normalized_term = search_term.strip().lower()
    return [
        member
        for member in members
        if isinstance(member, dict)
        and (
            normalized_term in str(member.get("name", "")).lower()
            or normalized_term in str(member.get("github_username", "")).lower()
        )
    ]


def display_member_list(members):
    """Print a numbered list of member dictionaries."""
    if not isinstance(members, list) or not members:
        print("No team members to display.")
        return

    print("\nTeam Member List:")
    for index, member in enumerate(members, start=1):
        name = str(member.get("name", "Unknown")) if isinstance(member, dict) else "Unknown"
        github_username = (
            str(member.get("github_username", "Unknown"))
            if isinstance(member, dict)
            else "Unknown"
        )
        print(f"{index}. {name} ({github_username})")


def get_team_member_count(members):
    """Return the number of team members."""
    if not isinstance(members, list):
        return 0
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

    if not members:
        print(" No members available for analysis.")
        return

    total_characters = 0
    for member in members:
        name_length = len(member)
        total_characters += name_length
        print(f" {member}: {name_length} characters")

    average_length = total_characters / len(members)
    print(f" Total characters: {total_characters}")
    print(f" Average name length: {average_length:.1f} characters")

def export_to_csv(members, filename="team_export.csv"):
    """Export team members to a CSV file."""
    if not isinstance(members, list):
        return False, "Export failed: invalid members list."
    if not isinstance(filename, str) or not filename.strip():
        return False, "Export failed: filename cannot be empty."

    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["name", "github_username"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for member in members:
                writer.writerow({
                    "name": member.get("name", ""),
                    "github_username": member.get("github_username", ""),
                })
        return True, f"Successfully exported {len(members)} members to '{filename}'."
    except OSError as error:
        return False, f"Export failed: {error}"
