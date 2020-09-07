def to_board(s):
    """Input is a string of space-separated rows filled with N^2 numbers.
       Result is a list of size N^2."""
    s = s.replace("\n", " ")
    return [int(x) for x in s.split()]

# only hor & ver, no wrapping
def neighbors(i):
    n = [] # changed () to []
    row = i//N # [0 ..N-1]

    col = i % N

    if col > 0:
        n.append(i - 1)
    if col < N - 1:
        n.append(i + 1)
    if row > 0:
        n.append(i - N)
    if row < N - 1:
        n.append(i + N)

    n = tuple(n)
    return n

def display(board):
    "input is a list of integers, print the list as a board"
    for i in range(0, SIZE, N):
        s = ''
        for x in board[i:i+N]: # extract the rows
            assert x < 100
            s = s + '{:3d}'.format(x)
        print(s)

# s = """
# 0  0  0  0  0  0  0  0 81
# 0  0 46 45  0 55 74  0  0
# 0 38  0  0 43  0  0 78  0
# 0 35  0  0  0  0  0 71  0
# 0  0 33  0  0  0 59  0  0
# 0 17  0  0  0  0  0 67  0
# 0 18  0  0 11  0  0 64  0
# 0  0 24 21  0  1  2  0  0
# 0  0  0  0  0  0  0  0  0 """

# s = """
# 1 0 0
# 0 5 0
# 0 0 9 """

# s = """
#  7  0  3  0  1  0 59  0 81
#  0  0  0 33 34 57  0  0  0
#  9  0 31  0  0  0 63  0 79
#  0 29  0  0  0  0  0 65  0
# 11 12  0  0 39  0  0 66 77
#  0 13  0  0  0  0  0 67  0
# 15  0 23  0  0  0 69  0 75
#  0  0  0 43 42 49  0  0  0
# 19  0 21  0 45  0 47  0 73"""

s = """
11 0  13 0  19 0  25 0  27
0  0  0  0  0  0  0  0  0
7 0  0  0  0  0  0  0  33
0  0  0  0  0  0  0  0  0
81 0  0  0  0  0  0  0  49
0  1  0  0  0  0  0  0  0
79 0  0  0  0  0  0  0  53
0  0  0  0  0  0  0  0  0
75 0  73 0  63 0  59 0  55"""

# s = """
# 11 12 13 18 19 24 25 26 27
# 10 9  14 17 20 23 30 29 28
# 7  8  15 16 21 22 31 32 33
# 6  5  4  39 38 37 36 35 34
# 81 2  3  40 41 42 47 48 49
# 80 1  70 69 68 43 46 51 50
# 79 78 71 66 67 44 45 52 53
# 76 77 72 65 62 61 58 57 54
# 75 74 73 64 63 60 59 56 55"""

b = to_board(s)

SIZE = len(b) # the total size, e.g. 81
N = int(SIZE**0.5) # size of row or column, e.g. 9

print("The board:")
display(b)
print("Solutions:") # changed a bit


# extract and sort the clues
clues = sorted([int(x) for x in b if x != 0])
assert clues[0] == 1
assert clues[-1] == SIZE # last clue must equal SIZE


# pos = index in list b, count = distance starting from 1, clue_index = index in list clues
# note : will try all paths & will find all solutions
def solve(pos, count, clue_index):

    #check if valid
    valid = False
    if b[pos] == 0 and clues[clue_index] != count:
        # empty spot and not past the next clue
        valid = True
    if b[pos] != 0 and b[pos] == count:
        # spot filled with correct number
        valid = True
    if valid:
        b[pos] = count
    else:
        return

    #if we hit a clue, clue_index++, if we hit the last one, print the board
    if b[pos] == clues[clue_index]:
        clue_index += 1
        if b[pos] == clues[-1]:
            display(b)
            print(" ")
            return

    #check all neighbors
    for n in neighbors(pos):
        solve(n, count + 1, clue_index)
    if b[pos] not in clues:
        b[pos] = 0


pos = b.index(1)
solve(pos, 1, 0)
