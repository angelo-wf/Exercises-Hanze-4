import matplotlib.pyplot as plt
import random
import time
import itertools
import math
import copy
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1])
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(5) # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

def nearest_neighbor(cities):
    cities = set(cities)
    last_city = cities.pop()
    tour = [last_city]
    while len(cities) != 0:
        closest_city = City(x=math.inf, y=math.inf)
        for city in cities:
            if distance(last_city, city) < distance(last_city, closest_city):
                closest_city = city
        tour.append(closest_city)
        last_city = closest_city
        cities.remove(closest_city)
    return tour

def get_intersecting_roads(tour):
    intersecting_roads = []
    tour_copy = tour #copy.deepcopy(tour)
    for i in range(len(tour_copy) - 1):
        for j in range(1, len(tour_copy) - 1):
            roads = ((tour_copy[i], tour_copy[i + 1]), (tour_copy[j], tour_copy[j + 1]))
            if tour_copy[i + 1] != tour_copy[j] and tour_copy[i] != tour_copy[j + 1] and roads[0] != roads[1]:
                if do_intersect(roads):
                    added = False
                    for r in intersecting_roads:
                        if roads[0] == r[1]:
                            added = True
                    if not added:
                        intersecting_roads.append(roads)
    return intersecting_roads

def do_intersect(roads):
    dir1 = dir(roads[0][0], roads[0][1], roads[1][0])
    dir2 = dir(roads[0][0], roads[0][1], roads[1][1])
    dir3 = dir(roads[1][0], roads[1][1], roads[0][0])
    dir4 = dir(roads[1][0], roads[1][1], roads[0][1])

    if dir1 != dir2 and dir3 != dir4:
        return True
    if dir1 == 0 and on_line(roads[0], roads[1][0]):
        return True
    if dir2 == 0 and on_line(roads[0], roads[1][1]):
        return True
    if dir3 == 0 and on_line(roads[1], roads[0][0]):
        return True
    if dir4 == 0 and on_line(roads[1], roads[0][1]):
        return True
    return False

def dir(a, b, c):
    # find direction of line segement
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if val == 0:
       return 0 # collinear
    elif val < 0:
        return 2 # anti-clockwise
    return 1 # clockwise

def on_line(road, city):
    return city.x <= max(road[0].x, road[1].x) and city.x <= min(road[0].x, road[1].x) and city.y <= max(road[0].y, road[1].y) and city.y <= min(road[0].y, road[1].y)

def two_opt_swap(tour, i, j):
    # new_tour = tour[:i]
    # new_tour.extend(reversed(tour[i:j]))
    # new_tour.extend(tour[j:])
    new_tour = tour[:i]
    new_tour.extend(reversed(tour[i:j + 1]))
    new_tour.extend(tour[j + 1:])
    return new_tour

def two_opt(cities):
    tour = nearest_neighbor(cities)
    intersecting_roads = get_intersecting_roads(tour)
    # print(tour)
    # print(len(tour))
    # print(intersecting_roads, len(intersecting_roads))
    print("intersections: {}".format(len(intersecting_roads)))
    for roads in intersecting_roads:
        # min_index = min(tour.index(roads[0][0]), tour.index(roads[1][1]))
        # max_index = max(tour.index(roads[0][0]), tour.index(roads[1][1]))
        min_index = tour.index(roads[0][1])
        max_index = tour.index(roads[1][0])
        tour = two_opt_swap(tour, min_index, max_index)
        # print(tour)
        # print(len(tour))
    return tour

# print(City(x=335, y=77) == City(x=335, y=77))
# print(do_intersect(((City(x=400, y=150), City(x=400, y=100)), (City(x=300, y=200), City(x=450, y=200)))))
# plot_tsp(try_all_tours, make_cities(100))
plot_tsp(nearest_neighbor, make_cities(25))
plot_tsp(two_opt, make_cities(25))

# A.
# using seed n = 10
# optimal tour has length 2521.9
# nn tour has length 3230.6
# difference in % = 28.1

# B.
# using 500 cities nn takes 0.117s
# tour has length 19447.7

# C.
# using 100 cities, there are 6 "intersecting roads"
# You can find "intersecting roads" by ...
# You don't have to check if the route is shorter,
# because removing a "intersecting roads" while always be shorter in this case by ysing equal weigths
