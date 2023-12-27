# Santa-2023---The-Polytope-Permutation-Puzzle

Santa 2023 using A* search!!
This Python script is designed to solve a set of puzzles as part of a Kaggle competition. It involves loading puzzle data, applying an A* search algorithm to find solutions, and saving these solutions in a format suitable for submission. This method takes too much time to find solution. 

Overview of Steps
Import Libraries
Define File Paths
Load and Parse Data
Define Helper Functions
Solve Puzzles
Save Solutions
1. Import Libraries
The script begins by importing necessary Python libraries:

numpy and pandas for data manipulation.
json for parsing JSON data.
heapq for implementing priority queues, essential for the A* search algorithm.
time for tracking the execution time of the search algorithm.
tqdm for displaying progress bars during puzzle solving.


2. Define File Paths
Paths to the puzzle data files are defined:

puzzle_info_path: Path to the file containing information about puzzle types and allowed moves.
puzzles_path: Path to the file with individual puzzle data.
sample_submission_path: Path to the sample submission file.


3. Load and Parse Data
Puzzle data is loaded from CSV files using pandas:

puzzle_info_df: DataFrame containing types of puzzles and their allowed moves.
puzzles_df: DataFrame containing specific puzzles to be solved.
sample_submission_df: DataFrame with sample submission format.
The allowed moves are parsed into a usable format using json.loads.

4. Define Helper Functions
Several functions are defined to assist in solving the puzzles:

apply_move: Applies a given move to a puzzle state.
heuristic: Estimates the cost from the current state to the goal state, used in the A* algorithm.
a_star_search: Implements the A* search algorithm to find a solution path.
format_solution_for_submission: Formats the solution into a string suitable for submission.
solve_puzzles: Solves a specified number of puzzles using the A* search algorithm.


5. Solve Puzzles
The solve_puzzles function is called to solve the first 30 puzzles. It iterates through each puzzle, applies the A* search algorithm, and formats the solution.

6. Save Solutions
The solutions are saved to a CSV file (solution.csv) in the Kaggle working directory. The path to the saved file is printed.

Usage
To use this script, ensure that the puzzle data files are located at the specified paths. Run the script in an environment where the necessary libraries are installed. The script will automatically load the data, solve the puzzles, and save the solutions to a CSV file.
