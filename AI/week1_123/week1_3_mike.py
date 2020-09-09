def to_board(s):
    """Input is a string of space-separated rows filled with N^2 numbers.
       Result is a list of size N^2."""
    s = s.replace("\n", " ")
    return [int(x) for x in s.split()]

# only hor & ver, no wrapping
def neighbors(i, b):
    n = []
    row = i//N # [0..N-1]
    if i + 1 < row * N + N: n.append(i + 1)
    if i - 1 >= row * N: n.append(i - 1)
    if i + N < SIZE: n.append(i + N)
    if i - N >= 0: n.append(i - N)
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
# 0  0  0  0  0  0  0  0  0
# 0 11 12 15 18 21 62 61  0
# 0  6  0  0  0  0  0 60  0
# 0 33  0  0  0  0  0 57  0
# 0 32  0  0  0  0  0 56  0
# 0 37  0  1  0  0  0 73  0
# 0 38  0  0  0  0  0 72  0
# 0 43 44 47 48 51 76 77  0
# 0  0  0  0  0  0  81  0  0 """

s = """
1 0 0
0 5 0
0 0 9 """

b = to_board(s)
print("the board> ", b)
print()

SIZE = len(b) # the total size, e.g. 81
N = int(SIZE**0.5) # size of row or column, e.g. 9

# extract and sort the clues
clues = sorted([int(x) for x in b if x != 0])
assert clues[0] == 1
assert clues[-1] == SIZE # last clue must equal SIZE


# pos = index in list b, count = distance starting from 1, clue_index = index in list clues
# note : will try all paths & will find all solutions
def solve(pos, count, clue_index, b):
    count += 1
    if count > SIZE:
        display(b)
        return
    for n in neighbors(pos, b):
        if 0 < b[n] < count:
            continue
        elif b[n] == clues[clue_index] and count == clues[clue_index]:
            clue_index += 1
            pos = n
            solve(pos, count, clue_index, b)
            return
    for n in neighbors(pos, b):
        temp_b = b.copy()
        if temp_b[n] == 0:
            temp_b[n] = count
            pos = n
            solve(pos, count, clue_index, temp_b)
       

pos = b.index(1)
solve(pos, 1, 1, b)
