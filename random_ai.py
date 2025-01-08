import sys
import ast
import random
import time
from model import *

# board_state = ast.literal_eval(sys.argv[1])
# player = int(sys.argv[2])
# moves = possible_moves_gui(board_state, player)
# print(random.choice(moves))

time.sleep(0.25)
print(random.choice(possible_moves_gui(ast.literal_eval(sys.argv[1]), int(sys.argv[2]))))