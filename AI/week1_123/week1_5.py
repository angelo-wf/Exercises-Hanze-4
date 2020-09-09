import math
import random

# state is a tuple of 9 items with empty spot as 0

def get_next(cur):
    # find where the empty spot is
    current = list(cur)
    i = 0
    for s in current:
        if s == 0:
            break
        i += 1

    final = []
    if i < 6:
        # we can move up into the spot
        new = current.copy()
        item = new[i + 3]
        new[i] = item
        new[i + 3] = 0
        final.append(tuple(new))
    if i > 2:
        # we can move down into the spot
        new = current.copy()
        item = new[i - 3]
        new[i] = item
        new[i - 3] = 0
        final.append(tuple(new))
    if (i % 3) < 2:
        # we can move left into the spot
        new = current.copy()
        item = new[i + 1]
        new[i] = item
        new[i + 1] = 0
        final.append(tuple(new))
    if (i % 3) > 0:
        # we can move right into the spot
        new = current.copy()
        item = new[i - 1]
        new[i] = item
        new[i - 1] = 0
        final.append(tuple(new))
    return final

def heuristic(current, goal):
    return 0

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

def a_star(start, goal):
    frontier = set()
    frontier.add(start)
    path = {}
    score = {}
    score[start] = 0
    priority = {}
    priority[start] = heuristic(start, goal)
    while len(frontier) > 0:
        # find the item in frontier whose priority is lowest
        lowest_prio = math.inf
        current = None
        for item in frontier:
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
                    frontier.add(neighbor)

def randomized_board(start, count):
    state = start
    for i in range(count):
        nb = get_next(state)
        state = nb[random.randint(0, len(nb) - 1)]
    return state

def print_board(current):
    a, b, c, d, e, f, g, h, i = current
    print("{} {} {}\n{} {} {}\n{} {} {}".format(a, b, c, d, e, f, g, h, i))


goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
start = randomized_board(goal, 40)

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

# TODO: add heuristic function, make it work for any NxN board
