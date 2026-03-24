import argparse
import os

from team import (
    add_member,
    count_name_lengths,
    display_member_list,
    display_team_summary,
    export_to_csv,
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


class SafeArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that raises a friendly ValueError instead of exiting."""

    def error(self, message):
        raise ValueError(message)


def parse_args():
    """Parse command-line options for the CLI script."""
    parser = SafeArgumentParser(
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
    parser.add_argument(
        "--export-csv",
        metavar="FILENAME",
        nargs="?",
        const="team_export.csv",
        help="Export team members to CSV file. Optional filename (default: team_export.csv)",
    )
    return parser.parse_args()


def validate_text_argument(value, flag_name):
    """Validate free-text CLI values and raise clear errors for invalid input."""
    if value is None:
        return

    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{flag_name} requires a non-empty value.")


def main():
    try:
        args = parse_args()

        validate_text_argument(args.greet, "--greet")
        validate_text_argument(args.search_member, "--search-member")

        team_data = load_team_data(DATA_FILE_PATH)
        team_name = team_data["team_name"]
        members = team_data["members"]
        team_members = [member["name"] for member in members]
        github_usernames = [member["github_username"] for member in members]

        if args.export_csv:
            success, message = export_to_csv(members, args.export_csv)
            print(message)
            return 0 if success else 1

        if args.add_member:
            name, github_username = args.add_member
            added, message = add_member(members, name, github_username)
            print(message)
            if added:
                save_team_data(DATA_FILE_PATH, team_data)

        if args.search_member:
            results = search_member(members, args.search_member)
            if results:
                display_member_list(results)
            else:
                print("No matching member found.")

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
                print(get_team_member_count(members))

            if args.greet:
                print(f"Hello, {args.greet}!")

            return 0

        print()
        print("Project check: The project runs correctly.")

        print("\nCustom functions section:")
        print(format_greeting(team_name))
        print(f"Total team members: {get_team_member_count(members)}")
        display_team_summary(team_name, team_members, github_usernames)
        print(say_hello(team_members))
        count_name_lengths(team_members)
        return 0

    except ValueError as error:
        print(f"Error: {error}")
        print("Run with --help to see valid usage.")
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as error:
        print(f"Unexpected error: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())