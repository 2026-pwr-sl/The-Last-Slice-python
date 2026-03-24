import argparse
import json
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
    try:
        args = parse_args()
        
        # Load team data with error handling
        try:
            team_data = load_team_data(DATA_FILE_PATH)
        except FileNotFoundError as e:
            print(f"\n{str(e)}\nPlease ensure the data file exists at: {DATA_FILE_PATH}")
            return
        except (IOError, ValueError) as e:
            print(f"\n{str(e)}\nUnable to load team data. Please check the file format.")
            return
        except json.JSONDecodeError as e:
            print(f"\n{str(e)}\nThe data file contains invalid JSON. Please fix the file format.")
            return
        
        # Validate team data structure
        if not isinstance(team_data, dict) or "team_name" not in team_data or "members" not in team_data:
            print("\nError: Invalid team data structure. Expected 'team_name' and 'members' fields.")
            return
        
        team_name = team_data["team_name"]
        members = team_data["members"]
        
        if not isinstance(members, list):
            print("\nError: 'members' must be a list.")
            return
        
        team_members = [member.get("name", "Unknown") for member in members if isinstance(member, dict)]
        github_usernames = [member.get("github_username", "Unknown") for member in members if isinstance(member, dict)]
        
        # Handle individual commands
        if args.add_member:
            name, github_username = args.add_member
            added, message = add_member(members, name, github_username)
            print(message)
            if added:
                try:
                    save_team_data(DATA_FILE_PATH, team_data)
                except (IOError, TypeError) as e:
                    print(f"Warning: Member was added but could not save: {str(e)}")

        if args.search_member:
            results = search_member(members, args.search_member)
            if results:
                display_member_list(results)
            else:
                print("\nNo matching member found.")

        if (
            args.show_team
            or args.display_list
            or args.count
            or args.greet
            or args.add_member
            or args.search_member
        ):
            if args.show_team:
                display_team_summary(team_name, team_members, github_usernames)

            if args.display_list:
                display_member_list(members)

            if args.count:
                member_count = get_team_member_count(members)
                print(f"Total team members: {member_count}")

            if args.greet:
                if args.greet.strip():
                    print(f"Hello, {args.greet}!")
                else:
                    print("Error: Greeting name cannot be empty.")

            return

        print()
        print("Project check: The project runs correctly.")

        print("\nCustom functions section:")
        print(format_greeting(team_name))
        print(f"Total team members: {get_team_member_count(members)}")
        display_team_summary(team_name, team_members, github_usernames)
        
        try:
            greeting_result = say_hello(team_members)
            print(greeting_result)
        except Exception as e:
            print(f"Error during greeting selection: {str(e)}")
        
        try:
            count_name_lengths(team_members)
        except Exception as e:
            print(f"Error calculating name statistics: {str(e)}")
    
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        print("Please check your input and try again.")


if __name__ == "__main__":
    main()
