import sys
import os
from dotenv import load_dotenv
import csv

# Task 1
def validate_arguments():
    dataset_file = sys.argv[1]

    # Check file extension
    if not dataset_file.lower().endswith(".csv"):
        print("Error: file must have .csv extension.")
        sys.exit(1)

    # Check if file exists
    if not os.path.isfile(dataset_file):
        print(f"Error: file '{dataset_file}' does not exist.")
        sys.exit(1)

    return dataset_file

# Task 2
def read_dataset(filename):
    players = []

    with open(filename, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            players.append(row)

    return players

# Task 3
def average_rating(players):
    total_rating = 0

    for player in players:
        total_rating += int(player["rating"])

    return total_rating / len(players)

def players_by_country(players):
    countries = {}

    for player in players:
        country = player["fed"]

        if country not in countries:
            countries[country] = 0

        countries[country] += 1

    return countries

def total_players(players):
    return len(players)

# Task 4
def average_rating_parameters(players, country, min_rating):
    total_rating = 0
    count = 0

    for player in players:

        if player["fed"] == country and int(player["rating"]) >= min_rating:
            total_rating += int(player["rating"])
            count += 1

    if count == 0:
        return 0

    return total_rating / count

# Task 5
def parse_arguments():
    output_file = None
    if len(sys.argv) >= 4 and sys.argv[2] == "-o":
        output_file = sys.argv[3]

    return output_file

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

def save_to_excel(avg, total, by_country, avg_parameters, country, min_rating, filename):
    wb = Workbook()

    ws = wb.active
    ws.title = "Summary"

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")

    ws["A1"] = "Metric"
    ws["B1"] = "Value"

    ws["A1"].font = header_font
    ws["B1"].font = header_font
    ws["A1"].fill = header_fill
    ws["B1"].fill = header_fill

    ws.append(["Average Rating (all)", avg])
    ws.append(["Total Players", total])
    ws.append([f"Filtered Average Rating ({country}, min {min_rating})", avg_parameters])

    sorted_countries = sorted(by_country.items(), key=lambda x: x[1], reverse=True)

    ws2 = wb.create_sheet("By Country")
    ws2.append(["Country", "Players"])

    for c, v in sorted_countries:
        ws2.append([c, v])

    wb.save(filename)

    print(f"Excel report saved to {filename}")

# Task 6
def help_flag():
    help_flag = False

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-h":
            help_flag = True

    return help_flag

def print_help():
    print("""
USAGE:
    python paper10_lab08.py <dataset.csv> [-o <file.xlsx>] [-h]

ARGUMENTS:
    dataset.csv
        Path to the CSV dataset file (required)

OPTIONS:
    -o <file.xlsx>
        Save results into an Excel file

    -h
        Show this help message

EXAMPLES:
    python paper10_lab08.py data/dataset.csv
    python paper10_lab08.py data/dataset.csv -o report.xlsx
""")

def main():
    # Task 1
    dataset_file = validate_arguments()
    print(f"Dataset file: {dataset_file}")
    print("File validation successful.")

    # Task 6
    if help_flag():
        print_help()
        sys.exit(0)

    # Task 2
    players = read_dataset(dataset_file)

    # Task 3
    avg = average_rating(players)
    by_country = players_by_country(players)
    total = total_players(players)   

    # Task 4
    load_dotenv()
    country = os.getenv("COUNTRY")
    min_rating = int(os.getenv("MIN_RATING"))
    avg_parameters = average_rating_parameters(players, country, min_rating)

    # Task 5
    output_file = parse_arguments()
    if output_file:
        save_to_excel(avg, total, by_country, avg_parameters, country, min_rating, output_file)
    else:
        print(f"Average rating: {avg:.2f}")
        print("Top countries:", list(by_country.items())[:5])
        print(f"Total players: {total}")  
        print(f"Country: {country}, minimum rating: {min_rating}, average rating: {avg_parameters:.2f}")
      
if __name__ == "__main__":
    main()