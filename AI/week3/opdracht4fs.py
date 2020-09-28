
"""
ABCDEF
001100 1
110000 2
010100 3
001001 4
100000 5
000110 6
select col E, handle row 6, 6 in partial solution: [6]
cover row 6 and rows that overlap row 6: 1, 3
cover columns that have 1 in row 6: D, E

New matrix:
ABCDEF
...... 1
110..0 2
...... 3
001..1 4
100..0 5
...... 6
Select col C, handle row 4, 4 in parial solution: [6, 4]
cover row 4 and rows that overlap row 4: none
cover columns that have 1 in row 4: C, F

New matrix:
ABCDEF
...... 1
11.... 2
...... 3
...... 4
10.... 5
...... 6
Select col B, handle row 2, 2 in partial solution: [6, 4, 2]
cover row 2 and rows that overlap row 2: 5
cover columns that have 1 in row 2:, A, B

New matrix:
ABCDEF
...... 1
...... 2
...... 3
...... 4
...... 5
...... 6
Solution found: [6, 4, 2]

"""

def active_cols(col_active):
    return [i for i in range(cols) if col_active[i]]

def active_rows(row_active):
    return [i for i in range(rows) if row_active[i]]

def print_matrix(row_active, col_active):
    for row in range(rows):
        for col in range(cols):
            if row_active[row] and col_active[col]:
                print(matrix[row][col], end="")
            else:
                print(".", end="")
        print("")

# gets the column with the lowest amount of 1's, returns (col, amount)
# (this to check for case where column has no 1's left, which means there is no solution)
def get_lowest_column(row_active, col_active):
    lowest_col = None
    lowest_count = rows # all rows 1 (which can't be the case)
    for col in active_cols(col_active):
        # col is not covered
        count = 0
        for row in active_rows(row_active):
            count += matrix[row][col]
        if count < lowest_count:
            lowest_count = count
            lowest_col = col
    return (lowest_col, lowest_count)

def cover(sel_row, row_active, col_active):
    # for each column that has a 1 in selected row
    for col in active_cols(col_active):
        if matrix[sel_row][col] == 1:
            # for each of these columns, go over each row and if they have a 1, cover it
            for row in active_rows(row_active):
                if matrix[row][col] == 1:
                    row_active[row] = False
            # and cover this column
            col_active[col] = False

def algo_x(row_active, col_active, partial):
    if True not in col_active:
        # no columns left, solution found
        solutions.append(partial)
        return
    # select column in matrix with lowest amount of 1's
    col, count = get_lowest_column(row_active, col_active)
    if count == 0:
        # not a solution
        return
    # for each row that has a 1 in in selected column
    for row in active_rows(row_active):
        if matrix[row][col] == 1:
            # add to partial solution
            n_partial = partial.copy()
            n_partial.append(row)
            # cover rows and cols
            n_row_active = row_active.copy()
            n_col_active = col_active.copy()
            cover(row, n_row_active, n_col_active)
            # repeat on new matrix
            algo_x(n_row_active, n_col_active, n_partial)

matrix = [
    [0, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0]
]
rows = len(matrix)
cols = len(matrix[0])

row_active = [True] * rows
col_active = [True] * cols
solutions = []
algo_x(row_active, col_active, [])
print(solutions)
