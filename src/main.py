import argparse
import os

from team import (
    add_member,
    count_name_lengths,
    display_member_list,
    display_team_summary,
    format_greeting,
    get_team_member_count,
    load_team_data,
    say_hello,
    save_team_data,
    search_member,
)

DATA_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "team_data.json")
)


def parse_args():
    """Parse command-line options for the CLI script."""
    parser = argparse.ArgumentParser(
        description="Team utility CLI for The Last Slice.",
    )
    parser.add_argument(
        "--show-team",
        action="store_true",
        help="Display all team members and GitHub usernames.",
    )
    parser.add_argument(
        "--display-list",
        action="store_true",
        help="Display the current team member list.",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Display the total number of team members.",
    )
    parser.add_argument(
        "--add-member",
        nargs=2,
        metavar=("NAME", "GITHUB_USERNAME"),
        help="Add a new member with name and GitHub username.",
    )
    parser.add_argument(
        "--search-member",
        metavar="QUERY",
        help="Search for a member by name or GitHub username.",
    )
    parser.add_argument(
        "--greet",
        metavar="NAME",
        help="Print a greeting to the provided name.",
    )
    return parser.parse_args()


def main():
    """Main entry point for the CLI application."""
    try:
        args = parse_args()
    except SystemExit:
        # argparse calls sys.exit() on error, which is expected behavior
        return
    
    # Load team data with error handling
    team_data, load_error = load_team_data(DATA_FILE_PATH)
    if team_data is None:
        print(load_error)
        return
    
    try:
        team_name = team_data["team_name"]
        members = team_data["members"]
        team_members = [member["name"] for member in members]
        github_usernames = [member["github_username"] for member in members]
    except (KeyError, TypeError, AttributeError) as e:
        print(f"Error: Unable to process team data. Details: {str(e)}")
        return

    if args.add_member:
        try:
            name, github_username = args.add_member
            added, message = add_member(members, name, github_username)
            print(message)
            if added:
                success, save_message = save_team_data(DATA_FILE_PATH, team_data)
                if not success:
                    print(save_message)
        except Exception as e:
            print(f"Error: Failed to add member. Details: {str(e)}")

    if args.search_member:
        try:
            results = search_member(members, args.search_member)
            if results:
                display_member_list(results)
            else:
                if args.search_member.strip():
                    print("No matching member found.")
                else:
                    print("Error: Search term cannot be empty.")
        except Exception as e:
            print(f"Error: Search failed. Details: {str(e)}")

    if (
        args.show_team
        or args.display_list
        or args.count
        or args.greet
        or args.add_member
        or args.search_member
    ):
        try:
            if args.show_team:
                display_team_summary(team_name, team_members, github_usernames)

            if args.display_list:
                display_member_list(members)

            if args.count:
                print(get_team_member_count(members))

            if args.greet:
                if not args.greet.strip():
                    print("Error: Name cannot be empty.")
                else:
                    print(f"Hello, {args.greet}!")
        except Exception as e:
            print(f"Error: Failed to execute command. Details: {str(e)}")
        return

    # Default behavior
    try:
        print()
        print("Project check: The project runs correctly.")

        print("\nCustom functions section:")
        print(format_greeting(team_name))
        print(f"Total team members: {get_team_member_count(members)}")
        display_team_summary(team_name, team_members, github_usernames)
        print(say_hello(team_members))
        count_name_lengths(team_members)
    except Exception as e:
        print(f"Error: An unexpected error occurred. Details: {str(e)}")


if __name__ == "__main__":
    main()
