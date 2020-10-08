# AI Puzzle Solver
CS 4033 (001) Homework

## Requirements
* Python 3.8

## How to Run
* Each vector should be formatted as such [1,2,0,...] where 0 represents the empty state. There must **NO** spaces
within the brackets of the vector.
* BFS only supports a 3-column grid at the moment. A* only supports a 6x3 grid.

### Command
    python {search to run} {input vector} {output vector}

## Supported Searches
* BFS (Breadth-First Search) - **bfs.py**
* A* Search (Heuristic = # of mismatches between start and goal state) - **a_star_firsth.py**
* A* Search (Heuristic = sum of smallest # of moves needed for each mismatch to be fixed) - **a_star_secondh.py**