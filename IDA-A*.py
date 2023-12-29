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

# Define the IDA - A* search algorithm
def ida_star_search(initial_state, goal_state, allowed_moves, timeout=300):
    def search(path, g, threshold):
        node = path[-1]
        f = g + heuristic(node, goal_state)
        if f > threshold:
            return f
        if node == goal_state:
            return 'FOUND'
        min_threshold = float('inf')
        for move_name, move in allowed_moves.items():
            new_state = apply_move(node, move)
            if new_state not in path:
                path.append(new_state)
                temp = search(path, g + 1, threshold)
                if temp == 'FOUND':
                    return 'FOUND'
                if temp < min_threshold:
                    min_threshold = temp
                path.pop()
        return min_threshold

    start_time = time.time()
    threshold = heuristic(initial_state, goal_state)
    path = [initial_state]
    while time.time() - start_time < timeout:
        temp = search(path, 0, threshold)
        if temp == 'FOUND':
            return [move for _, move in path[1:]]
        elif temp == float('inf'):
            return None
        threshold = temp
    return None

# Function to format the solution for submission
def format_solution_for_submission(puzzle_id, solution_moves):
    formatted_moves = ['-' + move if inverse else move for move, inverse in solution_moves]
    return {'id': puzzle_id, 'moves': '.'.join(formatted_moves)}

# Function to solve puzzles
def solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df):
    solutions = []

    for index, row in tqdm(puzzles_df.iterrows(), total=puzzles_df.shape[0], desc="Solving Puzzles"):
        puzzle_id = row['id']
        initial_state = row['initial_state']  
        goal_state = row['solution_state']    
        puzzle_type = row['puzzle_type']
        allowed_moves = puzzle_info_df[puzzle_info_df['puzzle_type'] == puzzle_type]['allowed_moves'].iloc[0]

        solution_moves = ida_star_search(initial_state, goal_state, allowed_moves)

        if solution_moves is None:
            solution_moves = sample_submission_df[sample_submission_df['id'] == puzzle_id]['moves'].iloc[0].split('.')
            solution_moves = [(move.lstrip('-'), move.startswith('-')) for move in solution_moves]

        formatted_solution = format_solution_for_submission(puzzle_id, solution_moves)
        solutions.append(formatted_solution)

    return pd.DataFrame(solutions)

# Solving all puzzles in the dataset
solved_puzzles_df = solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df)
print(solved_puzzles_df)

# Solving the first 30 puzzles in the dataset
solved_puzzles_df = solve_puzzles(puzzles_df, puzzle_info_df, sample_submission_df, num_puzzles=10)
print(solved_puzzles_df)

# Define the file path for the output CSV file
output_csv_path = '/kaggle/working/solution.csv'

# Save the output DataFrame to a CSV file
solved_puzzles_df.to_csv(output_csv_path, index=False)

# Display the path of the saved file
print(f"Solution saved to: {output_csv_path}")
