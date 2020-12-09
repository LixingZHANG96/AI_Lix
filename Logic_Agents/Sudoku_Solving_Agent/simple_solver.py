from simple_solver_utils import *


# `grid` is defined in the test code scope as the following:
# (note: changing the value here will _not_ change the test code)
# grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    empty_filler = "123456789"
    grid_list = list(grid)
    for i in range(len(grid)):
        if grid[i] == '.':
            grid_list[i] = empty_filler
    sudoku_dict = dict(zip(boxes, grid_list))
    return sudoku_dict


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    values_new = values.copy()
    for key in values.keys():
        for peer in peers[key]:
            peer_val = values[peer]
            if len(peer_val) == 1:
                values_new[key] = values_new[key].replace(peer_val, '')
    return values_new


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    values_new = values.copy()
    for key in peers.keys():
        box_val_set = set(values[key])
        if len(box_val_set) > 1:
            for peer in peers[key]:
                box_val_set -= set(values[peer])
        if len(box_val_set) == 1:
            values_new[key] = ''.join(box_val_set)
    return values_new


def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    values_copy = values.copy()
    for box_A in boxes:
        if len(values[box_A]) != 2: continue  # Only continue checking if the box has 2 values
        for unit in units[box_A]:
            for box_B in unit:
                if len(values[box_B]) != 2 or box_B == box_A: continue
                if values[box_A] == values[box_B]:
                    for value in values[box_A]:
                        for box in unit:
                            if box == box_A or box == box_B: continue
                            values_copy[box] = values_copy[box].replace(value, '')
    return values_copy


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)

        # Use the Only Choice Strategy
        values = only_choice(values)

        # Use the Only Choice Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


if __name__ == "__main__":
    grid = input("Please input the sudoku as a formatted String of length 81:\n")
    if len(grid) < 81:
        print("Invalid input, use internal grid instead!")
        grid = default_grid
    sudoku_dict = grid_values(grid)
    print("The original sudoku: ")
    display(sudoku_dict)
    sudoku_dict = search(sudoku_dict)
    print("The solved sudoku: ")
    display(sudoku_dict)
