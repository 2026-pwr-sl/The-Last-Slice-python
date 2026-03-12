print("")
team_name = "The Last Slice"
team_members = ["Henrique Esteves", "Ummay Sayemeen", "Vitalii Kozak"]
github_names = ["Henriqu3steves", "sayemeen21-blip", "kozak1715"]

print(f"Team Name: {team_name}")
print("Team Members:")
for n, m in zip(team_members, github_names):
	print(f"- {n} - {m}")
	
print("")
print("Project check: The project runs correctly.")
print("")

print("Custom functions section:")

def get_team_member_count(members):
	return "the number of team members is: " + str(len(members))


def format_greeting(team):
	return f"Welcome! This is team {team}."


def display_data_organized(team, members, github_users):
	"""Display team data in a consistent, readable format."""
	print("\nOrganized Team Summary:")
	print(f"Team: {team}")
	for member, github_user in zip(members, github_users):
		print(f"- {member} ({github_user})")

def say_hello(names):
	words = ["Hello", "Hi", "Hey", "Greetings", "Salutations", "Dzien dobry", "Hola", "Bonjour", "Ciao"]
	print("\nChoose a greeting:")
	for index, word in enumerate(words, start=1):
		print(f"{index}. {word}")

	try:
		greeting_choice = int(input("Enter the greeting number: "))
	except (ValueError, KeyboardInterrupt):
		return "Greeting selection cancelled."

	if greeting_choice < 1 or greeting_choice > len(words):
		return "Invalid greeting choice."

	selected_word = words[greeting_choice - 1]

	print("\nChoose the team member to greet:")
	for index, name in enumerate(names, start=1):
		print(f"{index}. {name}")

	try:
		name_choice = int(input("Enter the member number: "))
	except (ValueError, KeyboardInterrupt):
		return "Team member selection cancelled."

	if name_choice < 1 or name_choice > len(names):
		return "Invalid team member choice."

	selected_name = names[name_choice - 1]

	return f"{selected_word}, {selected_name}!"


print(format_greeting(team_name))
print(f"Total team members: {get_team_member_count(team_members)}")
display_data_organized(team_name, team_members, github_names)
print(say_hello(team_members))

# FUNCTION ADDED BY (@sayemeen21-blip)

def count_name_lengths(members):
    """Count and display the length of each team member's name"""
    print("\n")
    print("NAME LENGTH ANALYZER")
    print("Added by: @sayemeen21-blip")
   
    
    total_chars = 0
    for name in members:
        length = len(name)
        total_chars = total_chars + length
        print(f" {name}: {length} characters")
    
    average = total_chars / len(members)
    print(f" Total characters: {total_chars}")
    print(f" Average name length: {average:.1f} characters")
    
print(count_name_lengths(team_members))
