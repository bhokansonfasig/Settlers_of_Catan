# Catan.py
# Version 0.0.0
# Created by Ben Hokanson-Fasig
# Last update 02-16-16

from tkinter import *
from random import *


version = "0.0.0"

# Define aesthetic parameters
win_width = 1200  #window width
win_height = 800  #window height
menu_color = "#EECC8C"
button_color = "#FFFFCC"
sand_color = "#D7B992"
wood_color = "#2C8236"
brick_color = "#8B0000"
sheep_color = "#A6FFA6"
wheat_color = "#F5B800"
stone_color = "#686868"

if win_height<167:
    txt_size = 5
elif win_height>1200:
    txt_size = 36
else:
    txt_size = int(.03*win_height)


################################################################################
# Determining players and difficulty
# playnum = 0
# compnum = 0
#
# comp1diff = 0
# comp2diff = 0
# comp3diff = 0
# comp4diff = 0
#
# while (playnum<=1 or playnum>=5) or (compnum<=-1 or compnum>=5):
#     playnum = eval(input("Total number of players: "))
#     compnum = eval(input("Number of computer players: "))
#     if playnum==compnum:
#         comp1diff = eval(input("Computer 1 level: "))
#     if playnum<=compnum+1:
#         comp2diff = eval(input("Computer 2 level: "))
#     if playnum<=compnum+2 and playnum>=3:
#         comp3diff = eval(input("Computer 3 level: "))
#     if playnum<=compnum+3 and playnum==4:
#         comp4diff = eval(input("Computer 4 level: "))


# Raise errors for strange dimensions
if 2*win_width!=3*win_height:
    print("Board dimensions are incorrect, some elements may appear distorted.")
if win_width<800 or win_height<800:
    print("Board window too small, some features may not appear properly.")

################################################################################
# Define variables

# Geometry for board window
board_geometry = "%dx%d+50+50" % (win_width,win_height)

# Set width and height of hexagon section
hex_height = win_height*75/100
if win_width>=win_height:
    hex_width = hex_height
else:
    hex_width = win_width*75/100
    hex_height = hex_width

# Set width of water region
water_width = int(hex_width/10)

# Set offsets from top right corner for hexagon section (not including water)
hex_x_off = int(win_width-hex_width-water_width)
hex_y_off = int(win_height-hex_height-water_width)

# 25 tiles with attributes:
#  0 - tkinter index numbers: [hexagon, number]
#  1 - tile resource type ("empty" for nonlegal hexagon)
#  2 - tile dice roll number (-1 for nonlegal hexagon)
#  3 - array of owners of settlement points cw from top
#  4 - array of owners of road sides cw from top right
tiles = [
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "none", 0, [0,0,0,0,0,0], [0,0,0,0,0,0]],
    [[-1,-1], "empty", -1, [0,0,0,0,0,0], [0,0,0,0,0,0]]]

active_tiles = [1,2,3,5,6,7,8,10,11,12,13,14,15,16,17,18,21,22,23]


################################################################################
# Set up display classes

