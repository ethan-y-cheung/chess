import sys
import ast
from model import *

def find_next_move(board_state, token, depth):
    opp = token*-1
    alpha = -9999999999999999999999999999
    beta = 999999999999999999999999999999
    x = possible_moves(board_state, token)
    for move in x:
        newBoard = make_move(board_state, move)
        if king_in_check(newBoard[0],token):
            continue
        result = -negamax(newBoard, opp, depth-1, -beta, -alpha)
        if  result > alpha:
            alpha = result
            best_move = move
    print(best_move,depth)
    return best_move

def score_end(board_representation):
    B_moves, W_moves = possible_moves(board_representation, -1), possible_moves(board_representation, 1)
    if len(B_moves) == 0 and king_in_check(board_representation[0],-1):
        return 99999999999
    if len(W_moves) == 0 and king_in_check(board_representation[0],1):
        return -999999999999
    return 0

def negamax(board_state, token, depth, alpha, beta):
    copy = (board_state[0], board_state[1].copy())
    board, useless = copy
    opp = token*-1
    if depth == 0 or game_end(copy):
        s = score(copy) if token == 1 else -score(copy)
        s = score_end(copy)*token if game_end(copy) else s
        return s
    for move in possible_moves(copy, token):
        newBoard = make_move(copy, move)
        if king_in_check(newBoard[0],token):
            continue
        alpha = max(alpha, -negamax(newBoard, opp, depth-1, -beta, -alpha))
        if alpha >= beta:
            break
    return alpha

piece_value = {"k":999, "q":9, "r":5, "b":3, "n":3, "p":1}
bStartPos = {12:"n", 13:"b", 14:"q", 16:"b", 17:"n", 24:"p", 25:"p"}
wStartPos = {82:"N", 83:"B", 84:"Q", 86:"B", 87:"N", 74:"P", 75:"P"}
def score(board_state):
    board, useless = board_state
    score = 0
    for char in board:
        if char.isalpha():
            if char.isupper():
                score += piece_value[char.lower()]
            else:
                score -= piece_value[char]
    return score


# board = [["r", ".", "b", "q", "k", "b", "r", "."],  #1
#          [".", "p", "p", "p", "p", "p", "p", "p"],  #2
#          ["p", "P", "n", ".", ".", ".", ".", "."],  #3
#          [".", ".", ".", ".", ".", ".", ".", "."],  #4
#          [".", ".", ".", ".", ".", ".", ".", "."],  #5
#          [".", "Q", "P", ".", ".", "P", ".", "."],  #6
#          [".", "P", ".", "P", "P", ".", "P", "P"],  #7
#          ["R", "N", "B", ".", "K", "B", "N", "R"]]  #8
# str_board = list_to_board(board)
# state_board = state_variables(str_board)
# board_representation = (str_board, state_board)

board_state = sys.argv[1]

player = sys.argv[2]
depth = 1
for i in range(100):  # No need to look more spaces into the future than exist at all
    print(find_next_move(ast.literal_eval(board_state), int(player), depth))
    depth += 1
    
    
    # string_board, state_board = (board[0],board[1].copy())
    # moves = sort_capture_moves((string_board, state_board),token)
    # if game_end(board):
    #     score_board = score_end((string_board, state_board))
    # else:
    #     score_board = score((string_board, state_board))
    # if score_board >= b:
    #     return b
    # a = max(a,score_board)
    # moves = sort_capture_moves((string_board, state_board),token)
    # for move in moves:
    #     new_board = make_move((string_board, state_board),move):
    #     if king_in_check(new_board[0],token):
    #         continue
    #     eval = -capture_search(-b,-a)