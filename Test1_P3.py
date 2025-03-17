import numpy as np
import matplotlib.pyplot as plt
import random


class EightQueens:
    # self is a reference to the current instance of the class, allowing access to its attributes and methods.
    # __init__ is a special method that initializes the instance when it is created.
    def __init__(self):     #Constructor to initialize the state of the board
        self.state = np.random.permutation(8)  #Initialize with a random permutation of 8 queens

    def heuristic(self):
        
        attacks = 0
        for i in range(8):  # for each queen
            for j in range(i + 1, 8):   # check for each pair of queens
                #same diagonal is calculated by checking if the absolute difference in rows is equal to the absolute difference in columns
                if (abs(self.state[i] - self.state[j]) == j - i) or self.state[i] == self.state[j]:
                    attacks += 1
        return attacks

    def get_neighbors(self):
        neighbors = []
        for col in range(8):
            for row in range(8):
                if self.state[col] != row:  #to avoid moving the queen to its current position
                    new_state = self.state.copy()
                    new_state[col] = row
                    neighbors.append(EightQueens())
                    neighbors[-1].state = new_state
        return neighbors

    def hill_climb(self):
        best_state = self
        best_cost = self.heuristic()
        attempts = 0
        while best_cost > 0 and attempts < 1000:
            neighbors = self.get_neighbors()
            best_neighbor = min(neighbors, key=lambda x: x.heuristic())
            if best_neighbor.heuristic() < best_cost:
                best_state = best_neighbor
                best_cost = best_neighbor.heuristic()
            else:
                best_state = EightQueens()
                best_cost = best_state.heuristic()
            attempts += 1
        return best_state, best_cost

# 8-Puzzle problem
class EightPuzzle:
    def __init__(self, state=None):
        self.goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        if state is None:
            self.state = self.shuffle()
        else:
            self.state = state

    def shuffle(self):
        state = np.array(self.goal).flatten()
        np.random.shuffle(state)
        return state.reshape((3, 3))

    def heuristic(self):
        misplaced = 0
        for x in range(3):
            for y in range(3):
                val = self.state[x, y]
                if val != 0 and val != self.goal[x, y]:
                    misplaced += 1
        return misplaced

    def get_neighbors(self):
        neighbors = []
        x, y = np.argwhere(self.state == 0)[0]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = self.state.copy()
                new_state[x, y], new_state[nx, ny] = new_state[nx, ny], new_state[x, y]
                neighbors.append(EightPuzzle(new_state))
        return neighbors

    def hill_climb(self):
        best_state = self
        best_cost = self.heuristic()
        attempts = 0
        while best_cost > 0 and attempts < 1000:
            neighbors = self.get_neighbors()
            best_neighbor = min(neighbors, key=lambda x: x.heuristic())
            if best_neighbor.heuristic() < best_cost:
                best_state = best_neighbor
                best_cost = best_neighbor.heuristic()
            else:
                best_state = EightPuzzle()
                best_cost = best_state.heuristic()
            attempts += 1
        return best_state, best_cost

# Running the algorithms for 1000 iterations and plotting
iterations = 1000

# For each iteration, we will store the best cost found as a list
EQ_costs = []
EP_costs = []

for iteration in range(iterations):
    # Creating a new instance of the classes EightQueens and EightPuzzle
    eq_instance = EightQueens()

    # Running the hill climbing algorithm on the instance and appending the best cost found to the list
    best_state, cost = eq_instance.hill_climb()
    EQ_costs.append(cost)

    # 8-Puzzle
    ep_instance = EightPuzzle()
    best_state, cost = ep_instance.hill_climb()
    EP_costs.append(cost)

# Plotting results
plt.plot(range(iterations), EQ_costs, label='8-Queens')
plt.plot(range(iterations), EP_costs, label='8-Puzzle')
plt.xlabel('Iterations')
plt.ylabel('Best Cost')
plt.legend()
plt.title('Hill Climbing with Random Restart')
plt.show()
