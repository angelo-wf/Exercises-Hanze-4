
import time
import math
import copy

grid = {} # (x, y) -> {possible values (for doing Arc Consistency)}
peers = {} # for each cell, list of cells that are in same row, col or cell

def print_grid(grid):
    for y in range(9):
        for x in range(9):
            val = grid[(x, y)]
            print(next(iter(val)) if len(val) == 1 else ".", end="")
            if x % 3 == 2 and x < 8:
                print("|", end="")
        if y % 3 == 2  and y < 8:
            print("")
            for x in range(9):
                print("-", end="")
                if x % 3 == 2 and x < 8:
                    print("+", end="")
        print("")

def create_grid_and_peers():
    for x in range(9):
        for y in range(9):
            grid[(x, y)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            peer_set = set()
            for lv in range(9):
                peer_set.add((x, lv))
                peer_set.add((lv, y))
            # add in same cell, get top left corner of cell
            cell_l = (x // 3) * 3
            cell_t = (y // 3) * 3
            for tx in range(3):
                for ty in range(3):
                    peer_set.add((cell_l + tx, cell_t + ty))
            peer_set.remove((x, y))
            peers[(x, y)] = peer_set

def clear_grid(grid):
    length = 9
    for x in range(9):
        for y in range(9):
            grid[(x, y)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

def fill_grid(grid, string):
    loc = (0, 0)
    string_index = 0
    chars = "123456789"
    clear_grid(grid)
    assert len(string) == 9*9
    for i in range(len(string)):
        char = string[i]
        if char in chars:
            grid[loc] = {int(char)}
        loc = increment_loc(loc)

def is_valid(grid, loc, v):
    for peer in peers[loc]:
        if len(grid[peer]) == 1 and v in grid[peer]:
            return False
    return True

def is_full(grid):
    for y in range(9):
        for x in range(9):
            if len(grid[(x, y)]) > 1:
                return False
    return True

def increment_loc(loc):
    x, y = loc
    x += 1
    if x >= 9:
        x = 0
        y += 1
    return (x, y)

def get_next_loc(grid):
    lowest = math.inf
    loc = None
    for x in range(9):
        for y in range(9):
            length = len(grid[(x, y)])
            if length < lowest and length > 1:
                lowest = length
                loc = (x, y)
    return loc

def copy_grid(grid):
    return copy.deepcopy(grid)

def solve(grid):
    if is_full(grid):
        print("Solution:")
        print_grid(grid)
        return True
    loc = get_next_loc(grid)
    for v in grid[loc]:
        # put in each value and continue to next spot
        if is_valid(grid, loc, v):
            new_grid = copy.deepcopy(grid)
            new_grid[loc] = {v}
            if make_arc_consistent(new_grid, loc, v):
                if solve(new_grid):
                    return True
    return False

def make_arc_consistent(grid, loc, v):
    changed = False
    for peer in peers[loc]:
        # remove value from possibilities
        if v in grid[peer]:
            if len(grid[peer]) == 1:
                # can't remove, not arc consistent
                return False
            else:
                grid[peer].remove(v)
                changed = True
    if changed:
        # we changed, check for other values with only one option
        for peer in peers[loc]:
            if peer != loc and len(grid[peer]) == 1:
                if not make_arc_consistent(grid, peer, next(iter(grid[peer]))):
                    return False
    return True



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

create_grid_and_peers()

for i, puzzle in enumerate(slist):
    fill_grid(grid, puzzle)
    print("Puzzle {}".format(i))
    print_grid(grid)
    start_time = time.time()
    solve(grid)
    taken_time = time.time() - start_time
    print("Took {} seconds".format(taken_time))
