import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node

    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
        self.finder = {}

    def empty(self):
        return len(self.elements) == 0

    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        if item in self.finder:
            self.remove(item)
        entry = [priority, item, ""]
        self.finder[item] = entry
        heapq.heappush(self.elements, entry)

    def remove(self, item):
        entry = self.finder.pop(item)
        entry[2] = "REMOVED"

    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        while True:
            entry = heapq.heappop(self.elements)
            if entry[2] != "REMOVED":
                del self.finder[entry[1]]
                return entry[1]
            if self.empty():
                raise KeyError("failed to find item")


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def search(app, type):

    path = None
    if type == "UC":
        print("Doing UCS")
        path = ucs(app)
    else:
        print("Doing A*")
        path = astar(app)
    app.re_plot()
    app.draw_path(path)

def get_next(s):
    final = []
    if s[0] > 0 and get_grid_value((s[0] - 1, s[1])) != 'b':
        final.append((s[0] - 1, s[1]))
    if s[0] < cf.SIZE - 1 and get_grid_value((s[0] + 1, s[1])) != 'b':
        final.append((s[0] + 1, s[1]))
    if s[1] > 0 and get_grid_value((s[0], s[1] - 1)) != 'b':
        final.append((s[0], s[1] - 1))
    if s[1] < cf.SIZE - 1 and get_grid_value((s[0], s[1] + 1)) != 'b':
        final.append((s[0], s[1] + 1))
    return final

def heuristic(s, g):
    return abs(s[0] - g[0]) + abs(s[1] - g[1])

def ucs(app):
    frontier = PriorityQueue()
    frontier.put(cf.START, get_grid_value(cf.START))
    visited = set()
    visited.add(cf.START)
    path = {}
    while not frontier.empty():
        s = frontier.get()
        if s == cf.GOAL:
            return path
        visited.add(s)
        for next_s in get_next(s):
            new_cost = get_grid_value(s) + 1 # 1: cost of going to next node
            if (not next_s in visited) or (new_cost < get_grid_value(next_s)):
                set_grid_value(next_s, new_cost)
                frontier.put(next_s, get_grid_value(next_s))
                visited.add(s) # needed? Slides only show for a-star
                path[next_s] = s

                app.re_plot()
                app.draw_path(path, next_s)
                app.pause()

def astar(app):
    frontier = PriorityQueue()
    frontier.put(cf.START, get_grid_value(cf.START))
    visited = set()
    visited.add(cf.START)
    path = {}
    while not frontier.empty():
        s = frontier.get()
        if s == cf.GOAL:
            return path
        visited.add(s)
        for next_s in get_next(s):
            new_cost = get_grid_value(s) + 1 # 1: cost of going to next node
            if (not next_s in visited) or (new_cost < get_grid_value(next_s)):
                set_grid_value(next_s, new_cost)
                priority = new_cost + heuristic(next_s, cf.GOAL)
                frontier.put(next_s, priority)
                visited.add(s) # needed? Slides only show for a-star
                path[next_s] = s

                app.re_plot()
                app.draw_path(path, next_s)
                app.pause()
