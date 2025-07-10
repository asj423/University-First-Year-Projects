def sudoku_solver(sudoku):
    
    # Initialise arrays that store each cells possible values and the length of those possible values.
    possible_value_board = [[[] for _ in range(9)] for _ in range(9)]
    length_board = [[10 for _ in range(9)] for _ in range(9)]
    lowest_len = 10

    # Validate the starting board
    for a in range(9):
        for b in range(9):
            if sudoku[a][b] != 0:
                # Check row
                for c in range(9):
                    if c != b and sudoku[a][c] == sudoku[a][b]:
                        return np.full((9, 9), -1)
                # Check column
                for d in range(9):
                    if d != a and sudoku[d][b] == sudoku[a][b]:
                        return np.full((9, 9), -1)
                # Check 3x3 subgrid
                start_row = 3 * (a // 3)
                start_column = 3 * (b // 3)
                for e in range(start_row, start_row + 3):
                    for f in range(start_column, start_column + 3):
                        if (e != a or f !=  b) and sudoku[e][f] == sudoku[a][b]:
                            return np.full((9, 9), -1)

    # Main solving loop
    for a in range(9):
        for b in range(9):
            if sudoku[a][b] == 0:
                possible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

                # Check row and remove the values from the current cells possible values
                for c in range(9):
                    if sudoku[a][c] in possible_values:
                        possible_values.remove(sudoku[a][c])

                # Check column and remove the values from the current cells possible values
                for d in range(9):
                    if sudoku[d][b] in possible_values:
                        possible_values.remove(sudoku[d][b])

                # Check 3x3 subgrid and remove the values from the current cells possible values
                start_row = 3 * (a // 3)
                start_column = 3 * (b // 3)
                for e in range(start_row, start_row + 3):
                    for f in range(start_column, start_column + 3):
                        if sudoku[e][f] in possible_values:
                            possible_values.remove(sudoku[e][f])

                # If only one possible value exists fill in that cell
                if len(possible_values) == 1:
                    sudoku[a][b] = possible_values[0]
                    return sudoku_solver(np.copy(sudoku))

                # Update possible value and length arrays
                possible_value_board[a][b] = possible_values
                length_board[a][b] = len(possible_values)

    # Find the cell with the fewest possible values
    updated = False
    for row in range(9):
        for column in range(9):
            if sudoku[row][column] == 0 and length_board[row][column] < lowest_len:
                lowest_len = length_board[row][column]
                x = row
                y = column
                updated = True

    # If a cell with possibilities was found, attempt solving recursively
    if updated:
        for trial_number in possible_value_board[x][y]:
            sudoku[x][y] = trial_number
            solved_sudoku = sudoku_solver(np.copy(sudoku))
            if np.all(solved_sudoku != -1):
                return solved_sudoku
            sudoku[x][y] = 0  # Backtrack

        # If no solution is found, return failure state
        return np.full((9, 9), -1)

    # Check if the puzzle is fully solved
    if np.all(sudoku != 0):
        return sudoku
    else:
        return np.full((9, 9), -1)