import random 
import heapq
import copy

size = 3
class PriorityQueue:
   # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def search(app, type):
    path = None
    if type == "UC":
        print("Doing UCS")
        path = ucs(app)
    else:
        print("Doing A*")
        path = astar(app)

def copy_puzzle(puzzle):
    return copy.deepcopy(puzzle)

def get_next(puzzle):
    empty_x = puzzle["empty"][0]
    empty_y = puzzle["empty"][1]
    next_puzzles = []
    for x_diff, y_diff in [(1,0), (0,1), (-1,0), (0,-1)]:
        next_puzzle = copy_puzzle(puzzle)
        new_x = empty_x - x_diff
        new_y = empty_y - y_diff
        try:
            n = next_puzzle["tiles"][new_x][new_y]
            next_puzzle["tiles"][empty_x][empty_y] = n
            next_puzzle["tiles"][new_x][new_y] = 0
            next_puzzle["empty"] = (new_x, new_y)
            next_puzzles.append(next_puzzle)
        except IndexError:
            pass
    return next_puzzles

def is_solved(puzzle):
    i = 1
    for row in puzzle["tiles"]:
        for n in row:
            if n != 0 and n != i:
                return False
            i += 1
    return True
    
def heuristic(s, g): 
    # manhattan distance for 4 dirs, pythagorian distance for 8 dirs
    return abs(s[0] - g[0]) + abs(s[1] - g[1])
    # return math.sqrt((abs(s[0] - g[0]) ** 2) + (abs(s[1] - g[1]) ** 2))

def create_puzzle():
    numbers = list(range(size * size))
    puzzle = {"empty": (-1, -1), "tiles": []}
    for i in range(size):
        puzzle["tiles"].append([])
        for j in range(size):
            n = random.choice(numbers)
            if n == 0: 
                puzzle["empty"] = (i, j)
            numbers.remove(n)
            puzzle["tiles"][i].append(n)
    return puzzle

def print_puzzle(puzzle):
    for row in puzzle["tiles"]:
        for n in row:
            print(n, end="")
        print()
    print('*' * len(puzzle["tiles"]))

def ucs(puzzle):
    i = 0
    frontier = PriorityQueue()
    frontier.put(puzzle, i)
    i += 1
    visited = []
    visited.append(puzzle)
    while not frontier.empty():
        p = frontier.get()
        print_puzzle(p)
        if is_solved(p):
            is_solved(p)
            print_puzzle(p)
            return
        visited.append(p)
        for next_p in get_next(p):
            if (not next_p in visited):
                frontier.put(next_p, i)
                i += 1
                visited.append(next_p) 



def astar(app):
    pass

p = {"empty": (2, 1), "tiles": [[8, 6, 7], [2, 5, 4], [3, 0, 1]] } # create_puzzle()

# p_solved = {"empty": (2, 1), "tiles": [[1, 2, 3], [4, 5, 6], [7, 8, 0]] }
# print(is_solved(p_solved))

print_puzzle(p)

# print(get_next(p))

ucs(p)