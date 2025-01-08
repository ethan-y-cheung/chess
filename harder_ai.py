import sys
import ast
from model import *
import threading

pieceDict = {"K":"♔", "k":"♚", "Q":"♕", "q":"♛", "R":"♖", "r":"♜", "B":"♗", "b":"♝", "N":"♘", "n":"♞", "P":"♙", "p":"♟", ".":".", "?":""}
def list_to_board(listboard):
    full_string = "??????????"
    for i in listboard:
        row = "?"
        for j in i:
            row += j
        row += "?"
        full_string += row
    full_string += "??????????"
    return full_string


def print_board(string):
    rowString = ""
    for index, s in enumerate(string):
        rowString += " " + pieceDict[s]
        if (index+1)%10 == 0:
            print(rowString)
            rowString = ""

def score_end(board_representation):
    B_moves, W_moves = possible_moves(board_representation, -1), possible_moves(board_representation, 1)
    if len(B_moves) == 0 and king_in_check(board_representation[0],-1):
        return 99999999999
    if len(W_moves) == 0 and king_in_check(board_representation[0],1):
        return -99999999999
    if board_representation[0].count(".") == 62:
        return 0
    return 0


piece_value = {"k":99999, "q":900, "r":500, "b":340, "n":325, "p":100}
scoreMemo = dict()

piece_value = {"k":99999, "q":900, "r":500, "b":340, "n":325, "p":100}
pawn_table = [0,  0,  0,  0,  0,  0,  0,  0,
              50, 50, 50, 50, 50, 50, 50, 50,
              10, 10, 20, 30, 30, 20, 10, 10,
              5,  5, 10, 25, 25, 10,  5,  5,
              0,  0,  0, 20, 20,  0,  0,  0,
              5, -5,-10,  0,  0,-10, -5,  5,
              5, 10, 10,-20,-20, 10, 10,  5,
              0,  0,  0,  0,  0,  0,  0,  0]
knight_table = [-50,-40,-30,-30,-30,-30,-40,-50,
                -40,-20,  0,  0,  0,  0,-20,-40,
                -30,  0, 10, 15, 15, 10,  0,-30,
                -30,  5, 15, 20, 20, 15,  5,-30,
                -30,  0, 15, 20, 20, 15,  0,-30,
                -30,  5, 10, 15, 15, 10,  5,-30,
                -40,-20,  0,  5,  5,  0,-20,-40,
                -50,-40,-30,-30,-30,-30,-40,-50]
bishop_table = [-20,-10,-10,-10,-10,-10,-10,-20,
                -10,  0,  0,  0,  0,  0,  0,-10,
                -10,  0,  5, 10, 10,  5,  0,-10,
                -10,  5,  5, 10, 10,  5,  5,-10,
                -10,  0, 10, 10, 10, 10,  0,-10,
                -10, 10, 10, 10, 10, 10, 10,-10,
                -10,  5,  0,  0,  0,  0,  5,-10,
                -20,-10,-10,-10,-10,-10,-10,-20]
rook_table = [   0,  0,  0,  0,  0,  0,  0,  0,
                 5, 10, 10, 10, 10, 10, 10,  5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                -5,  0,  0,  0,  0,  0,  0, -5,
                0,  0,  0,  5,  5,  0,  0,  0]
queen_table = [-20,-10,-10, -5, -5,-10,-10,-20,
               -10,  0,  0,  0,  0,  0,  0,-10,
               -10,  0,  5,  5,  5,  5,  0,-10,
                -5,  0,  5,  5,  5,  5,  0, -5,
                 0,  0,  5,  5,  5,  5,  0, -5,
               -10,  5,  5,  5,  5,  5,  0,-10,
               -10,  0,  5,  0,  0,  0,  0,-10,
               -20,-10,-10, -5, -5,-10,-10,-20]
king_table = [  -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20]

