import numpy as np
import pandas as pd
import json
import heapq
import time
from tqdm import tqdm

# File paths for puzzle data
puzzle_info_path = '/kaggle/input/santa-2023/puzzle_info.csv'
puzzles_path = '/kaggle/input/santa-2023/puzzles.csv'
sample_submission_path = '/kaggle/input/santa-2023/sample_submission.csv'

# Load and parse the puzzle data
puzzle_info_df = pd.read_csv(puzzle_info_path)
puzzles_df = pd.read_csv(puzzles_path)
sample_submission_df = pd.read_csv(sample_submission_path)

# Parsing the allowed moves into a usable format
puzzle_info_df['allowed_moves'] = puzzle_info_df['allowed_moves'].apply(lambda x: json.loads(x.replace("'", '"')))

# Define the function to apply moves to the puzzle state
def apply_move(current_state, move):
    new_state = [current_state[i] for i in move]
    return new_state

# Define the heuristic function for A* search
def heuristic(state, goal_state):
    return sum(s != g for s, g in zip(state, goal_state))

# Define the A* search algorithm
def a_star_search(initial_state, goal_state, allowed_moves, timeout=300):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (0, initial_state, []))
    closed_set = set()

    while open_set:
        if time.time() - start_time > timeout:
            return None

        _, current_state, path = heapq.heappop(open_set)

        if current_state == goal_state:
            return path

        if tuple(current_state) in closed_set:
            continue

        closed_set.add(tuple(current_state))

        for move_name, move in allowed_moves.items():
            new_state = apply_move(current_state, move)
            if tuple(new_state) not in closed_set:
                priority = len(path) + 1 + heuristic(new_state, goal_state)
                heapq.heappush(open_set, (priority, new_state, path + [move_name]))

    return None

# Function to format the solution for submission
def format_solution_for_submission(puzzle_id, solution_moves):
    formatted_moves = ['-' + move if inverse else move for move, inverse in solution_moves]
    return {'id': puzzle_id, 'moves': '.'.join(formatted_moves)}

# Function to solve puzzles
def solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=30):
    solutions = []

    puzzles_to_solve = puzzles_df.head(num_puzzles)

    for index, row in tqdm(puzzles_to_solve.iterrows(), total=puzzles_to_solve.shape[0], desc="Solving Puzzles"):
        puzzle_id = row['id']
        initial_state = row['initial_state']  
        goal_state = row['solution_state']    
        puzzle_type = row['puzzle_type']
        allowed_moves = puzzle_info_df[puzzle_info_df['puzzle_type'] == puzzle_type]['allowed_moves'].iloc[0]

        solution_moves = a_star_search(initial_state, goal_state, allowed_moves)

        if solution_moves is None:
            solution_moves = sample_submission_df[sample_submission_df['id'] == puzzle_id]['moves'].iloc[0].split('.')
            solution_moves = [(move.lstrip('-'), move.startswith('-')) for move in solution_moves]

        formatted_solution = format_solution_for_submission(puzzle_id, solution_moves)
        solutions.append(formatted_solution)

    return pd.DataFrame(solutions)

# Solving the first 30 puzzles in the dataset
solved_puzzles_df = solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=30)
print(solved_puzzles_df)

# Define the file path for the output CSV file
output_csv_path = '/kaggle/working/solution.csv'

# Save the output DataFrame to a CSV file
solved_puzzles_df.to_csv(output_csv_path, index=False)

# Display the path of the saved file (For kaggle else not needed)
print(f"Solution saved to: {output_csv_path}")
