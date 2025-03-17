import math

def print_board(board):
    for i in range(0, 9, 3):
        print(board[i], " | ", board[i+1], " | ", board[i+2])
        if(i < 6):
            print("-------------")
    print()

def check_winner(board, player):
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)

def is_draw(board):
    return all(cell != ' ' for cell in board)

def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, 'X'):              #Checking for terminal states and assigning utility 
        return 10 - depth                     #  values to them. The recursion stops as soon as any of  
    if check_winner(board, 'O'):              #  these conditions are met, and the corresponding utility
        return depth - 10                     #  value is returned.
    if is_draw(board):
        return 0
    
    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                eval = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                evals = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                min_eval = min(min_eval, evals)
                beta = min(beta, evals)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            move_val = minimax(board, 0, False, -math.inf, math.inf)   #is_maximizing is set to False because once AI picks its move, the next turn is ours (minimizing).
            board[i] = ' '     #Undoing the move (backtracking); Done to reset the board after checking the move
            if move_val > best_val:
                best_val = move_val
                move = i
    return move

def tic_tac_toe():
    board = [' '] * 9       #board is a 1D array with 9 empty strings initially; indexed 0-8
    print("Tic-Tac-Toe: AI (X) vs. Human (O)")
    print_board(board)      #print_board function prints the board, and we keep calling it later to update the board as the players choose a move
    
    while True:
        ai_move = best_move(board)      #AI goes first and selects the "best move"; best move is a single number between 0-8 depending on the number of open positions on the board
        board[ai_move] = 'X'            #board is updated
        print("AI chooses position:", ai_move + 1)  
        print_board(board)              #print board with updated value
        
        if check_winner(board, 'X'):
            print("AI wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        
        while True:
            try:
                human_move = int(input("Enter your move (1-9): ")) - 1
                if 0 <= human_move < 9 and board[human_move] == ' ':
                    board[human_move] = 'O'
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 1 and 9.")
        
        print_board(board)
        
        if check_winner(board, 'O'):
            print("You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break

tic_tac_toe()
