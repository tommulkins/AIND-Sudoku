rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]
    pass

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    naked_twins_boxes = {}
    # Find all instances of naked twins
    for box, value in values.items():
        if len(value) == 2:
            for peer in peers[box]:
                if peer not in naked_twins_boxes and value == values[peer]:
                    naked_twins_boxes[peer] = value

    # Eliminate the naked twins as possibilities for their peers
    for box, value in naked_twins_boxes.items():
        for digit in value:
            for peer in peers[box]:
                if peer not in naked_twins_boxes and digit in values[peer] and len(values[peer]) > 1:
                    values[peer] = values[peer].replace(digit,'')
                    assign_value(values, peer, values[peer])

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # grid for the unsolved soduku string
    # Create our dict
    grid_dict = {}
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    # Replace any '.' with '123456789' and return our new dict
    for index, c in enumerate(boxes):
        if grid[index] is '.':
            grid_dict[c] = '123456789'
        else:
            grid_dict[c] = grid[index]

    return grid_dict
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    pass

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            assign_value(values, peer, values[peer])
    return values
    pass

def only_choice(values):
    new_values = values.copy()  # note: do not modify original values
    # Solution from Udacity example.  My example was unable to give same output due to the unordered nature of dicts.
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                new_values[dplaces[0]] = digit
                assign_value(new_values, dplaces[0], digit)
    return new_values
    pass

def reduce_puzzle(values):
    stalled = False # set stalled flag to false
    while not stalled:
        # Check how many boxes have one digit
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values) # First pass through eliminate strategy
        #values = naked_twins(values) # Next attempt naked twins strategy
        values = only_choice(values) # Next attempt only_choice strategy
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    #End of while loop
    return values
    pass

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False #Failed at reduce_puzzle
    if all(len(values[s]) == 1 for s in boxes):
        return values #Solved
    # Choose one of the unfilled squares with the fewest possibilities
    min_box_dict = min((len(v), k) for k, v in values.items() if len(v) > 1)
    min_box = min_box_dict[1]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[min_box]:
        new_sudoku = values.copy()
        new_sudoku[min_box] = value
        soduku_solved = search(new_sudoku)
        if soduku_solved:
            return soduku_solved
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    before_naked_twins_1 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
                            'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
                            'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
                            'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
                            'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
                            'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
                            'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
                            'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
                            'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
                            'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
                            'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

    print('Before')
    display(before_naked_twins_1)
    print('After')
    display(naked_twins(before_naked_twins_1))

    #display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        #visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
