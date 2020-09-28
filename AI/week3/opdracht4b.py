
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
        loc = increment_loc(grid, loc)
