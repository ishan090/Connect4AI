"""
Connect4 Player
"""

import math
import copy

R = "R"
Y = "Y"
EMPTY = None
w = 7
h = 6


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY]*w]*h


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    every = []
    for row in board:
        every += row
    if every.count(Y) < every.count(R):
        return Y
    return R

def inverse(board):
    """
    Returns the inverse of the board.
    """
    inv = [[]]*w
    for i in range(w):
        inv[i] = [board[j][i] for j in range(h)]
    return inv


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()  # set of possible values
    inv = inverse(board)  # inverse of the board. I know realise this may not have been necessary after all
    # look over all the columns, get the position of the first empty spot. add that as a possibility.
    for column in range(len(inv)):
        get_col = h - inv[column].count(EMPTY)
        if get_col < h:
            possible.add((get_col, column))
    return possible



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    turn = player(board)
    # b = [[EMPTY]*3]*3
    b_copy = copy.deepcopy(board)
    if b_copy[action[0]][action[1]] == EMPTY:
        b_copy[action[0]][action[1]] = turn
        return b_copy
    else:
        raise ValueError("action is not valid")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    to_compare = []
    for i in range(3):
        to_compare.append(board[i])
        to_compare.append([board[j][i] for j in range(3)])
    to_compare.append([board[0][0], board[1][1], board[2][2]])
    to_compare.append([board[0][2], board[1][1], board[2][0]])
    for row in to_compare:
        if all(row[0] == k for k in row):
            return row[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        # print("terminating board: w :", board)
        return True
    for i in board:
        for j in i:
            if j is None:
                return False
    # print("terminating board: nw :", board)
    return True


def utility(board):
    """
    Returns 1 if R has won the game, -1 if Y has won, 0 otherwise.
    """
    util_dict = {"R": 1, "Y": -1, None: 0}
    return util_dict[winner(board)]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    to_play = player(board)
    to_play = to_play == "R"
    if to_play:
        best = None
        best_val = -1e10
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best = action
    else:
        best = None
        best_val = 1e10
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best = action
    return best


def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = +1e10
        for action in actions(board):
            v = min(max_value(result(board, action)), v)
        return v

def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -1e10
        for action in actions(board):
            v = max(min_value(result(board, action)), v)
        return v

