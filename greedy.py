import sys
import ast
import time
from model import *

def score_end(board_representation):
    B_moves, W_moves = possible_moves_gui(board_representation, -1), possible_moves_gui(board_representation, 1)
    if len(B_moves) == 0 and king_in_check(board_representation[0],-1):
        return 99999999999
    if len(W_moves) == 0 and king_in_check(board_representation[0],1):
        return -99999999999
    if board_representation[0].count(".") == 62:
        return 0
    return 0

board_state = ast.literal_eval(sys.argv[1])
player = int(sys.argv[2])

board, state = board_state
piece_value = {"k":999, "q":9, "r":5, "b":3, "n":3, "p":1, ".":0}
moves = possible_moves_gui(board_state, player)
the_move, best = None, -1
best_move = -1
best_score = -99999999999999999
for move in moves:
    new_board = make_move(board_state,move)
    if game_end(new_board):
        score = score_end(new_board)*player
        if score > best_score:
            best_move = move
            break
    B_p = 0
    W_p = 0
    for p in new_board[0]:
        if p == "." or p == "?":
            continue
        elif p.isupper():
            W_p += piece_value[p.lower()]
        else:
            B_p += piece_value[p]
    score = (W_p - B_p)*player
    if score > best_score:
        best_score = score
        best_move = move
    

time.sleep(0.25)
print(best_move)