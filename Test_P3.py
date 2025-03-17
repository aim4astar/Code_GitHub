import random
import matplotlib.pyplot as plt

# Generic function to generate a random state for both 8-Queens and 8-Puzzle
def generateRandomState(size, isQueens=True):
    """
    Generate a random initial state for the given problem.
    """
    if isQueens:
        return [random.randint(0, size - 1) for _ in range(size)]
    else:
        state = list(range(size))
        random.shuffle(state)
        return state

# Generic heuristic function for both 8-Queens and 8-Puzzle
def calculateHeuristic(state, goalState=None, isQueens=True):
    """
    Calculate the heuristic cost for a given state.
    """
    if isQueens:
        conflicts = sum(
            state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j)
            for i in range(len(state)) for j in range(i + 1, len(state))
        ) #The sum function iterates over all unique pairs of queens (i, j) and counts conflicts.
        return conflicts
    else:
        return sum(1 for i in range(len(state)) if state[i] != goalState[i] and state[i] != 0) #It counts the number of tiles that are not in their correct position compared to the goal state.

# Generic Hill Climbing Algorithm with Random Restarts
def hillClimb(problem, calculateHeuristic, generateRandomState, getNeighbors, goalState=None, size=None, isQueens=True):

    maxIterations = 1000
    restartCount = 10
    bestCosts = []
   
    for _ in range(restartCount):
        state = generateRandomState(size, isQueens)
        bestCost = calculateHeuristic(state, goalState, isQueens)
        bestCostsRestart = [bestCost]
       
        for _ in range(maxIterations):
            neighbors = getNeighbors(state)  
            bestNeighbor = min(neighbors, key=lambda s: calculateHeuristic(s, goalState, isQueens)) # The lambda function calculates the heuristic for each neighbor, and min() returns the neighbor with the smallest heuristic value.
            newCost = calculateHeuristic(bestNeighbor, goalState, isQueens)
           
            if newCost < bestCost:
                state, bestCost = bestNeighbor, newCost

            bestCostsRestart.append(bestCost)
           
            if bestCost == 0:
                break
       
        bestCosts.extend(bestCostsRestart)
   
    return state, bestCosts

# 8-Queens Neighbors Function
def neighbors8Queens(state):
    """
    Generate all neighboring states by moving one queen per column to a different row.
    """
    neighbors = []
    for col in range(8):
        for row in range(8):
            if state[col] != row:
                newState = state[:]
                newState[col] = row # creating a new neighboring state for the 8-Queens problem.
                neighbors.append(newState)
    return neighbors

# 8-Puzzle Neighbors Function
def neighbors8Puzzle(state):
    """
    Generate all possible neighboring states by moving the blank space (tile 0) in the 8-Puzzle.
    """
    neighbors = []
    zeroPos = state.index(0)
    row, col = divmod(zeroPos, 3)
   
    movesDirection = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for rowChange, colChange in movesDirection:
        newRow, newCol = row + rowChange, col + colChange
        if 0 <= newRow < 3 and 0 <= newCol < 3:
            newZeroPos = newRow * 3 + newCol
            newState = state[:]
            newState[zeroPos], newState[newZeroPos] = newState[newZeroPos], newState[zeroPos] # Moving the blank space to a valid position in the 8-Puzzle.
            neighbors.append(newState)
    return neighbors

# Plotting Function
def plotResults(queenConflictHistory, puzzleMisplacementHistory):
    """
    Plot the results for both the 8-Queens and 8-Puzzle problems.
    """
    plt.figure(figsize=(12, 6))
   
    plt.subplot(1, 2, 1)
    plt.plot(queenConflictHistory, label="8-Queens")
    plt.xlabel("Iteration")
    plt.ylabel("Heuristic Cost (Conflicts)")
    plt.title("8-Queens Hill Climbing with Random Restarts")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(puzzleMisplacementHistory, label="8-Puzzle", color="orange")
    plt.xlabel("Iteration")
    plt.ylabel("Heuristic Cost (Misplaced Tiles)")
    plt.title("8-Puzzle Hill Climbing with Random Restarts")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Solve 8-Queens
finalStateQueens, bestCostsQueens = hillClimb(
    "8-Queens", calculateHeuristic, generateRandomState, neighbors8Queens, size=8, isQueens=True
)
print("8-Queens Final State:", finalStateQueens)
print("8-Queens Final Heuristic Cost:", calculateHeuristic(finalStateQueens, isQueens=True))
   
# Solve 8-Puzzle
goalState8Puzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
finalStatePuzzle, bestCostsPuzzle = hillClimb(
    "8-Puzzle", calculateHeuristic, generateRandomState, neighbors8Puzzle, goalState8Puzzle, size=9, isQueens=False
)
print("8-Puzzle Final State:", finalStatePuzzle)
print("8-Puzzle Final Heuristic Cost:", calculateHeuristic(finalStatePuzzle, goalState8Puzzle, isQueens=False))

# Plot results
plotResults(bestCostsQueens, bestCostsPuzzle)