# App screen class
class App(Frame):

    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Settlers of Catan - Welcome")
        self.pack(fill=BOTH, expand=1)

        splash_canvas = Canvas(self, background=menu_color)
        # Welcome text
        splash_canvas.create_text(200, 50, font=("Helvetica", 36),
            text="Settlers of Catan")
        splash_canvas.create_text(200, 100, font=("Helvetica", 18),
            text="Version "+version)
        splash_canvas.pack(fill=BOTH, expand=1)
        # Buttons
        play_button = Button(splash_canvas, font=("Helvetica", 16),
            text="New Game", command=new_game)
        play_button.configure(width=10, activebackground = button_color,
            command=new_game)
        play_button_window = splash_canvas.create_window(100, 200,
            window=play_button)
        load_button = Button(splash_canvas, font=("Helvetica", 16),
            text="Load Game", command=load_game)
        load_button.configure(width=10, activebackground = button_color,
            command=load_game)
        load_button_window = splash_canvas.create_window(300, 200,
            window=load_button)
        quit_button = Button(splash_canvas, font=("Helvetica", 16),
            text="Quit", command=self.quit)
        quit_button.configure(width=10, activebackground = button_color)
        quit_button_window = splash_canvas.create_window(200, 250,
            window=quit_button)

        # Create and hide board window
        global board
        board = Toplevel()
        board.geometry(board_geometry)
        board.title("Settlers of Catan - Play")
        global board_canvas
        board_canvas = Canvas(board)
        board_canvas.pack(fill=BOTH, expand=1)
        board.withdraw()
        #Skeleton
        hex1_points = [
            int(hex_width*2/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
        hex2_points = [
            int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
        hex3_points = [
            int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
        hex5_points = [
            int(hex_width*1/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
        hex6_points = [
            int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
        hex7_points = [
            int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
        hex8_points = [
            int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
        hex10_points = [
            int(hex_width*0/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*0/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*0/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
        hex11_points = [
            int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
        hex12_points = [
            int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
        hex13_points = [
            int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
        hex14_points = [
            int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*10/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*10/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
        hex15_points = [
            int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
        hex16_points = [
            int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
        hex17_points = [
            int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
        hex18_points = [
            int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*9/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
        hex21_points = [
            int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]
        hex22_points = [
            int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]
        hex23_points = [
            int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
            int(hex_width*8/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
            int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
            int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]

        board_canvas.create_rectangle(hex_x_off-water_width,
            hex_y_off-water_width, win_width, win_height, fill="#6680FF")

        tiles[1][0][0] = board_canvas.create_polygon(hex1_points,
            outline=sand_color, fill='white', width=4)
        tiles[2][0][0] = board_canvas.create_polygon(hex2_points,
            outline=sand_color, fill='white', width=4)
        tiles[3][0][0] = board_canvas.create_polygon(hex3_points,
            outline=sand_color, fill='white', width=4)
        tiles[5][0][0] = board_canvas.create_polygon(hex5_points,
            outline=sand_color, fill='white', width=4)
        tiles[6][0][0] = board_canvas.create_polygon(hex6_points,
            outline=sand_color, fill='white', width=4)
        tiles[7][0][0] = board_canvas.create_polygon(hex7_points,
            outline=sand_color, fill='white', width=4)
        tiles[8][0][0] = board_canvas.create_polygon(hex8_points,
            outline=sand_color, fill='white', width=4)
        tiles[10][0][0] = board_canvas.create_polygon(hex10_points,
            outline=sand_color, fill='white', width=4)
        tiles[11][0][0] = board_canvas.create_polygon(hex11_points,
            outline=sand_color, fill='white', width=4)
        tiles[12][0][0] = board_canvas.create_polygon(hex12_points,
            outline=sand_color, fill='white', width=4)
        tiles[13][0][0] = board_canvas.create_polygon(hex13_points,
            outline=sand_color, fill='white', width=4)
        tiles[14][0][0] = board_canvas.create_polygon(hex14_points,
            outline=sand_color, fill='white', width=4)
        tiles[15][0][0] = board_canvas.create_polygon(hex15_points,
            outline=sand_color, fill='white', width=4)
        tiles[16][0][0] = board_canvas.create_polygon(hex16_points,
            outline=sand_color, fill='white', width=4)
        tiles[17][0][0] = board_canvas.create_polygon(hex17_points,
            outline=sand_color, fill='white', width=4)
        tiles[18][0][0] = board_canvas.create_polygon(hex18_points,
            outline=sand_color, fill='white', width=4)
        tiles[21][0][0] = board_canvas.create_polygon(hex21_points,
            outline=sand_color, fill='white', width=4)
        tiles[22][0][0] = board_canvas.create_polygon(hex22_points,
            outline=sand_color, fill='white', width=4)
        tiles[23][0][0] = board_canvas.create_polygon(hex23_points,
            outline=sand_color, fill='white', width=4)



################################################################################
# Major function calls
def new_game():
    print("New game started")
    root.withdraw()
    board.update()
    board.deiconify()
    set_tiles()
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")
    end_game(board)


def load_game():
    print("Old game loaded")
    root.withdraw()
    board.update()
    board.deiconify()
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")
    end_game(board)


def end_game(board):
    board.withdraw()
    root.update()
    root.deiconify()


################################################################################
# Minor function calls
def set_tiles():
    # Suggested preset:
    tiles[1][1] = "wood"
    tiles[1][2] = 11
    tiles[2][1] = "sheep"
    tiles[2][2] = 12
    tiles[3][1] = "wheat"
    tiles[3][2] = 9
    tiles[5][1] = "brick"
    tiles[5][2] = 4
    tiles[6][1] = "stone"
    tiles[6][2] = 6
    tiles[7][1] = "brick"
    tiles[7][2] = 5
    tiles[8][1] = "sheep"
    tiles[8][2] = 10
    tiles[10][1] = "desert"
    tiles[10][2] = 0
    tiles[11][1] = "wood"
    tiles[11][2] = 3
    tiles[12][1] = "wheat"
    tiles[12][2] = 11
    tiles[13][1] = "wood"
    tiles[13][2] = 4
    tiles[14][1] = "wheat"
    tiles[14][2] = 8
    tiles[15][1] = "brick"
    tiles[15][2] = 8
    tiles[16][1] = "sheep"
    tiles[16][2] = 10
    tiles[17][1] = "sheep"
    tiles[17][2] = 9
    tiles[18][1] = "stone"
    tiles[18][2] = 3
    tiles[21][1] = "stone"
    tiles[21][2] = 5
    tiles[22][1] = "wheat"
    tiles[22][2] = 2
    tiles[23][1] = "wood"
    tiles[23][2] = 6

    # Random layout
    # use choice(array) to get one item from the array randomly

    # Fill in the appropriate colors and numbers
    for i in active_tiles:
        # Filling colors
        if tiles[i][1]=="wood":
            board_canvas.itemconfig(tiles[i][0][0],fill=wood_color)
        elif tiles[i][1]=="brick":
            board_canvas.itemconfig(tiles[i][0][0],fill=brick_color)
        elif tiles[i][1]=="sheep":
            board_canvas.itemconfig(tiles[i][0][0],fill=sheep_color)
        elif tiles[i][1]=="wheat":
            board_canvas.itemconfig(tiles[i][0][0],fill=wheat_color)
        elif tiles[i][1]=="stone":
            board_canvas.itemconfig(tiles[i][0][0],fill=stone_color)
        else:
            board_canvas.itemconfig(tiles[i][0][0],fill=sand_color)

        # Filling numbers
        pos = board_canvas.coords(tiles[i][0][0])
        pos_x = (pos[0]+pos[6])/2
        pos_y = (pos[1]+pos[7])/2
        if tiles[i][2]>0 and tiles[i][2]<6:
            tiles[i][0][1] = board_canvas.create_text(pos_x, pos_y,
                font=("Helvetica", txt_size), text=tiles[i][2])
        elif tiles[i][2]==6 or tiles[i][2]==8:
            tiles[i][0][1] = board_canvas.create_text(pos_x, pos_y,
                font=("Helvetica", txt_size), text=tiles[i][2], fill="red")
        elif tiles[i][2]>8:
            tiles[i][0][1] = board_canvas.create_text(pos_x, pos_y,
                font=("Helvetica", txt_size), text=tiles[i][2])

    print("Tiles set")

################################################################################
# Main loop

#root = Tk()
#ex = Example(root)
root = Tk()
app = App(root)
# Draw window Width x Height
root.geometry("400x300+100+100")
root.mainloop()
