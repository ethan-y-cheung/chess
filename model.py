pieceDict = {"K":"♔", "k":"♚", "Q":"♕", "q":"♛", "R":"♖", "r":"♜", "B":"♗", "b":"♝", "N":"♘", "n":"♞", "P":"♙", "p":"♟", ".":".", "?":""}


def conver_fen_to_board(fen):
    board = "??????????"
    row = ""
    for index,char in enumerate(fen):
        if char in "12345678":
            for i in range(int(char)):
                row += "."
        elif char == "/":
            board += "?" + row + "?"
            row = ""
        elif index == len(fen)-1:
            row += char
            final_ = 8-len(row)
            for i in range(final_):
                row += "."
            board += "?" + row + "?"
            row = ""   
        else:
            row += char
        # print(board)
        # input()
    board += "??????????"
    return board    

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

#Possible Moves
def knight_moves(index, piece, board, token):
    directions = [12, 8, 19, 21, -12, -8, -19, -21]  
    moves = []
    for dir in directions:
        new_move = index + dir
        if new_move >= 0 and new_move < 100 and board[new_move] != "?":
            new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
            if board[new_move] == ".":
                new_token = 0
            moves.append((piece, index, new_move)) if token != new_token else None
    return moves

def rook_moves(index, piece, board, token):
    directions = [1, 10, -1, -10]
    moves = []
    for dir in directions:
        new_move = index + dir
        while board[new_move] == ".":
            moves.append((piece, index, new_move)) if board[new_move] != "?" else None
            new_move += dir
        new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
        moves.append((piece, index, new_move)) if board[new_move] != "?" and token != new_token else None
    return moves

def bishop_moves(index, piece, board, token):
    directions = [9, 11, -9, -11]
    moves = []
    for dir in directions:
        new_move = index + dir
        while board[new_move] == ".":
            moves.append((piece, index, new_move)) if board[new_move] != "?" else None
            new_move += + dir
        new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
        moves.append((piece, index, new_move)) if board[new_move] != "?" and token != new_token else None
    return moves

def queen_moves(index, piece, board, token):
    directions = [9, 11, -9, -11, 1, 10, -1, -10]
    moves = []
    for dir in directions:
        new_move = index + dir
        while board[new_move] == ".":
            moves.append((piece, index, new_move)) if board[new_move] != "?" else None
            new_move += + dir
        new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
        moves.append((piece, index, new_move)) if board[new_move] != "?" and token != new_token else None
    return moves
     
def is_attacked(board, token, index):
    color = lambda x: (x.lower() if token == 1 else x.upper())
    b, r, n, p, k = color("b"), color("r"), color("n"), color("p"), color("k")
    pawn_dir = {9:p, 11:p, -9:p, -11:p}
    directions = {9:b, 11:b, -9:b, -11:b, 1:r, 10:r, -1:r, -10:r}
    knight_dir = {12:n, 8:n, 19:n, 21:n, -12:n, -8:n, -19:n, -21:n}
    king_dir = {1:k, -1:k, 10:k, -10:k}
    attack_score = 0
    for dir in directions:
        new_index = index + dir
        while board[new_index] == ".":
            new_index += dir
        if board[new_index] != "?" and (board[new_index] == directions[dir] or board[new_index] == color("q")):
            attack_score += 1
    for dir in knight_dir:
        new_index = index + dir
        if new_index < 100 and new_index >= 0 and board[new_index] == knight_dir[dir]:
            attack_score += 1
    for dir in pawn_dir:
        new_index = index + dir
        if board[new_index] == pawn_dir[dir]:
            attack_score += 1
    for dir in king_dir:
        new_index = index + dir
        if board[new_index] == king_dir[dir]:
            attack_score += 1
    return attack_score
 
