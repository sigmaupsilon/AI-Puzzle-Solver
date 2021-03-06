# AI Assignments 
CS 4033 (001) Homework

## Requirements
* Python 3.8
* Excel data with "X", "Y", and "Class" columns in same directory as script for *Decision Tree* and *Neural Networks*

## Puzzle Solver

### How to Run
* Each vector should be formatted as such [1,2,0,...] where 0 represents the empty state. There must **NO** spaces
within the brackets of the vector.
* BFS only supports a 3-column grid at the moment. A* only supports a 6x3 grid.

#### Command
    python {search to run} {input vector} {output vector}

### Supported Searches
* BFS (Breadth-First Search) - **bfs.py**
* A* Search (Heuristic = # of mismatches between start and goal state) - **a_star_firsth.py**
* A* Search (Heuristic = sum of smallest # of moves needed for each mismatch to be fixed) - **a_star_secondh.py**

## Cryptarithmetic CSP

### How to Run
Constraint support for 3 problems:

<ol type="a">
    <li>SINCE + JULIUS = CAESAR</li>
    <li>CHECK + THE = TIRES</li>
    <li>DO + YOU + FEEL = LUCKY</li>
</ol>

#### Command
    python main.py {a|b|c}

## Decision Trees

### How to Run
    python main.py

## Neural Networks

### How to Run
    python main.py
