
import itertools


def create_board(permutation):
    board = {}
    for i in range(len(permutation)):
        board[i] = permutation[i]
    return board

def print_board(board):
    print("\t\t{}\t\t".format(board[0]))
    print("{}\t{}\t{}\t\t".format(board[1], board[2], board[3]))
    print("\t{}\t{}\t{}\t".format(board[4], board[5], board[6]))
    print("\t\t{}\t\t".format(board[7]))

def print_solutions(solutions):
    for solution in solutions:
        print("Found solution after {} iterations".format(solution[1]))
        print_board(solution[0])
    print("Found {} solutions".format(len(solutions)))


def create_permutations():
    cards = ['A', 'A', 'H', 'H', 'V', 'V', 'B', 'B']
    permutations = set(itertools.permutations(cards))
    return permutations

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


def test_card(card, neighbors):
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

def test_all():
    permutations = create_permutations()
    iterations_count = 0
    solutions = []
    for permutation in permutations:
        iterations_count  += 1
        board = create_board(permutation) 
        if test_board(board):
            if not board in solutions:
                solutions.append((board, iterations_count))
    print_solutions(solutions)

test_all()

# A. 
# 1. Er zijn 2520 permutaties mogelijk 
# 2. Er moeten 1582 iteraties worden gedaan voor de eerste oplossing is gevonden
