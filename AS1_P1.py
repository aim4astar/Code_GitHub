from collections import deque


def is_valid(state):
    M, C, B = state                    #M, C are number of missionaries/Cnbls on the left
    M_right, C_right = 3 - M, 3 - C    #M_right, C_right --> number of mnaries/cnbls on the right

    if (M > 0 and M < C) or (M_right > 0 and M_right < C_right):
        return False

    return True


def get_next_state(state):
    M, C, B = state                                        #destructuring the values from the state and assigning variables for better understanding and                                                             readability

    moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]       #all the possible moves/actions from any state

    next_states = []                                       #saving all the generated valid states in a list

    for m, c in moves:                                     #iterating over all the possible moves and generating new states based on the move
        if(B == 'L'):
            new_state = (M - m, C - c, 'R')
        else:
            new_state = (M + m, C + c, 'L')
        
        if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3 and is_valid(new_state):     #multiple checks are being performed to ensure that the newly                                                                                             generated states are valid
            next_states.append(new_state)                                                 #first, we checked to make sure that the number of                                                                                                        missionaries/cannibals are always 0, 1, 2, or 3
                                                                                          #next, we check for the constraint given in the problem which                                                                                             says that missionaries cannot be outnumbered
    return next_states
        

def bfs():
    #state is represented as (m, c, b) where m is the number of missionaries on the left, c is the number of cannibals on the left, and b is the position of the boat- Left or Right
    start = (3, 3, 'L')
    goal = (0, 0, 'R')
    queue = deque([(start, [])])        #[] is the path, empty at the beginning
    visited = set()                     #to keep track of the states that we're visiting

    while queue:
        state, path = queue.popleft()   #state is the current state, and path the current path

        if state in visited:            #if state has already been visited, we will not explore it again
            continue

        visited.add(state)              #if state has NOT been visited, add it to the set of visited states
        new_path = path + [state]       #the path (sequence of nodes/states visited -- represents a solution) keeps track of the nodes visited so far

        if state == goal:
            return new_path

        for next_state in get_next_state(state):
            queue.append((next_state, new_path))

    
    return None    #No solution found



solution = bfs()
if solution:
    for step in solution:
        print(f"Missionaries(Left): {step[0]}, Cannibals(Left): {step[1]}, Boat: {step[2]}")
else:
    print("No Solution Found!")