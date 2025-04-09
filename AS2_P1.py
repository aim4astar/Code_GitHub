'''Consider a 4 × 4 GridWorld where each cell represents a state. Your goal is to reach a terminal state located at the
bottom-right cell. Some cells are obstacles, and you cannot pass through them. You have four actions: move {up,
down, left, right}. Each movement has a reward of −1, except for reaching the terminal cell, which yields a reward
of +10. You cannot move outside the grid or into obstacles. The intended action occurs with probability 0.8, and
perpendicular movements occur with probability 0.1 each. Hitting a wall keeps the agent in the same position, and
assume γ = 0.98
Task:
• Implement the Value Iteration algorithm.
• Compute the optimal state values and the optimal policy.
• Clearly display the optimal policy as arrows indicating the best action for each state.'''

import matplotlib.pyplot as plt
import numpy as np
import math


grid_size = 4
action_labels = ['U', 'D', 'L', 'R'] #tuple
actions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)} #dictionary
obstacles = [(1, 1), (2, 2)] #tuple
reward = -1
terminal = (3, 3)
terminal_utility = 10
gamma = 0.98
threshold = 1e-6

action_utilities = np.zeros((grid_size, grid_size, len(action_labels)))
utils = np.zeros((grid_size, grid_size))

arrow_directions = {'U': (0, 0.3), 'D': (0, -0.3), 'L': (-0.3, 0), 'R': (0.3, 0)}

def is_valid(state):
    i, j = state[0], state[1]
    return 0 <= i < grid_size and 0 <= j < grid_size and (i, j) not in obstacles


def get_next_state(state, action):
    curr_i, curr_j = state[0], state[1]
    di, dj = actions[action]
    new_i, new_j = curr_i + di, curr_j + dj
    if (is_valid((new_i, new_j))):
        return (new_i, new_j)
    
    return state

def value_iteration():
    global action_utilities, utils

    iterations = 0
    utils[terminal] = terminal_utility

    while True:
        util_change = 0
        iterations += 1

        for i in range(grid_size):
            for j in range(grid_size):
                if (i, j) == terminal or (i, j) in obstacles:
                    continue

                max_summation = -math.inf

                for action_index, a in enumerate(action_labels):
                    summation = 0

                    intended_next_state = get_next_state((i, j), a)
                    summation += 0.8 * utils[intended_next_state]
                    
                    
                    if a in ['U', 'D']:
                        left_state = get_next_state((i, j), 'L')
                        right_state = get_next_state((i, j), 'R')
                    else:
                        left_state = get_next_state((i, j), 'U')
                        right_state = get_next_state((i, j), 'D')

                    summation += 0.1 * utils[left_state]
                    summation += 0.1 * utils[right_state]

                    action_util = reward + gamma * summation
                    action_utilities[i, j, action_index] = action_util

                    max_summation = max(max_summation, summation)

                
                state_util = reward + gamma * max_summation
                util_change = max(util_change, abs(utils[i, j] - state_util))
                utils[i, j] = state_util
        
        if util_change < threshold:
            print("Converged in:", iterations, "iterations!")
            break


def plot(action_utilities):
    # Plotting utilities
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks(np.arange(0, grid_size, 1))
    ax.set_yticks(np.arange(0, grid_size, 1))
    ax.grid(True)

    for obs in obstacles:
        obs_x, obs_y = obs[1], grid_size - obs[0] - 1
        ax.add_patch(plt.Rectangle((obs_x, obs_y), 1, 1, color='gray', alpha=0.5))

    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in obstacles:
                continue
            cell_x, cell_y = j, grid_size - i - 1
            if (i, j) == terminal:
                ax.text(cell_x + 0.5, cell_y + 0.5, f'{terminal_utility:.1f}', fontsize=12, ha='center', va='center',
                        color='blue', fontweight='bold')
                continue
            ax.plot([cell_x, cell_x + 1], [cell_y, cell_y + 1], color='black', linewidth=0.5)
            ax.plot([cell_x, cell_x + 1], [cell_y + 1, cell_y], color='black', linewidth=0.5)
            utils = action_utilities[i, j]
            positions = {'U': (cell_x + 0.5, cell_y + 0.85),
                         'D': (cell_x + 0.5, cell_y + 0.15),
                         'L': (cell_x + 0.15, cell_y + 0.5),
                         'R': (cell_x + 0.85, cell_y + 0.5)}
            best_action_idx = np.argmax(utils)
            for k, label in enumerate(action_labels):
                color = 'red' if k == best_action_idx else 'black'
                weight = 'bold' if k == best_action_idx else 'normal'
                ax.text(positions[label][0], positions[label][1], f'{utils[k]:.2f}', fontsize=8,
                        ha='center', va='center', color=color, fontweight=weight)
                        
            best_action = action_labels[best_action_idx]
            dx, dy = arrow_directions[best_action]
            ax.arrow(cell_x + 0.5, cell_y + 0.5, dx, dy,
                     head_width=0.15, head_length=0.15, fc='black', ec='black')                     

    plt.show()

# Call the updated gridworld function
value_iteration()
plot(action_utilities)

