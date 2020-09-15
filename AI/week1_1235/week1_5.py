import math
import random

SIZE = 3 # board dimension (3 = 3x3 board)
USE_HEURISTIC = True # use heuristic (False = UCS, True = A*)

# state is a tuple of SIZE*SIZE items with empty spot as 0

def get_next(cur):
    # find where the empty spot is
    current = list(cur)
    i = 0
    for s in current:
        if s == 0:
            break
        i += 1

    final = []
    if i < (SIZE * (SIZE - 1)):
        # we can move up into the spot
        new = current.copy()
        item = new[i + SIZE]
        new[i] = item
        new[i + SIZE] = 0
        final.append(tuple(new))
    if i > (SIZE - 1):
        # we can move down into the spot
        new = current.copy()
        item = new[i - SIZE]
        new[i] = item
        new[i - SIZE] = 0
        final.append(tuple(new))
    if (i % SIZE) < (SIZE - 1):
        # we can move left into the spot
        new = current.copy()
        item = new[i + 1]
        new[i] = item
        new[i + 1] = 0
        final.append(tuple(new))
    if (i % SIZE) > 0:
        # we can move right into the spot
        new = current.copy()
        item = new[i - 1]
        new[i] = item
        new[i - 1] = 0
        final.append(tuple(new))
    return final

def heuristic(current, goal):
    if not USE_HEURISTIC:
        return 0

    # heuristic: the sum of the distances between current pos and goal pos of each non-empty tile
    totaldist = 0
    for i in range(1, SIZE*SIZE):
        # for each spot not empty
        # figure out where they are in both boards
        curloc = 0
        for s in current:
            if s == i:
                break
            curloc += 1
        goalloc = 0
        for s in goal:
            if s == i:
                break
            goalloc += 1
        # get them as coords
        curx = curloc % SIZE
        cury = curloc // SIZE
        goalx = goalloc % SIZE
        goaly = goalloc // SIZE
        # get distance between them
        dist = abs(curx - goalx) + abs(cury - goaly)
        totaldist += dist
    return totaldist

def get_score(first, second):
    return 1

def get_path(path, start, goal):
    current = goal
    final = [goal]
    while current != start:
        prev = path[current]
        final.append(prev)
        current = prev
    return final[::-1]

# based on code from wikipedia:
# https://en.wikipedia.org/wiki/A*_search_algorithm
def a_star(start, goal):
    frontier = []
    frontier.append(start)
    path = {}
    score = {}
    score[start] = 0
    priority = {}
    priority[start] = heuristic(start, goal)
    while len(frontier) > 0:
        # find the item in frontier whose priority is lowest
        lowest_prio = math.inf
        current = None
        for item in frontier[::-1]:
            if priority[item] < lowest_prio:
                lowest_prio = priority[item]
                current = item

        if current == goal:
            return get_path(path, start, goal)
        frontier.remove(current)
        for neighbor in get_next(current):
            new_score = score.get(current, math.inf) + get_score(current, neighbor)
            if new_score < score.get(neighbor, math.inf):
                path[neighbor] = current
                score[neighbor] = new_score
                priority[neighbor] = new_score + heuristic(neighbor, goal)
                if not neighbor in frontier:
                    frontier.append(neighbor)

def create_board():
    board = []
    for i in range(SIZE*SIZE):
        board.append(i + 1)
    board[SIZE*SIZE - 1] = 0
    return tuple(board)

def randomized_board(start, count):
    state = start
    for i in range(count):
        nb = get_next(state)
        state = nb[random.randint(0, len(nb) - 1)]
    return state

def print_board(current):
    for y in range(SIZE):
        for x in range(SIZE):
            print("{:02d} ".format(current[y * SIZE + x]), end="")
        print("")


goal = create_board()
start = randomized_board(goal, 20)

print("Starting board:")
print_board(start)
print("Goal board:")
print_board(goal)

path = a_star(start, goal)
# print(path)
print("Path:")
for item in path:
    print_board(item)
    print("")
