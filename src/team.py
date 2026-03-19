"""Team-related data operations and formatting."""

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