def king_moves(index, piece, board, token, king_moves, queen_rook_moves, king_rook_moves): #-1 if there is no king rook or -1 if there is no queen rook
    directions = [9, 11, -9, -11, 1, 10, -1, -10]
    moves = []
    rook_color = "K" if token == 1 else "k"
    for dir in directions:
        new_move = index + dir
        new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
        new_token = 0 if board[new_move] == "." else new_token
        moves.append((piece, index, new_move)) if board[new_move] != "?" and token != new_token else None

    expected_rook_index = 81 if token == 1 else 11
    expected_king_index = 85 if token == 1 else 15
    if  expected_king_index == index and king_moves == 0 and board[expected_rook_index].lower() == "r" and queen_rook_moves == 0:
        new_move = index - 1
        while board[new_move] == ".":
            if is_attacked(board,token,new_move) != 0:
                break
            new_move -= 1
        if new_move in [88, 81, 11, 18] and king_in_check(board, token) == False:
            castle_move = 83 if piece == "K" else 13
            moves.append((piece + "ooo", index, castle_move))
            
    expected_rook_index = 88 if token == 1 else 18
    if king_moves == 0  and board[expected_rook_index].lower() == "r" and king_rook_moves == 0:
        new_move = index + 1
        while board[new_move] == ".":
            if is_attacked(board,token,new_move) != 0:
                break
            new_move += 1
        if new_move in [88, 81, 11, 18] and king_in_check(board, token) == False:
            castle_move = 87 if piece == "K" else 17
            moves.append((piece + "oo", index, castle_move))

    return moves  

def pawn_moves(index, piece, board, token):
    directions = [-9*token, -10*token, -11*token]
    ogFile, promotion = (range(21, 29), range(81, 89)) if token == -1 else (range(71, 79), range(11, 19))
    color = lambda x: (x.lower() if token == -1 else x.upper())
    moves = []
    for dir in directions:
        new_move = index + dir
        new_token = -1 if board[new_move].isalpha() and board[new_move].islower() else 1
        new_token = 0 if board[new_move] == "." else new_token
        if abs(dir) in [9, 11]:
            if board[new_move] not in ["?","."] and token != new_token:
                if new_move in promotion:
                    for p in "qnrb":
                        moves.append((color(p), index, new_move))
                else:
                    moves.append((piece, index, new_move))
        elif board[new_move] == ".":
            if new_move in promotion:
                for p in "qnrb":
                    moves.append((color(p), index, new_move))
            else:
                moves.append((piece, index, new_move))
    if index in ogFile and board[index+(-20*token)] == "." and board[index+(-10*token)] == ".":
        moves.append((piece, index, index+(-20*token)))
    return moves

def king_in_check(board, token):
    color = lambda x: (x.lower() if token == 1 else x.upper())
    b, r, n, p, k = color("b"), color("r"), color("n"), color("p"), color("k")
    
    pawn_dir = {9:p, 11:p} if token == -1 else {-9:p, -11:p}
    directions = {9:b, 11:b, -9:b, -11:b, 1:r, 10:r, -1:r, -10:r}
    knight_dir = {12:n, 8:n, 19:n, 21:n, -12:n, -8:n, -19:n, -21:n}
    king_dir = {9:k, 11:k, -9:k, -11:k, 1:k, 10:k, -1:k, -10:k}
    king_index = board.find("k" if token == -1 else "K")
    
    for dir in directions:
        new_index = king_index + dir
        while board[new_index] == ".":
            new_index += dir
        if board[new_index] != "?" and (board[new_index] == directions[dir] or board[new_index] == color("q")):
            return True  
    for dir in knight_dir:
        new_index = king_index + dir
        if new_index < 100 and new_index >= 0 and board[new_index] == knight_dir[dir]:
            return True
    for dir in pawn_dir:
        new_index = king_index + dir
        if board[new_index] == pawn_dir[dir]:
            return True
    for dir in king_dir:
        new_index = king_index + dir
        if board[new_index] == king_dir[dir]:
            return True
    return False
     
memo = dict()

def possible_moves_gui(board_state_board, token):
    token_side = lambda x: (1 if x.isupper() else -1)
    board, state_board = board_state_board
    if (board, token) in memo:
        return memo[(board, token)]
    possible_moves = []
    for i in state_board:
        if token_side(board[i]) == token:
            moves = state_board[i][1]
            new_moves = []
            for move in moves:
                if not king_in_check(quick_make_move(board_state_board, move)[0], token):
                    new_moves.append(move)
            possible_moves += new_moves
    memo[(board, token)] = possible_moves 
    return  possible_moves

