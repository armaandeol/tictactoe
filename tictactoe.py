"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
                
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    
    # Check if action is valid
    if i not in range(3) or j not in range(3) or board[i][j] != EMPTY:
        raise Exception("Invalid action")
    
    # Create a deep copy of the board
    import copy
    new_board = copy.deepcopy(board)
    
    # Make the move
    new_board[i][j] = player(board)
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] is not EMPTY:
            return board[0][j]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    # No winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there's a winner
    if winner(board) is not None:
        return True
    
    # Check if the board is full
    for row in board:
        if EMPTY in row:
            return False
    
    # Board is full with no winner
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If the board is terminal, return None
    if terminal(board):
        return None
    
    current_player = player(board)
    
    # Helper functions with alpha-beta pruning
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            if v >= beta:  # Pruning
                return v
            alpha = max(alpha, v)
        return v
    
    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            if v <= alpha:  # Pruning
                return v
            beta = min(beta, v)
        return v
    
    # Find the optimal action
    if current_player == X:
        # X wants to maximize
        best_value = float('-inf')
        best_action = None
        
        for action in actions(board):
            value = min_value(result(board, action), float('-inf'), float('inf'))
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    else:
        # O wants to minimize
        best_value = float('inf')
        best_action = None
        
        for action in actions(board):
            value = max_value(result(board, action), float('-inf'), float('inf'))
            if value < best_value:
                best_value = value
                best_action = action
        
        return best_action