scoreMemo = dict()
def score(board_state):
    board, state = board_state
    if board in scoreMemo:
        return scoreMemo[board]
    
    if game_end(board_state):
        return score_end(board_state)
    

    score = 0
    w_king = board.find("K")
    b_king = board.find("k")
    w_fileDict = dict()
    b_fileDict = dict()
    w_b_count = 0
    b_b_count = 0
    w_r_files = []
    b_r_files = []
    convert_to_8x8 = lambda row, col: (row-1)*8 + col-1

    for index, char in enumerate(board):
        if not char.isalpha():
            continue
        row = index//10
        col = index%10
        index8x8 = convert_to_8x8(row, col)
        if char.isupper():
            score += piece_value[char.lower()]
            if char == "P":
                score += pawn_table[index8x8]
                #Stacked Pawns
                if col in w_fileDict:
                    score -= 7
                    w_fileDict[col] = 7
                else:
                    w_fileDict[col] = row
                    #Enemy in front
                    if (c:=board[index-10]) != "." and c.islower():
                        score -= (7-row)**2
            #Bishop
            elif char == "B":
                score += bishop_table[index8x8]
                w_b_count += 1
                if board[index-11].lower() == "p":
                    score -= 10
                if board[index-9].lower() == "p":
                    score -= 10
            #Rook
            elif char == "R":
                score += rook_table[index8x8]
                if col in w_r_files:
                    score += 15
                w_r_files.append(col)
                #Dist. to enemy king
                distance = ((row-b_king//10)**2 + (col-(b_king%10))**2)**0.5
                score -= distance*0.7
            #Knight
            elif char == "N":
                score += knight_table[index8x8]
                dist_to_center = ((row-4.5)**2 + (col-4.5)**2)**0.5
                score -= dist_to_center*5
            #Queen (COULD ALSO ADD FOR SAME DIAGONAL AS BISHOP BUT VERY NEGLIGIBLE)
            elif char == "Q":
                score += queen_table[index8x8]
                distance = ((row-b_king//10)**2 + (col-(b_king%10))**2)**0.5
                score -= distance*0.7
            #King
            else:
                score += king_table[index8x8]
                if state[index][3]: #Castled
                    score += 70
                elif index != 85:
                    score -= 30
        else:
            score -= piece_value[char]
            if char == "p":
                score -= pawn_table[::-1][index8x8]
                #Stacked Pawns
                if col in b_fileDict:
                    score += 7
                    b_fileDict[col] = 2
                else:
                    b_fileDict[col] = row
                    #Enemy in front
                    if (c:=board[index+10]) != "." and c.isupper():
                        score += (row-2)**2
            #Bishop
            elif char == "b":
                score -= bishop_table[::-1][index8x8]
                b_b_count += 1
                if board[index+11].lower() == "p":
                    score += 10
                if board[index+9].lower() == "p":
                    score += 10
            #Rook
            elif char == "r":
                score -= rook_table[::-1][index8x8]
                if col in b_r_files:
                    score -= 15
                b_r_files.append(col)
                #Dist. to enemy king
                distance = ((row-w_king//10)**2 + (col-(w_king%10))**2)**0.5
                score += distance*0.7
            #Knight
            elif char == "n":
                score -= knight_table[::-1][index8x8]
                dist_to_center = ((row-4.5)**2 + (col-4.5)**2)**0.5
                score += dist_to_center*3
            #Queen
            elif char == "q":
                score -= queen_table[::-1][index8x8]
                distance = ((row-w_king//10)**2 + (col-(w_king%10))**2)**0.5
                score += distance*0.7
            #King
            else:
                score -= king_table[::-1][index8x8]
                if state[index][3]: #Castled
                    score -= 70
                elif index != 15:
                    score += 30

    #Bishop Presence
    if w_b_count > 1:
        score += 40
    if b_b_count > 1:
        score -= 40
    #Rook Conditions
    for col in w_r_files:
        if not (col in w_fileDict or col in b_fileDict):
            score += 10
        elif col in b_fileDict:
            score += 3
    for col in b_r_files:
        if not (col in w_fileDict or col in b_fileDict):
            score -= 10
        elif col in w_fileDict:
            score -= 3
    #Isolated Pawns
    for col in w_fileDict:
        row = w_fileDict[col]
        if not (col+1 in w_fileDict and col-1 not in w_fileDict):
            score -= 2
        else:
            score += (7-row)**1.5
            if col not in [1, 8]:
                if board.count(".") < 54:
                    score += (7-row)**2
                score += (7-row)**1.5
    for col in b_fileDict:
        row = b_fileDict[col]
        if not (col+1 in b_fileDict and col-1 not in b_fileDict):
            score += 2
        else:
            score -= (row-2)**2
            if col not in [1, 8]:
                if board.count(".") < 54:
                    score -= (row-2)**2
                score -= (row-2)**1.5

    if len(state[b_king][1]) != 0 and len(state[w_king][1]) != 0:
        if score > 888:
            score += 300*(1/len(state[b_king][1]))
            king_distance = ((w_king//10-b_king//10)**2 + (w_king%10-b_king%10)**2)**0.5
            score += 200/king_distance
        elif score < -888:
            score -= 300/len(state[w_king][1])
            king_distance = ((w_king//10-b_king//10)**2 + (w_king%10-b_king%10)**2)**0.5
            score -= 200/king_distance
    
    scoreMemo[board] = score
    return score

def score_queen_end_game(board,token):
    score = 0
    op_possible_moves = possible_moves(board,token*-1)
    score += -100 if king_in_check(board[0],token*-1) else 0
    if len(op_possible_moves) != 2:
        score += (1/len(op_possible_moves))*20
    if len(op_possible_moves) == 2:
        score += 2000
        op_k = board[0].find("Q") if token == 1 else board[0].find("q")
        k = board[0].find("K") if token == 1 else board[0].find("k")
        distance = ((k%10 - op_k%10)**2 + (k//10 - op_k//10)**2)**0.5
        score += (1/distance)*20
        if game_end(board):
            score = 0
    return score*200000

x_squares = [22,27,77,72]
Move_table = {}
transposition_table = {}
orderMoves_table = {}  
killer_moves = set()
prev_moves = {}
DEPTH = 0


def order_move_scoring(move, board, key, prev_move):
    global best_move
    score = 0
    if prev_move != None and move[2] == prev_move[2]:
        score += 1000000
    if board[0][move[2]] != ".":
        score += piece_value[board[0][move[2]].lower()]
        score -= piece_value[board[0][move[1]].lower()]
    if  key in transposition_table and move == transposition_table[key]["best move"]:
        score += 1000
    if move in killer_moves:
        score += 50
    if move == best_move:
        score += 100000000
    return score

def orderMoves(board, token, prev_move):
    key = (board[0],str(board[1]))
    my_moves = possible_moves(board, token)
    my_moves_dict = {i: order_move_scoring(i,board,key, prev_move) for i in my_moves}
    my_sorted_moves = dict(sorted(my_moves_dict.items(), key=lambda item: item[1], reverse=True))
    return list(my_sorted_moves)


def capture_search(board,a,b,token,depth,last_move):
    string_board, state_board = (board[0],board[1])
    board_key = (string_board,str(state_board))
    
    if depth == 0:
        returning_value = token*score((string_board, state_board))
        return returning_value
    
    ply = ply0DrawMoves if token == ply0 else ply1DrawMoves
    if string_board in ply:
        returning_value = -contempt_factor
        if returning_value <= a:
            flag = "lowerbound"
        elif returning_value >= b:
            flag = "upperbound"
        else:
            flag = "exact"
        transposition_table[board_key] = {"value": returning_value, "depth": depth, "flag": flag}
        return returning_value   
    
    moves = orderMoves((string_board, state_board), token, last_move)[0:1]

    best_value = None
    
    for move in moves:
        if string_board[move[2]] == ".":
            continue
        new_board = make_move((string_board, state_board),move)
        if king_in_check(new_board[0],token):
            continue
        best_value = -capture_search(new_board,a,b,token*-1,depth-1, move)

    if best_value == None:
        returning_value = token*score((string_board, state_board))
        return returning_value    
    return best_value

ply0DrawMoves = set()
ply1DrawMoves = set()
contempt_factor = 650
def pvs(board, depth, token, a, b, f, first_depth, prev_move):
    string_board, state_board = (board[0],board[1])
    board_key = (string_board,str(state_board))
    queen = "Q" if token == 1 else "q"
    
    ply = ply0DrawMoves if token == ply0 else ply1DrawMoves
    if string_board in ply:
        returning_value = -contempt_factor
        if returning_value <= a:
            flag = "lowerbound"
        elif returning_value >= b:
            flag = "upperbound"
        else:
            flag = "exact"
        transposition_table[board_key] = {"value": returning_value, "depth": depth, "flag": flag, "best move":-1}
        return returning_value   
    
    if depth == 0 or game_end(board):
        returning_value = token*score(board)#capture_search(board,a,b,token,0,prev_move)
        if returning_value <= a:
            flag = "lowerbound"
        elif returning_value >= b:
            flag = "upperbound"
        else:
            flag = "exact"
        transposition_table[board_key] = {"value": returning_value, "depth": depth, "flag": flag, "best move":-1}
        return returning_value
   
    if board_key in transposition_table and depth != first_depth:
        entry = transposition_table[board_key]
        if entry["depth"] >= depth:
            if entry["flag"] == "exact":
                return entry["value"]
            elif entry["flag"] == "lowerbound":
                a = max(a, entry["value"])
            elif entry["flag"] == "upperbound":
                b = min(b, entry["value"])
            if a >= b:
                return entry["value"]
            
    children = orderMoves((string_board,state_board),token,prev_move)
    value = float('-inf')
    best_move = -1
    for moves in children:
        boards = make_move(board,moves)
        if king_in_check(boards[0],token):
            continue
        if f == "ab":
            prev_val = value
            value = max(value,-pvs(boards,depth-1,-token,-b,-a,"ab",first_depth,moves))
            if value != prev_val:
                best_move = moves
        else:
            prev_val = value
            value = max(value,-pvs(boards,depth-1,-token,-a-1,-a,"zw",first_depth,moves))
            if value != prev_val:
                best_move = moves
            if a < value < b:
                prev_val = value
                value = max(value,-pvs(boards,depth-1,-token,-b,-a,"ab",first_depth,moves))
                if value != prev_val:
                    best_move = moves
        a = max(a,value)
        if a >= b:
            killer_moves.add(moves)
            break
    if value <= a:
        flag = "lowerbound"
    elif value >= b:
        flag = "upperbound"
    else:
        flag = "exact"
    transposition_table[board_key] = {"value": value, "depth": depth, "flag": flag, "best move":best_move}
    return a

best_move = -1
eval_better_moves = []
def find_next_move(board,token,depth):
    global best_move
    
    token_key = token
    global prev_moves
    string_board, state_board = (board[0], board[1])
    if best_move == -1:
        allMoves = orderMoves((string_board,state_board),token, None)
        for move in allMoves:
            make = make_move((string_board,state_board),move)
            if not king_in_check(make[0],token):
                firstMove = move
                break
    else:
        firstMove = best_move
        allMoves = orderMoves((string_board,state_board),token,None) #possible_moves((string_board,state_board),token)#
       
    alpha = -9999999999999999999999999999999999999999999
    beta = 999999999999999999999999999999999999999999999
    all_evals = {}
   
    #eval_previous_variation
    bestMove = firstMove
    bestEval = -pvs((k:=make_move(board,firstMove)),depth-1,-token_key, -beta,-alpha,"ab",depth-1,firstMove)
    alpha = max(alpha,bestEval)
    all_evals[bestMove] = bestEval
    if alpha >= beta:
        return bestMove
   
    #rest of moves
    for move in allMoves:
        if move == firstMove:
            continue
        new_board = make_move(board,move)         
        if king_in_check(new_board[0],token):
            continue
        if new_board[0] in ply0DrawMoves:
            evalMove = 0
            if (evalMove-contempt_factor) > bestEval:
                bestEval = evalMove
                best_move = move
        else:
            evalMove = -pvs(new_board,depth-1,-token_key, -alpha-1,-alpha,"zw",depth-1,move)
            if alpha < evalMove < beta:
                evalMove = -pvs(new_board,depth-1,-token_key, -beta,-alpha,"ab",depth-1,move)
                if evalMove > bestEval:
                    bestMove = move
                    bestEval = evalMove
        all_evals[move] = evalMove
        alpha = max(alpha, evalMove)
        
    print(bestMove,bestEval,depth)
    best_move = bestMove
    return bestMove


ply0 = 1
# board=[["r", "n", "b", "q", "k", "b", "n", "r"],  #1
#         ["p", "p", "p", "p", "p", "p", "p", "p"],  #2
#         [".", ".", ".", ".", ".", ".", ".", "."],  #3
#         [".", ".", ".", ".", ".", ".", ".", "."],  #4
#         [".", ".", ".", ".", ".", ".", ".", "."],  #5
#         [".", ".", ".", ".", ".", ".", ".", "."],  #6
#         ["P", "P", "P", "P", "P", "P", "P", "P"],  #7
#         ["R", "N", "B", "Q", "K", "B", "N", "R"]]  #8
str_board = conver_fen_to_board("rn1qkbnr/pp2pppp/2p5/5b2/2p5/P3P3/1P1PBPPP/RNBQK1NR")
state_board = state_variables(str_board)
board_representation = (str_board, state_board)
from time import perf_counter
start = perf_counter()
for i in range(1,5):
    print(find_next_move(board_representation,1,i))
print(perf_counter()-start)

# board_state = ast.literal_eval(sys.argv[1])
# player = int(sys.argv[2])
# prev_moves = ast.literal_eval(sys.argv[3])
# board = board_state

# ply0_moves = possible_moves(board, player)
# for move in ply0_moves:
#     new_board = make_move(board,move)
#     if king_in_check(new_board[0], player):
#         continue
#     if new_board[0] in prev_moves:
#         ply0DrawMoves.add(new_board[0])
#     new_new_board = (new_board[0], new_board[1].copy())
#     ply1_moves = possible_moves(new_new_board, player*-1)
#     for new_moves in ply1_moves:
#         new_board2 = make_move(new_new_board, new_moves)
#         if king_in_check(new_board2[0], player*-1):
#             continue
#         if new_board2[0] in prev_moves:
#             ply1DrawMoves.add(new_board2[0])

# ply0 = player  
# depth = 1
# board, state_var = board_state
# for i in range(100):
#     print(find_next_move((board,state_var), player, depth))
#     depth += 1