def possible_moves(board_state_board, token):
    token_side = lambda x: (1 if x.isupper() else -1)
    board, state_board = board_state_board
    if (board, token) in memo:
        return memo[(board, token)]
    possible_moves = []
    for i in state_board:
        if token_side(board[i]) == token:
            possible_moves += state_board[i][1]
    memo[(board, token)] = possible_moves 
    return  possible_moves 

def beginning_state_moves(piece_info, board, token):
    piece,index = piece_info[0], piece_info[1]
    color = lambda x: (x.lower() if token == -1 else x.upper())
    
    if piece.lower() == "k":
        return king_moves(index, piece, board, token, 0, 0, 0)
    elif piece.lower() == "p":
        return pawn_moves(index, piece, board, token)
    elif piece.lower() == "n":
        return knight_moves(index, piece, board, token)
    elif piece.lower() == "b":
        return bishop_moves(index, piece, board, token)
    elif piece.lower() == "r":
        return rook_moves(index, piece, board, token)
    elif piece.lower() == "q":
        return queen_moves(index, piece, board, token)
        
    
def state_variables(board):
    states = {}
    for index, piece in enumerate(board):
        if piece in [".","?"]:
            continue
        
        token = 1 if piece.isupper() else -1
        piece_moves = beginning_state_moves((piece,index), board, token)

        if piece.lower() == "k":
            states[index] = (piece, piece_moves, 0, False) # piece,the moves that piece has avalible, how many times it has moved, has castled
        elif piece.lower() == "p":
            states[index] = (piece, piece_moves, 0, True) # amount of times it has moved and can it unpasunt
        elif piece.lower() == "r":
            states[index] = (piece, piece_moves, 0)
        else:
            states[index] = (piece, piece_moves)
    return states

def recalculation_indices(board, move):
    indices_for_recalculation = [board.find("k"), board.find("K")]
    areas = [move[1], move[2]]
    piece = move[0]
    token = 1 if move[0][0].isupper() else -1
    if "o" in piece:
        if piece[1:] == "oo":
            areas += ([88, 86] if token == 1 else [18, 16])
        else:
            areas += ([84, 81] if token == 1 else [14, 11])
    pawn_dir = {9:"P", 10:"P", 11:"P", -9:"p", -10:"p", -11:"p"}
    directions = {9:"b", 11:"b", -9:"b", -11:"b", 1:"r", 10:"r", -1:"r", -10:"r"}
    knight_dir = {12:"n", 8:"n", 19:"n", 21:"n", -12:"n", -8:"n", -19:"n", -21:"n"}
    
    for index in areas:
        for dir in directions:
            new_index = index + dir
            while board[new_index] == ".":
                new_index += dir
            if board[new_index] != "?" and (board[new_index].lower() == directions[dir] or board[new_index].lower() == "q"):
                indices_for_recalculation.append(new_index)
        for dir in knight_dir:
            new_index = index + dir
            if new_index < 100 and new_index >= 0 and board[new_index].lower() == "n":
                indices_for_recalculation.append(new_index)
        for dir in pawn_dir:
            new_index = index + dir
            if board[new_index] == pawn_dir[dir]:
                indices_for_recalculation.append(new_index)
        if index//10 == 4:
            new_index = index-20
            if board[new_index] == "p":
                indices_for_recalculation.append(new_index)
        elif index//10 == 5:
            new_index = index+20
            if board[new_index] == "P":
                indices_for_recalculation.append(new_index)

    return indices_for_recalculation

