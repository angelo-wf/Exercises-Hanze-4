
import copy


def create_board():
    board = {}
    for i in range(8):
        board[i] = ''
    return board

def print_solutions(solutions):
    for solution in solutions:
        print("Found solution after {} recursive calls:".format(solution[1]))
        print_board(solution[0])
    print("Found {} solutions".format(len(solutions)))

def copy_board(board):
    return copy.deepcopy(board)

def print_board(board):
    print("\t\t{}\t\t".format(board[0]))
    print("{}\t{}\t{}\t\t".format(board[1], board[2], board[3]))
    print("\t{}\t{}\t{}\t".format(board[4], board[5], board[6]))
    print("\t\t{}\t\t".format(board[7]))

def get_neighbors(board, i):
    neighbors = {
        0: [3], 
        1: [2], 
        2: [1, 3, 4],
        3: [0, 2, 5],
        4: [2, 5],
        5: [3, 4, 6, 7],
        6: [5],
        7: [5],
    }
    return [board[n] for n in neighbors[i]]

def two_card_in_board(board, card):
    return list(board.values()).count(card) == 2


def test_card(card, neighbors):
    if '' in neighbors:
        return True
    if card in neighbors:
        # twee kaarten van dezelfde soort mogen geen buren zijn
        return False
    if card == 'A':
        if 'V' in neighbors:
            # elke Aas grenst NIET aan een Vrouw
            return False
        elif not 'H' in neighbors:
            # elke Aas grenst aan een Heer
            return False
    if card == 'H' and not 'V' in neighbors:
        # elke Heer grenst aan een Vrouw
        return False
    if card == 'V' and not 'B' in neighbors:
        # elke Vrouw grenst aan een Boer
        return False
    # kaart grenst niet aan de juiste kaart
    return True

def test_board(board):
    for index in board.keys():
        neighbors = get_neighbors(board, index)
        card = board[index]
        if not test_card(card, neighbors):
            return False
    return True

def search(board, i):
    solution = None
    global recursive_calls
    recursive_calls += 1
    for card in ['A', 'H', 'V', 'B']:
        if two_card_in_board(board, card):
            continue
        new_board = copy_board(board)
        new_board[i] = card
        if test_board(new_board):
            if i < 7:
                solution = search(new_board, i + 1)
            else:
                solutions.append((new_board, recursive_calls))
    return solution 
                
solutions = []
recursive_calls = 0

search(create_board(), 0)

print_solutions(solutions)

# B. Eerste oplossing gevonden na 65 recursive calls

# C.

