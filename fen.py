#rn1qkbnr/pp2pppp/2p5/8/2p1P1b1/5NP1/PP1P1P1P/RNBQKB1R
from model import *
board = "??????????"

fen = "rn1qkbnr/pp2pppp/2p5/8/2p1P1b1/5NP1/PP1P1P1P/RNBQKB1R"
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
print(board)
print_board(board)