def recalculate_moves(board, state_board, move):
    indices = recalculation_indices(board, move)
    piece, prev_index, cur_index = move
    token_side = lambda x: (1 if x.isupper() else -1)
    
    #for all pieces
    for i in indices:
        if i == cur_index:
            continue
        
        piece = board[i]
        temp = state_board[i]
        token = token_side(piece)
        
        if piece.lower() == "p":
            state_board[i] = (piece, pawn_moves(i, piece, board, token), temp[2], temp[3])
        elif piece.lower() == "k":
            queen_rook_index = 81 if token == 1 else 11
            king_rook_index = 88 if token == 1 else 18
            queen_rook_moves = state_board[queen_rook_index][2] if board[queen_rook_index].lower() == "r" and token_side(board[queen_rook_index]) == token else -1
            king_rook_moves = state_board[king_rook_index][2] if board[king_rook_index].lower() == "r" and token_side(board[king_rook_index]) == token else -1
            state_board[i] = (piece, king_moves(i, piece, board, token, temp[2], queen_rook_moves, king_rook_moves), temp[2], temp[3])
        elif piece.lower() == "r":
            state_board[i] = (piece, rook_moves(i, piece, board, token), temp[2])
        else:
            piece_moves = {
                            "n":knight_moves,
                            "b":bishop_moves,
                            "q":queen_moves,            
                        }
            state_board[i] = (piece,piece_moves[piece.lower()](i, piece, board, token))
    #check en passant
    white_pawn_check = [41,42,43,44,45,46,47,48]
    black_pawn_check = [51,52,53,54,55,56,57,58]

    #white pawns
    for index in white_pawn_check:
        if board[index] == "P" and state_board[index][3] == False:
            state_board[index] = (state_board[index][0],state_board[index][1][:-1:],state_board[index][2],True)
    #black pawns
    for index in black_pawn_check:
        if board[index] == "p" and state_board[index][3] == False:
            state_board[index] = (state_board[index][0],state_board[index][1][:-1:],state_board[index][2],True)    
    return state_board

def make_move(board_state_board, move):
    new_board, state = board_state_board
    new_board = list(new_board)
    piece_type, index, new_move = move
    piece = piece_type[0]
    color = lambda x: (x.lower() if token == -1 else x.upper())
    token_side = lambda x: (1 if x.isupper() else -1)
    token = token_side(piece)
    state_board = state.copy()
    if new_move in state_board:
        state_board.pop(new_move)
        
    #Making the move
    if len(piece_type) == 1:
        new_board[index] = "."
        new_board[new_move] = piece
    elif piece_type[1:] == "oo": #King Side Castling
        state_board[index][3] == True 
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[88 if token == 1 else 18] = "."
        new_board[86 if token == 1 else 16] = color("r")
        temp1 = state_board[88 if token == 1 else 18]
        state_board.pop(88 if token == 1 else 18)
        state_board[86 if token == 1 else 16] = temp1
    
    elif piece_type[1:] == "ooo": #Queen Side Castling
        state_board[index][3] == True 
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[81 if token == 1 else 11] = "."
        new_board[84 if token == 1 else 14] = color("r")
        temp1 = state_board[81 if token == 1 else 11]
        state_board.pop(81 if token == 1 else 11)
        state_board[84 if token == 1 else 14] = temp1
      
    elif piece_type[1:] == "pas": #En Passant
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[new_move+10*token] = "."
        state_board.pop(new_move+10*token)
        
    #recalculations

    temp = state_board[move[1]]
    state_board.pop(index)
    new_board = "".join(new_board)
    
    #first to recalculate the current pieces moves
    

    if piece.lower() == "p":
        state_board[new_move] = (piece, pawn_moves(new_move, piece, new_board, token), temp[2]+1, temp[3])
    elif piece.lower() == "k":
        queen_rook_index = 81 if token == 1 else 11
        king_rook_index = 88 if token == 1 else 18
        queen_rook_moves = state_board[queen_rook_index][2] if new_board[queen_rook_index].lower() == "r" and token_side(new_board[queen_rook_index]) == token else -1
        king_rook_moves = state_board[king_rook_index][2] if new_board[king_rook_index].lower() == "r" and token_side(new_board[king_rook_index]) == token else -1
        state_board[new_move] = (piece, king_moves(new_move, piece, new_board, token, temp[2], queen_rook_moves, king_rook_moves), temp[2]+1, temp[3])
    elif piece.lower() == "r":
        state_board[new_move] = (piece, rook_moves(new_move, piece, new_board, token), temp[2]+1)
    else:
        piece_moves = {
                        "n":knight_moves,
                        "b":bishop_moves,
                        "q":queen_moves,            
                      }
        state_board[new_move] = (piece,piece_moves[piece.lower()](new_move, piece, new_board, token))
        
    # now recalculate all other piece moves
    recalculate_moves(new_board, state_board, move)
    
    #add en passant move
    
    #left
    if piece.lower() == "p" and abs(new_move-index) == 20 and new_board[new_move-1].lower() == "p" and token_side(new_board[new_move-1]) != token:
        passant_pawn_index = new_move-1
        temp = state_board[passant_pawn_index]
        move_type = "Ppas" if token_side(new_board[passant_pawn_index]) == 1 else "ppas"
        move_index = new_move-10 if move_type == "Ppas" else new_move+10
        state_board[passant_pawn_index] = (temp[0],temp[1] + [(move_type,passant_pawn_index,move_index)], temp[2], False)
    #right
    if piece.lower() == "p" and abs(new_move-index) == 20 and new_board[new_move+1].lower() == "p" and token_side(new_board[new_move+1]) != token:
        passant_pawn_index = new_move+1
        temp = state_board[passant_pawn_index]
        move_type = "Ppas" if token_side(new_board[passant_pawn_index]) == 1 else "ppas"
        move_index = new_move-10 if move_type == "Ppas" else new_move+10
        state_board[passant_pawn_index] = (temp[0],temp[1] + [(move_type,passant_pawn_index,move_index)], temp[2], False)
    
    return (new_board,state_board)  
