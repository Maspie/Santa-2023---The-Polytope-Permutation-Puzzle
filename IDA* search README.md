Iterative Deepening A* (IDA*) Algorithm

Introduction
The Iterative Deepening A (IDA)** algorithm is an advanced search algorithm used in computer science, particularly in the field of Artificial Intelligence for pathfinding and graph traversing problems. It combines the strengths of two powerful algorithms: the A search algorithm* and Iterative Deepening Depth-First Search (IDDFS).

Why IDA*?
Space Efficiency:

IDA* significantly reduces memory usage compared to traditional A*. While A* stores all generated nodes, IDA* only needs to store a single path from the root node to a leaf node along with some auxiliary data for siblings of these nodes. This makes it especially advantageous in problems with a vast search space.
Optimality and Completeness:

Like A*, IDA* is both optimal and complete, assuming the heuristic function is admissible (never overestimates the true cost to reach the goal). This means IDA* will always find the best solution if one exists.
Adaptability to Varying Problem Sizes:

IDA* is particularly effective in situations where the depth of the solution is not known in advance. It can handle varying problem sizes and complexities adaptively.
Balancing Depth-First and Best-First Search:

IDA* leverages the depth-first search's space efficiency while utilizing the heuristic-driven and performance-oriented nature of the best-first search (A*). This balance allows for exploring more complex and deeper search trees with limited memory.
