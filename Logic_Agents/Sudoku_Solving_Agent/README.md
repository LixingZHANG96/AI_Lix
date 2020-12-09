# AI Sudoku Solver

## I. Project Overview
Sudoku is a game of strict logic, and thus a perfect platform for testing.
There are 2 ways of solving the sudoku using logical agents:
1. Recursively apply certain logic rules until a feasible solution appears.
This is effective for a problem as simple as sudoku, but would not be capable enough in real-life problems.
2. Using logic propagation rules, propagate the original data into a solution. This is most commonly used in real-life applications.

In this folder, only the first has been implemented, correspondingly, the "simple solver".

## II. Code Structure
### 1. The simple solver
- The **simple_solver_utils.py** provides all necessary functions for pre- and post- processing of sudoku data.
- The **simple_solver.py** implements different logic rules and solve the sudoku problem. Rules used include:
  1. the **elimination** rule, let all other peers in a unit not having a solved value.
  2. the **single_value** rule. If a value is possible for only one box inside a unit, assign it.
  3. the **naked_twins** rule. Details: [Naked Twins for Sudoku](http://www.sudokudragon.com/guidenakedtwins.htm)

## III. Usage
### 1. The simple solver
Simply run the **simple_solver.py** and input a sudoku string or simply use the default sudoku.