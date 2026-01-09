"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state() -> list:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board) -> str:
    """
    Returns player who has the next turn on a board.
    """
    # raise NotImplementedError
    num_X = 0
    num_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                num_X += 1
            elif board[i][j] == O:
                num_O += 1
    if num_X > num_O:
        return O    
    else:
        return X 


def actions(board) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # raise NotImplementedError
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action) -> list:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # 1. Check if the index is out of bounds (0, 1, or 2)
    if i < 0 or i >= 3 or j < 0 or j >= 3:
        raise Exception("Invalid Action: Out of bounds")

    # 2. Check if the cell is already occupied
    if board[i][j] != EMPTY:
        raise Exception("Invalid Action: Position already taken")

    # Make the move
    new_board = copy.deepcopy(board)
    current_player = player(board)
    new_board[i][j] = current_player
    return new_board


def winner(board) -> str:
    """
    Returns the winner of the game, if there is one.
    """
    # raise NotImplementedError
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            if board[i][0] == X:
                return X
            else:
                return O
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] and board[0][j] != EMPTY:
            if board[0][j] == X:
                return X
            else:
                return O
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        if board[0][0] == X:
            return X
        else:
            return O
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        if board[0][2] == X:
            return X
        else:
            return O
    return None


def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    # raise NotImplementedError
    if winner(board) is not None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # raise NotImplementedError
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board) -> tuple:
    """
    Returns the optimal action for the current player on the board.
    """
    # raise NotImplementedError
    if terminal(board):
        return None
    current_player = player(board)
    best_action = None
    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
    return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v