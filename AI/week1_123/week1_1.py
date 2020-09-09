
# from math import factorial

# gets the possible next states from a certain state, only gives valid states
def get_next_states(state):
    retstates = []
    possible = ['G', 'W', 'C']
    source = 0
    dest = 1
    if 'F' in state[1]:
        source = 1
        dest = 0
    
    # going right
    for p in possible:
        if p in state[source]:
            newstate = copy_state(state)
            newstate[source].remove('F')
            newstate[source].remove(p)
            newstate[dest].add('F')
            newstate[dest].add(p)
            retstates.append(newstate)
    newstate = copy_state(state)
    newstate[source].remove('F')
    newstate[dest].add('F')
    retstates.append(newstate)
    return retstates

# copy state
def copy_state(state):
    return (state[0].copy(), state[1].copy())

# checks if a state is valid
def is_valid(state):
    for i in range(2):
        if 'G' in state[i] and 'C' in state[i] and not 'F' in state[i]:
            return False
        if 'W' in state[i] and 'G' in state[i] and not 'F' in state[i]:
            return False
    return True

# prints the given state
def print_state(state):
    for s in state[0]:
        print(s, end='')
    print(" | ", end='')
    for s in state[1]:
        print(s, end='')
    print()

# check if a state is the final state
def is_final_state(state):
    if state[0] == set() and state[1] == {'F', 'G', 'C', 'W'}:
        return True
    return False

def solve(state, visited):
    # if the current state is the final state, print it and return, else, go through each further possible state
    visited.append(copy_state(state))
    # print("solve with state: ", state)
    if is_final_state(state):
        print("Solution found:")
        print_state(state)
        print("Steps:")
        for s in visited:
            print_state(s)
        print("---")
    else:
        for s in get_next_states(state):
            if is_valid(s):
                # print("Valid next state: ", s)
                if s not in visited:
                    solve(s, visited.copy())

state = ({'F', 'G', 'C', 'W'}, set())
solve(state, [])

# The time comlexity is O(2^n)

# def amount_of_options(n):
#     sum = 0
#     for k in range(n + 1):
#         sum += factorial(n) / (factorial(k) * factorial(n - k))
#     return sum

# for i in range(10):
#     print("options for {}:".format(i), amount_of_options(i))