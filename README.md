# The-Last-Slice-python


## Group Information
- Group Name: **The Last Slice**

## Team Members
- sayemeen21-blip
- kozak1715
- Henriqu3steves

## Project Description
This is our first team programming project. The goal is to create a simple Python program that displays our team information and demonstrates basic Python functions while learning how to collaborate using GitHub.

"Three developers, one repository, countless lessons in collaboration."

## Prerequisites
    Python 3.x installed (Download Python)
    Git installed (Download Git)
    GitHub account


## Steps to Run:

1. **Clone the repository**
   ```bash
   git clone https://github.com/2026-pwr-sl/The-Last-Slice-python.git
   cd The-Last-Slice-python
   ````
2. **Run the program**
   ```bash
   python src\main.py
   ````
3. **Test**
   ```bash
   python tests/run_all_tests.py
   ````

   
## Lab02 - Standard Input and Output

### Logging Library Documentation

- [Logging Library Documentation](https://docs.python.org/3/library/logging.html)
- [Logging Tutorial](https://docs.python.org/3/howto/logging.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

### Python Documentation for Lab02.py

- [str.split()](https://docs.python.org/3/library/stdtypes.html#str.split)
- [ipaddress module](https://docs.python.org/3/library/ipaddress.html)
- [ipaddress.IPv4Address](https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address)
- [ipaddress.IPv4Network](https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network)
- [datetime module and datetime class](https://docs.python.org/3/library/datetime.html)

### How to Run

```bash
python lab2.py < log.txt
````


## Lab07 - Regular Expressions

### pycodestyle output
    No errors or warnings found.



## Team Contributions(Lab01):
### Henrique Esteves (@Henriqu3steves)
Responsibilities: Wrote the first Python program and created 3 custom functions including the interactive greeting function, and performed tests.

Problems Encountered: Faced challenges with the logic of the greeting function as it was more complex than expected, requiring careful handling of user input and error cases

What I Learned: Discovered that GitHub has more dimensions and uses than I previously knew, proving itself as an even more capable tool and accelerator of teamwork. Python showed itself as a simple language to understand and manage, being very good for data manipulation and management.


### Ummay Sayemeen (@sayemeen21-blip)
Responsibilities: Set up the repository structure, added team members, created .gitignore file, created initial README, added count_name_lengths function to analyze team member names, and updated README with team contributions summary.

Problems Encountered: Faced Python installation issues blocked by system policy, resolved merge conflicts manually, accidentally merged own PR without review (learned to never do that!), and had to navigate duplicate folder structures.

What I Learned: Mastered Git commands (branching, committing, pushing, fetching), learned to resolve merge conflicts, understood the importance of code reviews, and discovered that collaboration makes code better.


### Vitalii Kozak (@kozak1715)
Responsibilities: Divided the work using GitHub Issues, implemented three basic sorting functions (bubble sort, selection sort, insertion sort) in src/sorting_functions.py, and prepared unit tests to verify their behavior

Problems Encountered: Had to pull main.py from the main branch into my feature branch to test the functions properly, and learned to stage, commit, and push changes correctly so they appear on GitHub

What I Learned: Learned to work effectively with branches, create and test Python functions (including basic sorting algorithms), perform unit testing using assert statements, and use GitHub for commits, pushes, and Pull Requests.





## Paper10_lab08 Task 0 

**FIDE World Chess Ratings 201K Players**

Dataset URL:
```bash
https://www.kaggle.com/datasets/ibrahimqasimi/fide-world-chess-ratings-201k-players
````

Description:
Complete monthly rating list from FIDE (Fédération Internationale des Échecs), the international chess governing body. Contains 201,016 active rated players from 204 countries including world champion Magnus Carlsen, Hikaru Nakamura, Gukesh Dommaraju, and every grandmaster, FIDE master, and rated amateur on Earth. This is the August 2025 list, capturing the post-Carlsen world champion era.

Columns:
```bash
id — Unique FIDE player ID
name — Player full name
fed — Federation / country (3-letter code)
sex — M or F
title — Highest standard title (GM, IM, FM, CM)
wtitle — Women's title (WGM, WIM, WFM, WCM)
otitle / foa — Other / online titles
rating — Standard Elo rating
games — Number of rated games played
k — K-factor (rating volatility)
bday — Birth year
````

Key Stats:
```bash
Total players: 201,016
Countries: 204
Rating range: 1,400 to 2,839
Snapshot: August 2025 rating list
````

## Paper10_lab08 Task 4

### Environment Variables

The application uses the following environment variables:

#### COUNTRY

Three-letter federation code used to filter players.

Examples:
- POL
- USA
- IND

#### MIN_RATING

Minimum rating of players included in the statistical analysis.

Examples:
- 1800
- 2000
- 2500

The statistical operation "average rating" is calculated only for players satisfying both conditions.


### Thank you for visiting our project! 
Created by Team "The Last Slice"
