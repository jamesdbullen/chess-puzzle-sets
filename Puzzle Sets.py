# Import libraries.

import chess
import pandas as pd
import os

# Load data.

path = r"C:\Insert\Your\Path\Here"

files = os.listdir(path)
print(files)

df = pd.read_csv(os.path.join(path, "lichess_db_puzzle.csv"))

# Subset puzzles based on what we want.

puzzles_subset = df[
    (df['Rating'] < 1300) &
    (~df['Themes'].str.contains("endgame")) &
    (df['GameUrl'].str.contains("black")) &
    (df['NbPlays'] > 10000) &
    (df['Popularity'] > 90) &
    (df['Popularity'] < 95)
].sample(n = 1000)

# Select relevant columns.

puzzles_subset = puzzles_subset.iloc[:, [1, 2, 8]]

# Split into a list of strings.

puzzles_subset['Moves'] = puzzles_subset['Moves'].str.split()

# Function to process each row.

def process_row(fen, moves):
    board = chess.Board(fen)
    fen_parts = fen.split(" ")
    move_number = int(fen_parts[-1])
    san_moves_with_numbers = []

    for uci_move in moves:
        move = chess.Move.from_uci(uci_move)
        if move in board.legal_moves:
            if board.turn == chess.WHITE:
                san_moves_with_numbers.append(f"{move_number}. {board.san(move)}")
            else:
                san_moves_with_numbers.append(board.san(move))
                move_number += 1
            board.push(move)
        else:
            san_moves_with_numbers.append(f"Illegal move: {uci_move}")

    return " ".join(san_moves_with_numbers)

# Apply the function to each row of data.

puzzles_subset['Processed_Moves'] = puzzles_subset.apply(lambda row: process_row(row['FEN'], row['Moves']), axis=1)

# Apply first move to FEN and generate new FEN (because puzzle begins after first move). 

def process_row(fen, moves):
    board = chess.Board(fen)
    fen_parts = fen.split(" ")
    move_number = int(fen_parts[-1])
    san_moves_with_numbers = []

    if moves:
        first_move = chess.Move.from_uci(moves[0])
        if first_move in board.legal_moves:
            board.push(first_move)
            new_fen = board.fen()
            remaining_moves = moves[1:]
        else:
            return fen, "Illegal first move: " + moves[0]

        for uci_move in remaining_moves:
            move = chess.Move.from_uci(uci_move)
            if move in board.legal_moves:
                if board.turn == chess.WHITE:
                    san_moves_with_numbers.append(f"{move_number}. {board.san(move)}")
                else:
                    san_moves_with_numbers.append(board.san(move))
                    move_number += 1
                board.push(move)
            else:
                san_moves_with_numbers.append(f"Illegal move: {uci_move}")

    else:
        new_fen = fen

    processed_moves = " ".join(san_moves_with_numbers)
    return new_fen, processed_moves

# Apply the function to each row of data.

puzzles_subset[['New_FEN', 'Processed_Moves']] = puzzles_subset.apply(lambda row: process_row(row['FEN'], row['Moves']), axis=1, result_type='expand')

# Add new PGN output.

def format_pgn(counter, new_fen, processed_moves):
    return '[Event "Warm-Up Puzzle Set"]\n[White "{}"]\n[Black "Opponent"]\n[Variant "From Position"]\n[FEN "{}"]\n{}'.format(counter, new_fen, processed_moves)

puzzles_subset['PGN'] = [format_pgn(i + 1, row.New_FEN, row.Processed_Moves) for i, row in enumerate(puzzles_subset.itertuples())]

puzzles_subset = puzzles_subset[['FEN', 'Moves', 'New_FEN', 'Processed_Moves', 'PGN']]

# Write PGN file.

pgn_filename = path + " Warm Up Puzzles.pgn"

with open(pgn_filename, "w") as file:
    for pgn in puzzles_subset['PGN']:
        file.write(pgn + "\n\n")