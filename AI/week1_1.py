
# state as a ?
# list[2] of lists?, list[2] of sets?, just a string?

# gets the possible next states from a certain state, only gives valid states
def get_next_states(state):
    return []

# prints the given state
def print_state(state):
    print(state)

# check if a state is the final state
def is_final_state(state):
    return false

# TODO: how to print path to state?

def solve(state):
    # if the current state is the final state, print it and return, else, go through each further possible state
    if is_final_state(state):
        print_state(state)
    else:
        for s in get_next_states(state):
            solve(s)
