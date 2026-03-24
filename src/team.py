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
    """Load team data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_team_data(file_path, team_data):
    """Persist team data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(team_data, file, indent=2)


def add_member(members, name, github_username):
    """Add a member dictionary to the list if it does not already exist."""
    for member in members:
        same_name = member["name"].strip().lower() == name.strip().lower()
        same_github = (
            member["github_username"].strip().lower()
            == github_username.strip().lower()
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
    normalized_term = search_term.strip().lower()
    return [
        member
        for member in members
        if normalized_term in member["name"].lower()
        or normalized_term in member["github_username"].lower()
    ]


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
