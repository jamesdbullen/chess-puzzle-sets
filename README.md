# chess-puzzle-sets
Creating custom chess puzzle sets using the Lichess Puzzles Database.

# Background.

I wanted a set of easy puzzles to use as a warm up for online games. Lichess is an open-source chess platform where you can play puzzles sorted by rating and theme, but I wanted more granular control over the puzzle themes/rating.

Lichess maintains a large database of puzzles and I am learning to code so thought it would be a good project to build my own custom puzzle set from that database.

Disclaimer: I used ChatGPT to help me write the script because I mostly work in R (but the R chess packages aren’t as good, so Python is used here).

# Data.

To run the code, you will need to download the Lichess Puzzles Database available here: https://database.lichess.org/#puzzles.

As described on the website, this database includes more than three million puzzles in a CSV format with fields for FEN, moves (in UCI format), puzzle rating and popularity, puzzle themes and the URL of the game the puzzle comes from.

# Outline.*

The script allows you to filter based on desirable characteristics (e.g. you may want to specify a theme/themes you want the puzzle to contain, a rating range or other criteria). This means that you could, if you wanted, create a puzzle set of entirely mate-in-one puzzles or puzzles with an endgame theme.

Once you have the subset of puzzles you desire, it will turn each puzzle's FEN into a PGN format using Python's chess package.

We can then write each puzzle into a single PGN for use in a PGN reader/chess program.

