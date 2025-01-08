#FINAL TO DO LIST: pawn promotion, start and endgame sounds, and change settings ability

import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import PhotoImage
from PIL import Image
from PIL import ImageTk
import webcolors
from time import perf_counter
import multiprocessing
from multiprocessing import Process, freeze_support
import sys
import subprocess
import ast
import random
import threading
from model import *
from pygame import mixer
#Chess Modeling:

#pip install webcolors
#py3 -m pip install pillow

timer_end = False
def game_end(board_representation):
    B_moves, W_moves = possible_moves(board_representation, 1), possible_moves(board_representation, -1)
    if len(B_moves) == 0 or len(W_moves) == 0 or timer_end == True:
        return True
    return False



board=[["r", "n", "b", "q", "k", "b", "n", "r"],  #1
        ["p", "p", "p", "p", "p", "p", "p", "p"],  #2
        [".", ".", ".", ".", ".", ".", ".", "."],  #3
        [".", ".", ".", ".", ".", ".", ".", "."],  #4
        [".", ".", ".", ".", ".", ".", ".", "."],  #5
        [".", ".", ".", ".", ".", ".", ".", "."],  #6
        ["P", "P", "P", "P", "P", "P", "P", "P"],  #7
        ["R", "N", "B", "Q", "K", "B", "N", "R"]]  #8
# board = [[".", ".", "R", "R", ".", ".", ".", "."],  #1
#          [".", ".", ".", ".", ".", "P", "P", "."],  #2
#          [".", ".", ".", ".", ".", ".", ".", "."],  #3
#          [".", ".", ".", ".", ".", ".", ".", "."],  #4
#          ["k", ".", ".", ".", ".", ".", ".", "."],  #5
#          [".", ".", ".", ".", ".", ".", ".", "."],  #6
#          [".", ".", ".", ".", "Q", ".", ".", "."],  #7
#          [".", ".", ".", ".", ".", ".", "K", "."]]  #8
8
time_in_seconds = 100
str_board = list_to_board(board)
state_board = state_variables(str_board)
image_board = {i:None for i in state_board}
board_representation = (str_board, state_board)


