import math   #for using min, max, math.inf, .....


def print_board(board):
    for i in range(0, 9, 3):
        print(board[i], " | ", board[i + 1], " | ", board[i + 2])
        if i < 6:
            print("--------------")
            

def is_draw(board):
    return all(cell != ' ' for cell in board)       #all() returns a boolean depending on whether ALL the values in the iterable meet the condition (returns True) or not (returns False).


def check_win(board, player):
    win_configurations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_configurations)        #any() returns a boolean depending on whether AT LEAST one of the values in the iterable meets the condition (returns True) or not (returns False)



#5 parameters; The "depth" parameter provides a way to evaluate how soon a win/loss occurs. Quicker wins are preferable for the AI, while delayed losses are preferable for us.
#is_maximizing is a boolean indicating whose turn it is(True for 'X'/Max and False for 'O'/Min)
def minimax(board, depth, is_maximizing, alpha, beta):
    #FIRST, we check for and assign terminal utilities for the three terminal states: X wins, O wins, or it's a draw. In each case, a different terminal utility value will be assigned.
    #This is crucial for the recursion to work properly.
     
    if check_win(board, 'X'):
        return 10 - depth       #higher terminal utility value for winning in few moves

    if check_win (board, 'O'):
        return depth - 10       #higher terminal utility for delaying the win for the opponent (and hoping it leads to our own win)
         
    if is_draw(board):
        return 0                #terminal utility value of 0 for a draw
        
    
    if is_maximizing:
        best_val = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                utility_val = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                best_val = max(best_val, utility_val)
                alpha = max(alpha, best_val)
                if alpha >= beta:
                    break
                
        return best_val
    
    else:
        best_val = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                utility_val = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                best_val = min(best_val, utility_val)
                beta = min(beta, best_val)
                if alpha >= beta:
                    break
        
        return best_val



def best_move(board):
    best_value = -math.inf          #since AI is going first, and thus maximizing its utility, we initialize best_value (initial utility) as - infinity and update it later as we get better values from the minimax algorithm
    move = -1                       #initialize the move(0 - 8) that AI will take once minimax is fully run
    
    for i in range(9):              
        if board[i] == ' ':         #loop will only iterate through the positions that are empty
            board[i] = 'X'          #Putting 'X' in a position, simulating the rest of the game using minimax with the assumption that the opponent plays optimally, and computing the utility values
            utility_value = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = ' '                     #VERY IMPORTANT; once we have run the "simulation" of putting 'X' in a particular position and running the minimax algorithm, we have to clear the board before assigning 'X' to a different
            if utility_value > best_value:     # value and starting a new simulation.
                best_value = utility_value
                move = i
    
    return move
    

def tic_tac_toe():
    board = [' '] * 9       #initialize the playing board
    print("Tic-Tac-Toe: AI('X') vs. Human('O')")
    print_board(board)      #print empty board
    
    
    while(True):
        ai_move = best_move(board)      #returns the best move (0 - 8) for the AI from the current board state
        board[ai_move] = 'X'            #update the board to reflect the move
        print("AI chose position: ", ai_move + 1)
        print_board(board)              #print the board

        if check_win(board, 'X'):       #check whether AI has won, and if it has then break
            print("AI Wins!")
            break
        
        if is_draw(board):              #check whether it's a draw
            print("It's a draw!")
            break


        while(True):
            try:
                human_move = int(input("Enter your move(1 - 9): ")) - 1     #It's the human's turn; take their input, change it to an index on the board
                if 0 <= human_move <= 8 and board[human_move] == ' ':                   
                    board[human_move] = 'O'                                 #update the board with the new move
                    break
                
                else:
                    print("Invalid move. Try again.")
            
            except ValueError:
                print("Invalid input. Try again.")
                
            print_board(board)
            
            if check_win(board, 'O'):    #check whether human has won, and if it has then break
                print("You Win!")
                break
        
            if is_draw(board):           #check whether it's a draw
                print("It's a draw!")
                break


tic_tac_toe()
                
        