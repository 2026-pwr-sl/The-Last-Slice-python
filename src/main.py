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


def main():

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