root = Tk()
mixer.init()
root.title("Chessica")
root.resizable(False, False)
ico = Image.open('image_assets/B_pawn.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

Canvas_width = 1000
Canvas_height = 850
canvas = Canvas(root, width=Canvas_width, height=Canvas_height, bg="#252529")
canvas.pack()

# Mouse Listener
TileSelected = False
Current_tile = ""
Prev_tile_rect = None
Highlited_moves = []
Move_index = -1


images=[]
# Define a function to make the transparent rectangle
def hex_to_rgb(hex_color):
    return webcolors.hex_to_rgb(hex_color)

def create_rectangle(x, y, a, b, **options):
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')

        # Check if the fill color is a hex color
        if fill.startswith("#"):
            fill = hex_to_rgb(fill) + (alpha,)
        else:
            fill = Canvas.winfo_rgb(fill) + (alpha,)

        image = Image.new('RGBA', (a - x, b - y), fill)
        images.append(ImageTk.PhotoImage(image))
        ex = canvas.create_image(x, y, image=images[-1], anchor='nw')
        rec = canvas.create_rectangle(x, y, a, b, **options)
        if Start_game == True :
            for i in image_board:
                canvas.tag_lower(ex,image_board[i][0])
                canvas.tag_lower(rec,image_board[i][0])
                break
        Highlited_moves.append(rec)
        Highlited_moves.append(ex)
      
def on_mouse_click(event):
    global TileSelected, tile_starting_point_x, tile_width, tile_height, Current_tile, Prev_tile_rect, board_moves, Move_index, board_representation
    if Prev_tile_rect:
        canvas.delete(Prev_tile_rect)
    TileSelected = not TileSelected
    #making the move
    if not TileSelected:
        prev_move_index = Move_index
        for m in Highlited_moves:
            canvas.delete(m)
        for row in range(0, 8):
            for col in range(0, 8):
                tile_x = tile_starting_point_x + tile_width *row
                tile_y = tile_starting_point_y + tile_height*col
                if (tile_x < event.x < tile_x + tile_width) and (tile_y < event.y < tile_y + tile_height):
                    Move_index = int(str(col + 1) + str(row + 1))
                
    #displaying possible moves, when tile is selected 

    if (tile_starting_point_x < event.x < tile_starting_point_x + Board_Pxsize - 10) and (
            tile_starting_point_y < event.y < tile_starting_point_y + Board_Pxsize - 10):
        select_color = "#990000" #change later
        highlight_color = "#990000" #change later
        for row in range(0, 8):
            for col in range(0, 8):
                tile_x = tile_starting_point_x + tile_width * row
                tile_y = tile_starting_point_y + tile_height * col
                if (tile_x < event.x < tile_x + tile_width) and (tile_y < event.y < tile_y + tile_height) and TileSelected:
                    Current_tile = int(str(col + 1) + str(row + 1))
                    for move in board_moves:
                        if move[1] == Current_tile:
                            col = int(str(move[2])[0])-1
                            row = int(str(move[2])[1])-1
                            move_tile_x = tile_starting_point_x + tile_width * row
                            move_tile_y = tile_starting_point_y + tile_height * col
                            create_rectangle(int(move_tile_x), int(move_tile_y), int(move_tile_x + tile_width+1), int(move_tile_y + tile_height+1), fill=highlight_color, width = 0, alpha = 0.5)
                    Prev_tile_rect = create_rectangle(int(tile_x), int(tile_y), int(tile_x + tile_width+1), int(tile_y + tile_height+1), fill=select_color, width=0 , alpha = 0.5)
        if str_board[Current_tile] == "." or Current_tile == Move_index:
            Move_index = -1         
canvas.bind("<Button-1>", on_mouse_click)

# Draw the grid
tile_starting_point_x, tile_starting_point_y, Board_Pxsize, tile_width, tile_height,Board_Pxsize = 0, 0, 0, 0, 0, 0
# Draw the Pieces
letters = []
def draw_grid():
    global Canvas_width, Canvas_height, tile_starting_point_x, tile_starting_point_y, Board_Pxsize, tile_width, tile_height,Board_Pxsize
    
    bg_outline = 4
    start = bg_outline
    canvas.create_rectangle(start,start,Canvas_width,Canvas_height,width = bg_outline)
    Board_Pxsize = Canvas_width * 0.65
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height

    board_thickness = 5

    board_start_x = int(Canvas_width * width_margin)
    board_start_y = int(Canvas_height * height_margin)

    # Board outline
    canvas.create_rectangle(board_start_x, board_start_y, board_start_x + Board_Pxsize, board_start_y + Board_Pxsize,
                            outline='Black', width=board_thickness)
    # drawing tiles
    tile_starting_point_x = board_start_x + board_thickness / 2
    tile_starting_point_y = board_start_y + board_thickness / 2
    tile_width = (Board_Pxsize - board_thickness) / 8
    tile_height = (Board_Pxsize - board_thickness) / 8
    white_color = "#A97A65"
    black_color = "#F1D9C0"

    current_tile_color = black_color
    for row in range(0, 8):
        for col in range(0, 8):
            tile_x = tile_starting_point_x + tile_width * row
            tile_y = tile_starting_point_y + tile_height * col
            canvas.create_rectangle(tile_x, tile_y, tile_x + tile_width, tile_y + tile_height, width=0, fill=current_tile_color)
            if row == 0:
                canvas.create_text(tile_x + 8, tile_y + 12, text=str(8-col), font=("Arial", 14), fill=(white_color if current_tile_color == black_color else black_color))
            if col == 7:
                letter = canvas.create_text(tile_x + tile_width-8, tile_y + tile_height-12, text="abcdefgh"[row], font=("Arial", 14), fill=(white_color if current_tile_color == black_color else black_color))
                letters.append(letter)
            current_tile_color = white_color if current_tile_color == black_color else black_color
        current_tile_color = white_color if current_tile_color == black_color else black_color

pics = {}

def draw_pieces():
    global tile_starting_point_x, tile_starting_point_y, Board_Pxsize, tile_width, tile_height, board
    K = ImageTk.PhotoImage(Image.open("image_assets/W_king.png").resize((int(tile_height), int(tile_width))))
    root.K = K
    k = ImageTk.PhotoImage(Image.open("image_assets/B_king.png").resize((int(tile_height), int(tile_width))))
    root.k = k
    Q =ImageTk.PhotoImage(Image.open("image_assets/W_queen.png").resize((int(tile_height), int(tile_width))))
    root.Q = Q
    q = ImageTk.PhotoImage(Image.open("image_assets/B_queen.png").resize((int(tile_height), int(tile_width))))
    root.q = q
    R = ImageTk.PhotoImage(Image.open("image_assets/W_rook.png").resize((int(tile_height), int(tile_width))))
    root.R = R
    r = ImageTk.PhotoImage(Image.open("image_assets/B_rook.png").resize((int(tile_height), int(tile_width))))
    root.r = r
    B = ImageTk.PhotoImage(Image.open("image_assets/W_bishop.png").resize((int(tile_height), int(tile_width))))
    root.B = B
    b = ImageTk.PhotoImage(Image.open("image_assets/B_bishop.png").resize((int(tile_height), int(tile_width))))
    root.b = b
    N = ImageTk.PhotoImage(Image.open("image_assets/W_Knight.png").resize((int(tile_height), int(tile_width))))
    root.N = N
    n = ImageTk.PhotoImage(Image.open("image_assets/B_Knight.png").resize((int(tile_height), int(tile_width))))
    root.n = n
    P = ImageTk.PhotoImage(Image.open("image_assets/W_pawn.png").resize((int(tile_height), int(tile_width))))
    root.P = P
    p = ImageTk.PhotoImage(Image.open("image_assets/B_pawn.png").resize((int(tile_height), int(tile_width))))
    root.p = p
    
    pics = {"K":K, "k":k, "Q":Q, "q":q, "R":R, "r":r, "B":B, "b":b, "N":N, "n":n, "P":P, "p":p}
    for row in range(0, 8):
            for col in range(0, 8):
                tile_x = tile_starting_point_x + tile_width * row
                tile_y = tile_starting_point_y + tile_height * col
                tile_index = int(str(col + 1) + str(row + 1))
                
                piece = str_board[tile_index]

                image_path = ""
                if piece in pics :
                    image_board[tile_index] = (canvas.create_image(int(tile_x), int(tile_y), image=pics[piece], anchor=tk.NW), int(tile_x), int(tile_y))   
                    
white_timer, black_timer = None, None
deactive_color = "#6f6f78"
active_color = "#c5c5d1"

#set up the timer cordinates

def draw_timer():
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height

    timer_box_width = Canvas_width*0.13
    timer_box_height = Canvas_height*0.05

    White_box_x = Canvas_width*width_margin
    White_box_y = Canvas_height*0.9

    Black_box_x = Canvas_width-Canvas_width*width_margin-timer_box_width-4
    Black_box_y = Canvas_height*0.05
    global white_timer,black_timer

    #white box and text
    minutes = time_in_seconds//60
    seconds = time_in_seconds%60
    time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
    canvas.create_rectangle(White_box_x,White_box_y, White_box_x+timer_box_width,White_box_y+timer_box_height,outline="Black",width=1, fill="#4d4d52")
    white_timer = canvas.create_text(White_box_x + 50, (2*White_box_y+timer_box_height)/2, text= time_text , font=("Conforta", 25), fill= deactive_color)
    
    #black box and text
    canvas.create_rectangle(Black_box_x,Black_box_y, Black_box_x+timer_box_width,Black_box_y+timer_box_height,outline="Black",width=1, fill="#4d4d52")
    black_timer = canvas.create_text(Black_box_x + 50, (2*Black_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= deactive_color)


black_time, white_time = time_in_seconds,time_in_seconds
count = 0
def update_timer():
    global Whites_turn,time_in_seconds,white_time,black_time, black_timer, white_timer,timer_end,count
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height

    timer_box_width = Canvas_width*0.13
    timer_box_height = Canvas_height*0.05

    White_box_x = Canvas_width*width_margin
    White_box_y = Canvas_height*0.9

    Black_box_x = Canvas_width-Canvas_width*width_margin-timer_box_width-4
    Black_box_y = Canvas_height*0.05
    if Whites_turn and count%100 == 0:

        canvas.delete(white_timer)
        white_time -= 1
        minutes = white_time//60
        seconds = white_time%60
        time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
        white_timer = canvas.create_text(White_box_x + 50, (2*White_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= active_color)
    elif count%100 == 0:
        canvas.delete(black_timer)
        black_time -= 1
        minutes = black_time//60
        seconds = black_time%60
        time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
        black_timer = canvas.create_text(Black_box_x + 50, (2*Black_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= active_color)
        
        

    if white_time == 0 or black_time == 0 or game_end(board_representation):
        timer_end = True
    else:
        count += 1
        root.after(10,update_timer)
        
def deactivate_black():
    global Whites_turn,time_in_seconds,white_time,black_time, black_timer, white_timer,timer_end
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height

    timer_box_width = Canvas_width*0.13
    timer_box_height = Canvas_height*0.05

    Black_box_x = Canvas_width-Canvas_width*width_margin-timer_box_width-4
    Black_box_y = Canvas_height*0.05
    
    White_box_x = Canvas_width*width_margin
    White_box_y = Canvas_height*0.9
    
    canvas.delete(black_timer)
    minutes = black_time//60
    seconds = black_time%60
    time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
    black_timer = canvas.create_text(Black_box_x + 50, (2*Black_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= deactive_color)

    canvas.delete(white_timer)
    minutes = white_time//60
    seconds = white_time%60
    time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
    white_timer = canvas.create_text(White_box_x + 50, (2*White_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= active_color)
    
def deactivate_white():
    global Whites_turn,time_in_seconds,white_time,black_time, black_timer, white_timer,timer_end
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height

    timer_box_width = Canvas_width*0.13
    timer_box_height = Canvas_height*0.05

    Black_box_x = Canvas_width-Canvas_width*width_margin-timer_box_width-4
    Black_box_y = Canvas_height*0.05
    
    White_box_x = Canvas_width*width_margin
    White_box_y = Canvas_height*0.9
    
    canvas.delete(black_timer)
    minutes = black_time//60
    seconds = black_time%60
    time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
    black_timer = canvas.create_text(Black_box_x + 50, (2*Black_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= active_color)
    
    canvas.delete(white_timer)
    minutes = white_time//60
    seconds = white_time%60
    time_text = str(minutes) + ":" + str(seconds) if len(str(seconds)) > 1 else str(minutes) + ":" + "0" + str(seconds)
    white_timer = canvas.create_text(White_box_x + 50, (2*White_box_y+timer_box_height)/2, text= time_text, font=("Conforta", 25), fill= deactive_color)
            
def useless_funct(event):
    return None

def animate(image_index, ending_coordinates, move_index, move,str_board1):
    global move_to_make,tile_starting_point_x,tile_starting_point_y, tile_width,board_representation,move_rect
    image_id, start_x, start_y = image_board[image_index]
    end_x, end_y = ending_coordinates

    step_size = 4
    if ((end_x-start_x)**2 + (end_y-start_y)**2)**0.5 < 4:
        step_size = 1
    elif ((end_x-start_x)**2 + (end_y-start_y)**2)**0.5 > 4:
        step_size = 4
    dx = step_size if end_x > start_x else -step_size
    dx = 0 if end_x-start_x == 0 else dx
    
    dy = step_size if end_y > start_y else -step_size
    dy = 0 if end_y-start_y == 0 else dy
    
    if move[0][0].lower() == "n":
        if abs(move[1]-move[2]) == 19 or abs(move[1]-move[2]) == 21 :
            dx = dx*0.5
        else:
            dy = dy*0.5

    if move[0][1:] == "oo":
        index = str(move[2]-1)
        
        rook_index = 88 if move[0][0].isupper() else 18
        rook_id, rook_x, rook_y = image_board[rook_index]
        
        final_col = int(index[0])-1
        final_row = int(index[1])-1
        
        final_x = tile_starting_point_x + tile_width * final_row
        
        rook_dx  = step_size if final_x > rook_x else -step_size
    if move[0][1:] == "ooo":
        index = str(move[2]+1)
        
        rook_index = 81 if move[0][0].isupper() else 11
        rook_id, rook_x, rook_y = image_board[rook_index]
        
        final_col = int(index[0])-1
        final_row = int(index[1])-1
        
        final_x = tile_starting_point_x + tile_width * final_row
        print(final_row)       
        rook_dx  = step_size if final_x > rook_x else -step_size        
        


    if abs(start_x-end_x) <= 1 and abs(start_y-end_y) <= 1 and "oo" not in move[0]:
        if move_index in image_board:
            canvas.delete(image_board[move_index][0])
            image_board.pop(move_index)
        temp = image_board[image_index]
        image_board.pop(image_index)
        image_board[move_index] = temp
        if "pas" in move[0]:
            index = move[2]-10 if move[0][0].islower() else move[2]+10
            canvas.delete(image_board[index][0])
            image_board.pop(index)
        _,rect_x,rect_y = image_board[move[2]]
        
        if move[0][0] != str_board1[move[1]]:
            Q1 =ImageTk.PhotoImage(Image.open("image_assets/W_queen.png").resize((int(tile_height), int(tile_width))))
            root.Q1 = Q1
            q1 = ImageTk.PhotoImage(Image.open("image_assets/B_queen.png").resize((int(tile_height), int(tile_width))))
            root.q1 = q1
            R1 = ImageTk.PhotoImage(Image.open("image_assets/W_rook.png").resize((int(tile_height), int(tile_width))))
            root.R1 = R1
            r1 = ImageTk.PhotoImage(Image.open("image_assets/B_rook.png").resize((int(tile_height), int(tile_width))))
            root.r1 = r1
            B1 = ImageTk.PhotoImage(Image.open("image_assets/W_bishop.png").resize((int(tile_height), int(tile_width))))
            root.B1 = B1
            b1 = ImageTk.PhotoImage(Image.open("image_assets/B_bishop.png").resize((int(tile_height), int(tile_width))))
            root.b1 = b1
            N1 = ImageTk.PhotoImage(Image.open("image_assets/W_Knight.png").resize((int(tile_height), int(tile_width))))
            root.N1 = N1
            n1 = ImageTk.PhotoImage(Image.open("image_assets/B_Knight.png").resize((int(tile_height), int(tile_width))))
            root.n1 = n1

            pics1 = {"Q":Q1, "q":q1, "R":R1, "r":r1, "B":B1, "b":b1, "N":N1, "n":n1}
            canvas.delete(image_board[move_index][0])
            image_board[move_index] = (canvas.create_image(image_board[move_index][1],image_board[move_index][2], image=pics1[move[0][0]], anchor = tk.NW),image_board[move_index][1],image_board[move_index][2])

        return None
    elif "oo" in move[0] and abs(start_x-end_x) <= 1 and abs(start_y-end_y) <= 1 and abs(rook_x-final_x) <= 1:
        if move_index in image_board:
            canvas.delete(image_board[move_index][0])
            image_board.pop(move_index)
        temp = image_board[image_index]
        image_board.pop(image_index)
        image_board[move_index] = temp
        
        temp = image_board[rook_index]
        image_board.pop(rook_index)
        image_board[move[2]-1 if move[0][1:] == "oo" else move[2]+1] = temp

    else:
        if "oo" not in move[0]:
            image_board[image_index] = (image_id, start_x + dx, start_y + dy)
            canvas.move(image_id, dx, dy)
            root.after(1, animate, image_index, ending_coordinates, move_index, move, str_board1)
        else:
            image_board[image_index] = (image_id, start_x + dx, start_y + dy)
            image_board[rook_index] = (rook_id,rook_x + rook_dx, rook_y)
            canvas.move(image_id, dx, dy)
            canvas.move(rook_id, rook_dx, 0)
            root.after(1, animate, image_index, ending_coordinates, move_index, move, str_board1)

pre_move_rect, move_rect = None, None

capture = "audio_assets/capture.mp3"
castle = "audio_assets/castle.mp3"
check = "audio_assets/check.mp3"
move = "audio_assets/move.mp3"
promote = "audio_assets/promote.mp3"

prev_selected = []
def delete_selected():
    for i in prev_selected:
        canvas.delete(i)
    canvas.delete("rect")
        
def create_rectangle_2(x, y, a, b, **options):
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')

        # Check if the fill color is a hex color
        if fill.startswith("#"):
            fill = hex_to_rgb(fill) + (alpha,)
        else:
            fill = Canvas.winfo_rgb(fill) + (alpha,)

        image = Image.new('RGBA', (a - x, b - y), fill)
        images.append(ImageTk.PhotoImage(image))
        ex = canvas.create_image(x, y, image=images[-1], anchor='nw', tag="rect")
        rec = canvas.create_rectangle(x, y, a, b, **options, tag="rect")
        prev_selected.append(rec)
        prev_selected.append(ex)

def redraw():
    global tile_starting_point_x,tile_starting_point_y, tile_width, tile_height, Move_index,move_rect, pre_move_rect
    animate_move = move_to_make

    if move_to_make == -1:
        canvas.delete("all")
        draw_grid()
        draw_pieces()
        draw_timer()
        for letter in letters:
            canvas.tag_raise(letter)
    else:
        for row in range(0, 8):
                for col in range(0, 8):
                    tile_x = tile_starting_point_x + tile_width * row
                    tile_y = tile_starting_point_y + tile_height * col
                    tile_index = int(str(col + 1) + str(row + 1))
                    if tile_index == animate_move[2]:
                        _,rect_x,rect_y = image_board[animate_move[1]]
                        create_rectangle_2(int(rect_x),int(rect_y),int(rect_x+tile_width+1),int(rect_y+tile_height+1),fill="#F7E672", width = 0, alpha = 0.5)
                        rect_x,rect_y = (tile_x,tile_y)
                        create_rectangle_2(int(rect_x),int(rect_y),int(rect_x+tile_width+1),int(rect_y+tile_height+1),fill="#F7E672", width = 0, alpha = 0.5)
                        canvas.tag_lower("rect",image_board[animate_move[1]][0])
                        animate(animate_move[1],(tile_x,tile_y),animate_move[2],animate_move, str_board)
                        
                        break
    if animate_move == -1:
        None 
    elif str_board[animate_move[2]] != "." or "pas" in animate_move[0]:
        print(animate_move)
        mixer.music.load(capture)
        mixer.music.play()
    elif "oo" in animate_move[0]:
        mixer.music.load(castle)
        mixer.music.play()
    else:
        mixer.music.load(move)
        mixer.music.play()     

    
board_moves = possible_moves_gui(board_representation, 1)
Whites_turn = True
White_player = "p"
Black_player = "p"


Has_poped_up = True
def end_game(message):
    global Has_poped_up 
    if not Has_poped_up:
        popup = Toplevel(root)
        popup.title("Game Ended")
        label = Label(popup, text=message)
        label.pack(padx=20, pady=20)
        Has_poped_up = not Has_poped_up

prev_moves = set()
move_to_make = -1
threads = []
def game_loop():
    #game starts here
    global board_moves, board_representation, Move_index, str_board, Whites_turn, Black_player, White_player,best_outcome,best_move,Recreate,move_to_make,threads,count
    if Whites_turn:
        if "ai" in White_player:
            canvas.bind("<Button-1>", useless_funct)
            new_board_rep = (board_representation[0],board_representation[1].copy())
            
            if len(threads) == 0:
                thread = threading.Thread(target=get_best_move, args=(1,White_player))
                threads.append(thread)
                thread.start()
                
            if move_to_make != -1:
                move_index = 1
                threads = []
                prev_moves.add(new_board_rep[0])
                delete_selected()
                redraw()
                board_representation = make_move(board_representation, move_to_make)
                str_board = board_representation[0]
                board_moves = possible_moves_gui(board_representation, -1)
                Move_index = 1
                deactivate_white()
                move_to_make = -1
                canvas.bind("<Button-1>", on_mouse_click)
                Whites_turn = not Whites_turn
                if king_in_check(board_representation[0],-1):
                    mixer.music.load(check)
                    mixer.music.play()  

            
        else:
            canvas.bind("<Button-1>", on_mouse_click)
            if Move_index != -1 and White_player == "p":
                move_to_make = None
                for move in board_moves:
                    if move[1] == Current_tile and move[2] == Move_index:
                        move_to_make = move
                        delete_selected()
                        redraw()
                        board_representation = make_move(board_representation, move)
                        deactivate_white()
                        str_board = board_representation[0]
                        board_moves = possible_moves_gui(board_representation, -1)
                        Move_index = -1
                        move_to_make = -1
                        Whites_turn = not Whites_turn
                        if king_in_check(board_representation[0],-1):
                            mixer.music.load(check)
                            mixer.music.play()  
                        break
    else:

        if "ai" in Black_player:
            canvas.bind("<Button-1>", useless_funct)
            new_board_rep = (board_representation[0],board_representation[1].copy())
            if len(threads) == 0:
                thread = threading.Thread(target=get_best_move, args=(-1,Black_player))
                threads.append(thread)
                thread.start()
            if move_to_make != -1:
                threads = []
                prev_moves.add(new_board_rep[0])
                delete_selected()
                redraw()
                deactivate_black()
                board_representation = make_move(board_representation, move_to_make)
                str_board = board_representation[0]
                board_moves = possible_moves_gui(board_representation, 1)
                Move_index = 1
                move_to_make = -1
                if king_in_check(board_representation[0],1):
                    mixer.music.load(check)
                    mixer.music.play()  
                Whites_turn = not Whites_turn
                canvas.bind("<Button-1>", on_mouse_click)
        else:
            canvas.bind("<Button-1>", on_mouse_click)
        
        if Move_index != -1 and Black_player == "p":            
            for move in board_moves:
                if move[1] == Current_tile and move[2] == Move_index:
                    move_to_make = move
                    delete_selected()
                    redraw()
                    deactivate_black()
                    board_representation = make_move(board_representation, move)
                    str_board = board_representation[0]
                    board_moves = possible_moves_gui(board_representation, 1)
                    Move_index = -1
                    move_to_make = -1
                    Whites_turn = not Whites_turn
                    if king_in_check(board_representation[0],1):
                        mixer.music.load(check)
                        mixer.music.play()  
                    break
    rec = None
    if not game_end(board_representation):
        root.after(16, game_loop)
    else:
        Recreate = False
        # title_screen()
        print("game has ended")


white_player_choice = StringVar(root)
black_player_choice = StringVar(root)

# Set default choices
white_player_choice.set("Human")
black_player_choice.set("Human")

# Increase the size of the dropdown menu font
sub_font = font.Font(family="Times", size=60)

# Set initial value for Recreate
Recreate = False
Start_game = False
def play_button_callback():
    global White_player,Black_player,Start_game,board_representation,Move_index,str_board
    print("Play button clicked")
    print("White Player:", white_player_choice.get())
    print("Black Player:", black_player_choice.get())
    if white_player_choice.get() == "Human":
        White_player = "p"
    elif white_player_choice.get() == "Random AI":
        White_player = "Random ai"     
    elif white_player_choice.get() == "Greedy AI":
        White_player = "Greed ai"   
    elif white_player_choice.get() == "Medium AI":
        White_player = "Medium ai"
    elif white_player_choice.get() == "Hard AI":
        White_player = "Hard ai"
    elif white_player_choice.get() == "Medium L2 AI":
        White_player = "L2 ai"
        
    if black_player_choice.get() == "Human":
        Black_player = "p"
    elif black_player_choice.get() == "Random AI":
        Black_player = "Random ai"     
    elif black_player_choice.get() == "Greedy AI":
        Black_player = "Greed ai"   
    elif black_player_choice.get() == "Medium AI":
        Black_player = "Medium ai"
    elif black_player_choice.get() == "Hard AI":
        Black_player = "Hard ai"
    elif black_player_choice.get() == "Medium L2 AI":
        Black_player = "L2 ai"
    
    # board=[["r", "n", "b", "q", "k", "b", "n", "r"],  #1
    #        ["p", "p", "p", "p", "p", "p", "p", "p"],  #2
    #        [".", ".", ".", ".", ".", ".", ".", "."],  #3
    #        [".", ".", ".", ".", ".", ".", ".", "."],  #4
    #        [".", ".", ".", ".", ".", ".", ".", "."],  #5
    #        [".", ".", ".", ".", ".", ".", ".", "."],  #6
    #        ["P", "P", "P", "P", "P", "P", "P", "P"],  #7
    #        ["R", "N", "B", "Q", "K", "B", "N", "R"]]  #8
    str_board = list_to_board(board)
    state_board = state_variables(str_board)
    board_representation = (str_board, state_board)
    canvas.delete('all')
    black_player_choice.destroy()
    white_player_choice.destroy()
    play_button.destroy()
    Move_index = None
    redraw()
    #display who is playing
    width_margin = ((Canvas_width - Board_Pxsize) / 2) / Canvas_width
    height_margin = ((Canvas_height - Board_Pxsize) / 2) / Canvas_height
    
    box_height = Canvas_height*0.05
    box_width = Canvas_width*0.15
    
    Black_box_x = Canvas_width*width_margin + 4
    Black_box_y = Canvas_height*0.05
    
    White_box_x = Canvas_width-Canvas_width*width_margin-box_width-4
    White_box_y = Canvas_height*0.9
    
    White_text = "Player 1" if White_player == "p" else White_player
    Black_text = "Player 2" if Black_player == "p" else Black_player
    
    canvas.create_rectangle(White_box_x, White_box_y, White_box_x + box_width, White_box_y + box_height, width= 1,fill="#4d4d52")
    canvas.create_text(White_box_x + 70 , (2*White_box_y + box_height)//2 , text= White_text,fill= active_color, font=("Conforta", 18, "bold"))
    
    canvas.create_rectangle(Black_box_x, Black_box_y, Black_box_x + box_width, Black_box_y + box_height, width= 1,fill="#4d4d52")
    canvas.create_text(Black_box_x + 70 , (2*Black_box_y + box_height)//2 , text= Black_text,fill= active_color, font=("Conforta", 18, "bold"))
    game_loop()
    update_timer()

    Start_game = True

def get_best_move(token, Player):
    time_limit = 2
    global board_representation, best_move, move_to_make
    print_board(str_board)
    ai_type = "ai.py"
    if Player == "Greed ai":
        ai_type = "greedy.py"
    elif Player == "Random ai":
        ai_type = "random_ai.py"
    elif Player == "Medium ai":
        ai_type = "ab.py"
    elif Player == "Hard ai":
        ai_type = "hard_ai.py"
    else:
        ai_type = "ap_h.py"
    try:
        # The next two lines run a subprocess that runs a player's script with appropriate args and captures output.
        # args is the list of arguments sent to start the process.  sys.executable is the python executable that is
        # running the current file; -u makes the output unbuffered so it can all be captured; the rest are command
        # line args sent to the python executable - first the name of the .py file we're running, then the args
        # sent to the .py file - the board and the current token, x or o.
        if ai_type == "hard_ai.py": 
            args = [sys.executable, "-u", ai_type,str(board_representation), str(token),str(prev_moves)]
        else:
            args = [sys.executable, "-u", ai_type,str(board_representation), str(token)]
        stream = subprocess.run(args, capture_output=True, text=True, timeout=time_limit)
        outs = stream.stdout  # This will happen if the subprocess ends itself within the time limit.
        errs = stream.stderr
        print("Turn ended in less than time limit.")
    except subprocess.TimeoutExpired as timeErr:
        # This "except" block happens when the process does not end itself in time and times out; this still will
        # capture the output, but now gets it from the TimeoutExpired exception itself.  Either way: output and any
        # error messages that arose along the way are captured.
        outs = timeErr.stdout
        errs = timeErr.stderr
        print("Turn killed after time limit.")
    if len(errs) > 0:
        print("Error message from", str(token) + ":")
        print()
        print(outs)
        print()
        print(errs)
        print("Attempting to continue play.")
    # Now that the output of the player's code is captured, try to get a valid move out of it.
    try:
        print(outs)
        outputs = outs.strip().split("\n")
        move = ast.literal_eval(outputs[-1])
        move_to_make = move
    except Exception as e:
        
        print("error",e)
    return None


from tkinter import ttk
import random

        
def title_screen():
    global Recreate, Start_game, canvas, Canvas_width, Canvas_height, white_player_choice, black_player_choice, title_text_id,white_player_choice,black_player_choice,play_button

    
    if not Recreate:
        canvas.bind("<Button-1>", useless_funct)

            
        Icon_height = Canvas_height * 0.5
        Icon_width = Canvas_width * 0.5
        Icon_x = ((Canvas_width - Icon_width) / 2)
        Icon_y = ((Canvas_height - Icon_height) / 2) - Canvas_height * 0.1

        canvas.delete("all")
        redraw()
        outline_thickness = 6
        title_screen_bg_color = "#282836"
        create_rectangle(
            outline_thickness, outline_thickness, Canvas_width, Canvas_height,
            fill=title_screen_bg_color, width=outline_thickness, alpha=0.95
        )

        # Creating play button
        button_width = Canvas_width * 0.2 
        button_height = Canvas_height * 0.1 

        play_button = Button(
            text="Play",
            font=("Conforta", 36, "bold"),
            command=play_button_callback,
            bg="#3C404D",
            fg="#FFFFFF"
        )
        play_button.place(relx=0.5, rely=0.75, anchor="center", width=button_width, height=button_height)

 
        title_text = "Chess AI"
        title_font = ("Conforta", 50, "bold")
        title_color = "#FFFFFF"
        title_text_id = canvas.create_text(Canvas_width // 2, Canvas_height * 0.2, text=title_text, font=title_font, fill=title_color)

   
        player_options = ["Human", "Random AI", "Greedy AI", "Medium AI", "Medium L2 AI", "Hard AI"]

        drop_down_width = 250
        drop_down_height = 50
        drop_down_font_size = 20
        
        white_player_label = canvas.create_text(Canvas_width // 2, Canvas_height * 0.35, text="White Player", font=("Conforta", 30, "bold"), fill="#FFFFFF")
        white_player_choice = ttk.Combobox(canvas, values=player_options, state="readonly", font=("Conforta", drop_down_font_size), width=drop_down_width, height=drop_down_height, style="TCombobox",)
        white_player_choice.set("Human")
        white_player_choice.place(relx=0.5, rely=0.41, anchor="center", width=drop_down_width, height=drop_down_height)  


        black_player_label = canvas.create_text(Canvas_width // 2, Canvas_height * 0.5, text="Black Player", font=("Conforta", 30, "bold"), fill="#FFFFFF")
        black_player_choice = ttk.Combobox(canvas, values=player_options, state="readonly", font=("Conforta", drop_down_font_size), width=drop_down_width, height=drop_down_height, style="TCombobox",)
        
        black_player_choice.set("Human")
        black_player_choice.place(relx=0.5, rely=0.56, anchor="center", width=drop_down_width, height=drop_down_height)  
        made_by_text = canvas.create_text(Canvas_width*0.2, Canvas_height * 0.95, text="Made by: Ethan Cheung", font=("Conforta", 16), fill="#FFFFFF")
        
        t = ImageTk.PhotoImage(Image.open("image_assets/title_pic_w.png").resize((int(Canvas_width*0.5),int(Canvas_width*0.5))))
        root.t = t
        t1 = ImageTk.PhotoImage(Image.open("image_assets/title_pic.png").resize((int(Canvas_width*0.5),int(Canvas_width*0.5))).rotate(180))
        root.t1 = t1
        p = {1:t,2:t1}
        
        canvas.create_image(Canvas_width*0.6, Canvas_height*0.42, image=p[1], anchor=tk.NW)

        canvas.create_image(Canvas_width*(-0.10), Canvas_height*0.0, image=p[2], anchor=tk.NW)
        
        Recreate = True

    if not Start_game:
        root.after(100, title_screen)




if __name__ == "__main__":
    canvas.delete('all')
    title_screen()

    root.mainloop()