def quick_make_move(board_state_board, move):
    new_board, state = board_state_board
    new_board = list(new_board)
    piece_type, index, new_move = move
    piece = piece_type[0]
    color = lambda x: (x.lower() if token == -1 else x.upper())
    token_side = lambda x: (1 if x.isupper() else -1)
    token = token_side(piece)
    state_board = state.copy()

        
    #Making the move
    if len(piece_type) == 1:
        new_board[index] = "."
        new_board[new_move] = piece
    elif piece_type[1:] == "oo": #King Side Castling
        state_board[index][3] == True 
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[88 if token == 1 else 18] = "."
        new_board[86 if token == 1 else 16] = color("r")
        temp1 = state_board[88 if token == 1 else 18]
        state_board.pop(88 if token == 1 else 18)
        state_board[86 if token == 1 else 16] = temp1
    
    elif piece_type[1:] == "ooo": #Queen Side Castling
        state_board[index][3] == True 
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[81 if token == 1 else 11] = "."
        new_board[84 if token == 1 else 14] = color("r")
        temp1 = state_board[81 if token == 1 else 11]
        state_board.pop(81 if token == 1 else 11)
        state_board[84 if token == 1 else 14] = temp1
      
    elif piece_type[1:] == "pas": #En Passant
        new_board[index] = "."
        new_board[new_move] = piece[0]
        new_board[new_move+10*token] = "."
        state_board.pop(new_move+10*token)
        
    return ("".join(new_board),state_board)    
def game_end(board_representation):
    B_moves, W_moves = possible_moves_gui(board_representation, -1), possible_moves_gui(board_representation, 1)
    if len(B_moves) == 0 or len(W_moves) == 0:
        return True
    if board_representation[0].count(".") == 62:
        return True
    return False

# board = [[".", ".", ".", ".", ".", ".", ".", "."],  #1
#          [".", ".", ".", ".", ".", ".", ".", "."],  #2
#          [".", ".", ".", ".", ".", ".", ".", "."],  #3
#          [".", ".", ".", ".", ".", ".", ".", "."],  #4
#          [".", ".", ".", ".", ".", ".", ".", "K"],  #5
#          [".", "Q", ".", ".", ".", ".", ".", "."],  #6
#          [".", ".", ".", ".", ".", ".", ".", "."],  #7
#          ["k", ".", ".", ".", ".", ".", ".", "."]]  #8

# str_board = list_to_board(board)
# state_board = state_variables(str_board)
# print(game_end((str_board,state_board)))