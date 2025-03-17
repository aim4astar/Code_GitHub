"Implementing a tic-tac-toe game where the AI plays first, followed by input from the user. The AI uses the Minimax algorithm with Alpha-Beta pruning to compute the best"
"next move, with the assumption that the user is playing optimally."

import math


def print_board(board):
    for i in range(0, 9, 3):
        print(board[i], " | ", board[i + 1], " | ", board[i + 2])
        if i < 6:
            print("-------------")


def check_winner(board, player):
    win_configurations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    return any(board[i] == board[j] == board[k] == player for i, j, k in win_configurations)

def is_draw(board):
    return all(board[i] != ' ' for i in range(9))


def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, 'X'):
        return 10 - depth
    
    if check_winner(board, 'O'):
        return depth - 10
    
    if is_draw(board):
        return 0
    
    if is_maximizing:
        best_utility = -math.inf
        for i in range(9):
            if(board[i] == ' '):
                board[i] = 'X'
                utility = minimax(board, depth + 1, False, alpha, beta)
                board[i] = ' '
                best_utility = max(best_utility, utility)
                alpha = max(alpha, best_utility)
                if (alpha >= beta):
                    break
        return best_utility
    else:
        best_utility = math.inf
        for i in range(9):
            if(board[i] == ' '):
                board[i] = 'O'
                utility = minimax(board, depth + 1, True, alpha, beta)
                board[i] = ' '
                best_utility = min(best_utility, utility)
                beta = min(beta, best_utility)
                if (alpha >= beta):
                    break
        return best_utility


def best_move(board):
    best_val = -math.inf
    move = -1
    for i in range(9):
        if(board[i] == ' '):
            board[i] = 'X'
            utility_val = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = ' '
            if utility_val > best_val: 
                best_val = utility_val
                move = i

    return move


def tic_tac_toe():
    board = [' '] * 9
    print("Tic-Tac-Toe: AI('X') vs. Human('O')")
    print_board(board)

    while(True):
        ai_move = best_move(board)
        board[ai_move] = 'X'
        print("AI chose position: ", ai_move + 1)
        print_board(board)

        if check_winner(board, 'X'):
            print("AI Wins!")
            break
        
        if is_draw(board):
            print("It's a Draw!")
            break
        
        while(True):
            try:
                human_move = int(input("Enter your move (1 - 9): ")) - 1
                if(0 <= human_move <= 8 and board[human_move] == ' '):
                    board[human_move] = 'O'
                    break
                else:
                    print("Invalid Move! Try again.")
            except ValueError:
                print("Invalid input! Try again.")


            if check_winner(board, 'O'):
                print("You Win!")
                break
        
            if is_draw(board):
                print("It's a Draw!")
                break
        
            

tic_tac_toe()