
import math


class Reversi:
    def __init__(self):
        self.board = [0 for x in range(64)]
        self.turn = 1 # 1: player 1; 2: player 2; 0: game ended
        self.board[3 * 8 + 3] = 2
        self.board[3 * 8 + 4] = 1
        self.board[4 * 8 + 3] = 1
        self.board[4 * 8 + 4] = 2

    def start(self):
        self.print_board()
        print("Player {} to move".format(self.turn))

    def do_move(self, x, y):
        if self.turn == 0:
            print("I said, the game has ended!")
            return
        if not self.in_range(x) or not self.in_range(y):
            print("Invalid coordinates: ({}, {}), player {}".format(x, y, self.turn))
            return
        moves = self.handle_turn(x, y, self.turn, self.board)
        if moves is None:
            print("Can't do move: ({}, {}), player {}".format(x, y, self.turn))
            return
        # apply changes to board
        for move in moves:
            self.board[move[1] * 8 + move[0]] = self.turn
        # swap turns
        self.turn = 1 if self.turn == 2 else 2
        # check if 'next' player can do any moves
        if not self.can_move(self.turn):
            # he couldn't, so swap back to 'current' player and check again
            self.turn = 1 if self.turn == 2 else 2
            if not self.can_move(self.turn):
                # 'current' player can't move either, game has ended
                self.turn = 0
        self.print_board()
        if self.turn != 0:
            print("Player {} to move".format(self.turn))
        else:
            print("Game has ended")

    def print_board(self):
        for y in range(8):
            for x in range(8):
                piece = self.board[y * 8 + x]
                if piece == 0:
                    print(".", end="")
                elif piece == 1:
                    print("O", end="")
                elif piece == 2:
                    print("#", end="")
            print("")

    def can_move(self, turn):
        for x in range(8):
            for y in range(8):
                if self.handle_turn(x, y, turn, self.board) is not None:
                    return True
        return False

    def handle_turn(self, mx, my, turn, board):
        # if there is already a piece there, invalid move
        if board[my * 8 + mx] != 0:
            return None
        allowed = False
        changes = [] # list of changed pieces
        for i in range(-1, 2):
            for j in range(-1, 2):
                # for each of the 8 cells
                # if it is out of range, check next cell
                if not self.in_range(mx + i) or not self.in_range(my + j):
                    continue
                # get the coords for the piece next to the placed piece
                cx = mx + i
                cy = my + j
                # if it is our piece or empty, check next cell
                if board[cy * 8 + cx] == turn or board[cy * 8 + cx] == 0:
                    continue
                can_do = False
                t = 2 # amount of pieces away from placed piece
                # starting at 2 because we know the first piece in the direction must be from the other player
                while self.in_range(mx + (i * t)) and self.in_range(my + (j * t)):
                    tcx = mx + (i * t)
                    tcy = my + (j * t)
                    # if the cell is empty, not valid
                    if board[tcy * 8 + tcx] == 0:
                        break
                    # if the cell is our piece, it is valid, indicate and break
                    if board[tcy * 8 + tcx] == turn:
                        can_do = True
                        break
                    t += 1
                if can_do:
                    # we can do a move, append to changes the pieces that will flip
                    u = 1 # amount of pieces away from placed piece
                    while self.in_range(mx + (i * u)) and self.in_range(my + (j * u)):
                        tcx = mx + (i * u)
                        tcy = my + (j * u)
                        # break if we hit our piece
                        if board[tcy * 8 + tcx] == turn:
                            break
                        changes.append((tcx, tcy))
                        u += 1
                    allowed = True
        if allowed:
            # add the just placed piece to changes
            changes.append((mx, my))
            return changes
        return None

    def in_range(self, val):
        return val >= 0 and val < 8

reversi = Reversi()

# ----- AI (minimax) -----

MAX_DEPTH = 4
WEIGHTS = [
    100, 3, 20, 12, 12, 20, 3, 100,
    3, 1, 6, 6, 6, 6, 1, 3,
    20, 6, 12, 10, 10, 12, 6, 20,
    12, 6, 10, 8, 8, 10, 6, 12,
    12, 6, 10, 8, 8, 10, 6, 12,
    20, 6, 12, 10, 10, 12, 6, 20,
    3, 1, 6, 6, 6, 6, 1, 3,
    100, 3, 20, 12, 12, 20, 3, 100,
]

# returns ((x, y), score)
def minimax(board, turn, depth, us):
    if depth > MAX_DEPTH:
        # calculate board score
        score = get_score(board, us)
        return ((0, 0), score)
    highest_score = -math.inf
    highest_move = None
    lowest_score = math.inf
    lowest_move = None
    # check for all possible moves what scores they get
    for move in get_possible_moves(board, turn):
        # apply it, then minimax it for the other player
        new_board = board.copy()
        for change in move:
            new_board[change[1] * 8 + change[0]] = turn
        result = None
        if len(get_possible_moves(new_board, 1 if turn == 2 else 2)) > 0:
            score = minimax(new_board, 1 if turn == 2 else 2, depth + 1, us)[1]
            result = (move[-1], score) # assumes last in array is the stone that was placed
        else:
            # if other player can not move, minimax ourselves instead
            score = minimax(new_board, turn, depth + 1, us)[1]
            result = (move[-1], score) # assume last in array is the stone that was placed
        if result[1] > highest_score:
            highest_score = result[1]
            highest_move = result
        if result[1] < lowest_score:
            lowest_score = result[1]
            lowest_move = result
    if highest_move is None:
        # there were no moves, get score from board
        score = get_score(board, us)
        return ((0, 0), score)
    if turn == us:
        return highest_move
    return lowest_move

def get_score(board, us):
    total = 0
    for x in range(8):
        for y in range(8):
            if board[y * 8 + x] == us:
                total += WEIGHTS[y * 8 + x]
            elif board[y * 8 + x] != 0:
                total -= WEIGHTS[y * 8 + x]
    return total

def get_best_move(board, player):
    return minimax(board, player, 0, player)[0]

def get_possible_moves(board, turn):
    possible = []
    for x in range(8):
        for y in range(8):
            changes = reversi.handle_turn(x, y, turn, board)
            if changes is not None:
                possible.append(changes)
    return possible

# ----- running -----

reversi.start()
while True:
    print("Move: ", end="")
    move = input().split(",")
    (x, y) = tuple(move)
    reversi.do_move(int(x), int(y))
    while reversi.turn == 2:
        move = get_best_move(reversi.board.copy(), 2)
        print("AI did move: ({}, {})".format(move[0], move[1]))
        reversi.do_move(move[0], move[1])
    if reversi.turn == 0:
        break
