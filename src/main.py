print("")
team_name = "The Last Slice"
team_members = ["Henrique Esteves", "Ummay Sayemeen", "Vitalii Kozak"]
github_names = ["Henriqu3steves", "sayemeen21-blip", "kozak1715"]

print(f"Team Name: {team_name}")
print("Team Members:")
for n, m in zip(team_members, github_names):
	print(f"- {n} ({m})")

print("")
print("Project check: The project runs correctly.")
print("")