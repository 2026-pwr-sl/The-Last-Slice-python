import argparse

from team import (
	count_name_lengths,
	display_team_summary,
	format_greeting,
	get_team_member_count,
	say_hello,
)

TEAM_NAME = "The Last Slice"
TEAM_MEMBERS = ["Henrique Esteves", "Ummay Sayemeen", "Vitalii Kozak"]
GITHUB_USERNAMES = ["Henriqu3steves", "sayemeen21-blip", "kozak1715"]


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
		"--count",
		action="store_true",
		help="Display the total number of team members.",
	)
	parser.add_argument(
		"--greet",
		metavar="NAME",
		help="Print a greeting to the provided name.",
	)
	return parser.parse_args()


def main():
	args = parse_args()

	if args.show_team or args.count or args.greet:
		if args.show_team:
			display_team_summary(TEAM_NAME, TEAM_MEMBERS, GITHUB_USERNAMES)

		if args.count:
			print(get_team_member_count(TEAM_MEMBERS))

		if args.greet:
			print(f"Hello, {args.greet}!")

		return

	print()
	print("Project check: The project runs correctly.")

	print("\nCustom functions section:")
	print(format_greeting(TEAM_NAME))
	print(f"Total team members: {get_team_member_count(TEAM_MEMBERS)}")
	display_team_summary(TEAM_NAME, TEAM_MEMBERS, GITHUB_USERNAMES)
	print(say_hello(TEAM_MEMBERS))
	count_name_lengths(TEAM_MEMBERS)


if __name__ == "__main__":
	main()
