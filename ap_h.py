import sys
import ast
from model import *

piece_value = {"k":999, "q":9, "r":5, "b":3, "n":3, "p":1}
def score(board_state):
    board, state = board_state
    score = 0
    W_king = board.find("K")
    B_king = board.find("k")
    W_fileDict = dict()
    B_fileDict = dict()
    W_b_count = 0
    B_b_count = 0
    W_r_files = []
    B_r_files = []
    for index, char in enumerate(board):
        if not char.isalpha():
            continue
        row = index//10
        col = index%10
        if char.isupper():
            score += piece_value[char.lower()]
            if char == "P":
                #Stacked Pawns
                if col in W_fileDict:
                    score -= 7
                    W_fileDict[col] = 7
            #Bishop
            elif char == "B":
                W_b_count += 1
                if board[index-11].lower() == "p":
                    score -= 10
                if board[index-9].lower() == "p":
                    score -= 10
            #Rook
            elif char == "R":
                if col in W_r_files:
                    score += 15
                W_r_files.append(col)
                #Dist. to enemy king
                distance = ((row-B_king//10)**2 + (col-(B_king%10))**2)**0.5
                score -= distance*0.7
            #Knight (COULD ADD DISTANCE TO ENEMY KING BUT IDK)
            elif char == "N":
                dist_to_center = ((row-4.5)**2 + (col-4.5)**2)**0.5
                score -= dist_to_center*5
            #Queen (COULD ALSO ADD FOR SAME DIAGONAL AS BISHOP BUT VERY NEGLIGIBLE)
            elif char == "Q":
                distance = ((row-B_king//10)**2 + (col-(B_king%10))**2)**0.5
                score -= distance*0.7
        else:
            score -= piece_value[char]
            if char == "p":
                #Stacked Pawns
                if col in B_fileDict:
                    score += 7
                    B_fileDict[col] = 2
            #Bishop
            elif char == "b":
                B_b_count += 1
                if board[index+11].lower() == "p":
                    score += 10
                if board[index+9].lower() == "p":
                    score += 10
            #Rook
            elif char == "r":
                if col in B_r_files:
                    score -= 15
                B_r_files.append(col)
                #Dist. to enemy king
                distance = ((row-W_king//10)**2 + (col-(W_king%10))**2)**0.5
                score += distance*0.7
            #Knight
            elif char == "n":
                dist_to_center = ((row-4.5)**2 + (col-4.5)**2)**0.5
                score += dist_to_center*3
            #Queen
            elif char == "q":
                distance = ((row-W_king//10)**2 + (col-(W_king%10))**2)**0.5
                score += distance*0.7

    #Bishop Presence
    if W_b_count > 1:
        score += 40
    if B_b_count > 1:
        score -= 40
    #Rook Conditions
    for col in W_r_files:
        if not (col in W_fileDict or col in B_fileDict):
            score += 10
        elif col in B_fileDict:
            score += 3
    for col in B_r_files:
        if not (col in W_fileDict or col in B_fileDict):
            score -= 10
        elif col in W_fileDict:
            score -= 3
    for col in B_fileDict:
        row = B_fileDict[col]
        if not (col+1 in B_fileDict and col-1 not in B_fileDict):
            score += 2
        else:
            score -= (row-2)**2
            if col not in [1, 8]:
                if board.count(".") < 54:
                    score -= (row-2)**2
                score -= (row-2)**1.5
    return score


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


board_state = sys.argv[1]

player = sys.argv[2]
depth = 1
for i in range(100):  # No need to look more spaces into the future than exist at all
    print(find_next_move(ast.literal_eval(board_state), int(player), depth))
    depth += 1