
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
    if card in neighbors:
        # twee kaarten van dezelfde soort mogen geen buren zijn
        return False
    if '' in neighbors:
        # kaart grenst nog niet aan alleen maar andere kaarten
        return True
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
# bord[5] kan geen Aas zijn omdat:
# Stel 5 is een Aas
# - 3,4,6,7 kunnen geen A zijn vanwege [5]
# - 3,4,6,7 kunnen geen V zijn vanwege [4]
# - dus 3,4,6,7 moet een H of B zijn
# - er zijn maar 2xH en 2xB kaarten, dus 0,1,2 moet een A of V zijn
# - 1, 2 kunnen niet beide Vrouw of Aas zijn, dus 5 kan geen Aas zijn
# board[5] kan geen Vrouw zijn omdat:
# Stel 5 is een Vrouw
# - 3,4,6,7 kunnen geen V zijn vanwege [5]
# - 3,4,6,7 kunnen geen A zijn vanwege [4]
# - dus 3,4,6,7 moet een H of B zijn
# - er zijn maar 2xH en 2xB kaarten, dus 0,1,2 moet een A of V zijn
# - 1, 2 kunnen niet beide Vrouw of Aas zijn, dus 5 kan geen Vrouw zijn
# Stel 5 is een Boer
# - 3,4,6,7 kunnen geen B zijn vanwege [5]
# - 3,4,6,7 zijn Aas, Vrouw of Heer
# - 6, 7 moeten een Vrouw zijn, omdat Aas aan Heer moet grensen en Heer aan Vrouw moet grenzen
# - Heer kan niet meer grenzen aan Vrouw, dus 5 kan geen Boer zijn
# dus bord[5] moet een Heer zijn!

# - 0 kan geen Aas zijn omdat dan 3 een Heer moet zijn maar 3 kan geen Heer zijn wegens [5]
# Stel 0 is een Vrouw
# - 3 kan geen Vrouw of Aas zijn wegens [4] en [5]
# - 3 kan geen Heer zijn wegens [5], dus 3 = B
# - van 4, 6, 7  moet een een vrouw zijn wegens [2]
# - 6, 7 kunnen geen vrouw zijn want die grenst niet aan een boer, dus 4 = V
# - Elke vrouw grenst aan een boer, dus 2 = B
# - 3 = B, dus 2 kan geen boer zijn, dus 0 is geen Vrouw
# Stel 0 is een Boer
# - 3 kan geen Boer of Heer zijn wegens [5]
# - stel 3 is A
#   - Dan moet 2 = B, als 1, 4 = V, dan grenzen ze aan een Boer
#   - Maar dan moet H op 6 of 7, kan niet wegens [5] 
#   - 6, 7 kunnen geen vrouw zijn want die grenst niet aan een boer, 
# - stel 3 = V
#   - Vrouw moet op 1 of 4 kan niet 2 wegens [5] en kan niet op 6 of 7 wegens [3]
#   - Dan moet 2 = B wegens [3]
#   - 4, 6, 7 kunnen geen Heer zijn wegens [5]
#   - dus 1 = H, kan niet wegens [2]
# Dus 0 kan geen Boer zijn


