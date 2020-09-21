from random import choice

def create_board():
    board = []
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(size):
        board.append([])
        for j in range(size):
            board[i].append(choice(letters))
    return board

def print_board(board):
    for row in board:
        for c in row:
            print(c, end=" ")
        print()

def load_words():
    words = []
    with open("words.txt", "r", encoding="cp1250") as f:
        for line in f:
            word = line.strip()
            words.append(word)
    print("Loaded {} words".format(len(words)))
    return words

def create_prefix_set(words):
    final = set()
    for w in words:
        for l in range(1, len(w)):
            final.add(w[0:l])
    return final

def get_neighbors(row, col):
    neighbors = []
    neighbors.append(((row - 1) % size, col))
    neighbors.append(((row + 1) % size, col))
    neighbors.append((row, (col - 1) % size))
    neighbors.append((row, (col + 1) % size))
    return neighbors

def solve(row, col, path, done, found):
    # for each neightbor, check if the path is in the words array and print it
    # then, check if it is in the prefix array, and then solve for that state
    done.append((row, col))
    for s in get_neighbors(row, col):
        letter = board[s[0]][s[1]]
        path = path + letter
        if s not in done:
            if path in words:
                print("Found word: {}".format(path))
                found.append(path)
            if path in prefixes:
                solve(s[0], s[1], path, done.copy(), found)
        path = path[:-1]
    return found

def find_words():
    all = []
    for x in range(size):
        for y in range(size):
            print("starting at {}, {}".format(x, y))
            solve(x, y, board[x][y], [], all)
    return all

# The time comlexity is O(n^2); (with n as board size)

size = 4

words = load_words()
prefixes = create_prefix_set(words)

board = create_board()
print_board(board)

all_words = find_words()
print(all_words)
