
import time

SIZE = 3 # size of box within sudoku (2: 4x4 sudoku, 3: 9x9 sudoku)

def clear_grid(grid):
    length = SIZE*SIZE
    for x in range(length):
        for y in range(length):
            grid[(x, y)] = 0

def fill_grid(grid, string):
    loc = (0, 0)
    string_index = 0
    chars = "123456789"
    clear_grid(grid)
    assert len(string) == SIZE*SIZE*SIZE*SIZE
    for i in range(len(string)):
        char = string[i]
        if char in chars:
            grid[loc] = int(char)
        loc = increment_loc(loc)

def increment_loc(loc):
    x, y = loc
    x += 1
    if x >= SIZE*SIZE:
        x = 0
        y += 1
    return (x, y)

def print_grid(grid):
    for y in range(SIZE*SIZE):
        for x in range(SIZE*SIZE):
            val = grid[(x, y)]
            print(val if val > 0 else ".", end="")
            if x % SIZE == SIZE - 1 and x < (SIZE * SIZE) - 1:
                print("|", end="")
        if y % SIZE == SIZE - 1  and y < (SIZE * SIZE) - 1:
            print("")
            for x in range(SIZE*SIZE):
                print("-", end="")
                if x % SIZE == SIZE - 1  and x < (SIZE * SIZE) - 1:
                    print("+", end="")
        print("")

# getting matrix from grid, final grid from exact cover

def make_matrix():
    # create a matrix for a sudoku
    length = SIZE*SIZE
    row_count = length * length * length # rows: for each cell (l*l) l options
    col_count = length * length * 4 # each cell unique value (l*l), each value in each row, col and box (l*l)
    # create the initial matrix
    matrix = [None] * row_count
    for i in range(row_count):
        matrix[i] = [0] * col_count
    for x in range(length):
        for y in range(length):
            loc = (y * length + x)
            # handle unique value
            for i in range(length):
                matrix[loc * length + i][loc] = 1
            # handle rows
            for i in range(length):
                matrix[loc * length + i][length*length + y * length + i] = 1
            # handle cols
            for i in range(length):
                matrix[loc * length + i][2*length*length + x * length + i] = 1
            # handle boxes
            box_x = x // SIZE
            box_y = y // SIZE
            box = box_y * SIZE + box_x
            # handle cols
            for i in range(length):
                matrix[loc * length + i][3*length*length + box * length + i] = 1
    return matrix

def cover_clues(grid, row_active, col_active):
    # given the known clues, covers the rows/cols that are no longer possible/needed
    # return the rows that correspond to the clues
    clue_rows = []
    length = SIZE*SIZE
    for x in range(length):
        for y in range(length):
            if grid[(x, y)] > 0:
                cell = y * length + x
                val = grid[(x, y)] - 1
                row = cell * length + val
                cover(row, row_active, col_active)
                clue_rows.append(row)
    return clue_rows

def make_final_grid(grid, solution):
    # fills the grid according to the rows returned by algorithm X
    length = SIZE*SIZE
    for row in solution:
        cell = row // length
        val = row % length
        cell_x = cell % length
        cell_y = cell // length
        grid[(cell_x, cell_y)] = val + 1

# algorithm X

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

def get_lowest_column(row_active, col_active):
    # get column with lowest amount of 1's and this amount (for detecting empty columns)
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
        return True
    # select column in matrix with lowest amount of 1's
    col, count = get_lowest_column(row_active, col_active)
    if count == 0:
        # not a solution
        return False
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
            if algo_x(n_row_active, n_col_active, n_partial):
                return True
    return False

slist = [None for x in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10]= '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11]= '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13]= '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14]= '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15]= '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16]= '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17]= '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18]= '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19]= '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'

grid = {}
matrix = make_matrix()
rows = len(matrix)
cols = len(matrix[0])

for i, puzzle in enumerate(slist):

    # if i == 12:
    #     continue

    print("Puzzle {}:".format(i))
    fill_grid(grid, puzzle)
    print_grid(grid)

    solutions = []

    row_active = [True] * rows
    col_active = [True] * cols
    start_time = time.time()
    partial = cover_clues(grid, row_active, col_active)
    algo_x(row_active, col_active, partial)
    taken_time = time.time() - start_time

    for solution in solutions:
        print("Solution:")
        make_final_grid(grid, solution)
        print_grid(grid)

    print("Took {} seconds".format(taken_time))
