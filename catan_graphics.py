from tkinter import *
from main import version, new_game, load_game


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

        global board
        board = 0

        splash_canvas = Canvas(self, background=menu_color)
        # Welcome text
        splash_canvas.create_text(200, 50, font=("Helvetica", 36),
            text="Settlers of Catan")
        splash_canvas.create_text(200, 100, font=("Helvetica", 18),
            text="Version "+version)
        splash_canvas.pack(fill=BOTH, expand=1)
        # Buttons
        play_button = Button(splash_canvas, font=("Helvetica", 16),
            text="New Game", command=lambda : new_game(self.parent, board))
        play_button.configure(width=10, activebackground = button_color)
        play_button_window = splash_canvas.create_window(100, 200,
            window=play_button)
        load_button = Button(splash_canvas, font=("Helvetica", 16),
            text="Load Game", command=lambda : load_game(self.parent, board))
        load_button.configure(width=10, activebackground = button_color)
        load_button_window = splash_canvas.create_window(300, 200,
            window=load_button)
        quit_button = Button(splash_canvas, font=("Helvetica", 16),
            text="Quit", command=self.quit)
        quit_button.configure(width=10, activebackground = button_color)
        quit_button_window = splash_canvas.create_window(200, 250,
            window=quit_button)

        # Create and hide board window
        board = Toplevel()
        board.geometry(board_geometry)
        board.title("Settlers of Catan - Play")
        global board_canvas
        board_canvas = Canvas(board)
        board_canvas.pack(fill=BOTH, expand=1)
        board.withdraw()

        # 49 tiles with attributes:
        #  0 - tkinter index numbers: [hexagon, number]
        #  1 - tile resource type
        #  2 - tile dice roll number
        #  3 - array of owners of settlement points (up to 6; i.e. 3 cities)
        #  4 - array of owners of road sides (up to 6)
        global tiles
        tiles = []
        for i in range(49):
            tiles.append([[-1,-1], "none", -1, [], []])

        draw_tile_skeleton()

        # Define board bindings & protocols
        def reset_size(event):
            """Resizes board elements when the window size is changed."""
            win_width = event.width
            win_height = event.height
            aesthetics(win_width,win_height)
            board_canvas.delete(ALL)
            draw_tile_skeleton()
            draw_tiles(tiles)

        def user_closed():
            """Closes board window nicely if user manually closes it."""
            # Later may use this to create saves
            close_board_window(self.parent,board)

        # Set board bindings & protocols
        board_canvas.bind("<Configure>", reset_size)
        board.protocol("WM_DELETE_WINDOW", user_closed)


################################################################################
# Function definitions

def aesthetics(width,height):
    """Defines aesthetic parameters for the GUI"""

    # Define window dimensions and colors
    global win_width, win_height, menu_color, button_color, sand_color
    global wood_color, brick_color, sheep_color, wheat_color, stone_color

    win_width = width
    win_height = height
    menu_color = "#EECC8C"
    button_color = "#FFFFCC"
    sand_color = "#D7B992"
    wood_color = "#2C8236"
    brick_color = "#8B0000"
    sheep_color = "#A6FFA6"
    wheat_color = "#F5B800"
    stone_color = "#686868"

    global txt_size
    if win_height<167:
        txt_size = 5
    elif win_height>1200:
        txt_size = 36
    else:
        txt_size = int(.03*win_height)

    # Raise errors for strange dimensions
    if 2*win_width>3.1*win_height or 2*win_width<2.9*win_height:
        print("Board dimensions are incorrect, some elements may appear",
            "distorted.")
    if win_width<500 or win_height<500:
        print("Board window too small, some features may not appear properly.")

    # Geometry for board window
    global board_geometry
    board_geometry = "%dx%d+50+50" % (win_width,win_height)

    # Set width and height of hexagon section
    global hex_height, hex_width
    hex_height = win_height*75/100
    if win_width>=win_height:
        hex_width = hex_height
    else:
        hex_width = win_width*75/100
        hex_height = hex_width

    # Set width of water region
    global water_width
    water_width = int(hex_width/10)

    # Set offsets from top right corner for hexagon section (without water)
    global hex_x_off, hex_y_off
    hex_x_off = int(win_width-hex_width-water_width)
    hex_y_off = int(win_height-hex_height-water_width)

    return width, height


def open_board_window(splash,board):
    """Hides splash window and reveals board window"""
    splash.withdraw()
    board.update()
    board.deiconify()


def close_board_window(splash,board):
    """Hides board window and reveals splash window"""
    board.withdraw()
    splash.update()
    splash.deiconify()


def set_players():
    """Gets the number and type of players and returns an array of this info"""
    # Players array, one row for each player
    #  0 - Player index (1-4)
    #  1 - Name (string)
    #  2 - AI difficulty (-1 for human player)
    players = [[1,"nobody",0],[2,"nobody",0],[3,"nobody",0],[4,"nobody",0]]
    playnum = 0
    compnum = 0

    # Command line implementation; pretty broken honestly...
    while (playnum<=1 or playnum>=5) or (compnum<=-1 or compnum>=5):
        playnum = eval(input("Total number of players: "))
        compnum = eval(input("Number of computer players: "))
    if playnum==compnum:
        players[0][1] = "Computer 1"
        players[0][2] = eval(input("Computer 1 level: "))
    else:
        players[0][1] = input("Player 1 name: ")
        players[0][2] = -1
    if playnum<=compnum+1:
        players[1][1] = "Computer 2"
        players[1][2] = eval(input("Computer 2 level: "))
    else:
        players[1][1] = input("Player 2 name: ")
        players[1][2] = -1
    if playnum<=compnum+2 and playnum>=3:
        players[2][1] = "Computer 3"
        players[2][2] = eval(input("Computer 3 level: "))
    elif playnum>=3:
        players[2][1] = input("Player 3 name: ")
        players[2][2] = -1
    if playnum<=compnum+3 and playnum==4:
        players[3][1] = "Computer 4"
        players[3][2] = eval(input("Computer 4 level: "))
    elif playnum==4:
        players[3][1] = input("Player 4 name: ")
        players[3][2] = -1

    # Get rid of extra players from array
    if playnum<4:
        players.pop(3)
    if playnum<3:
        players.pop(2)

    return players


def get_tiles():
    """Returns tile array"""
    return tiles


def draw_tile_skeleton():
    hex9_points = [
        int(hex_width*2/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
    hex10_points = [
        int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
    hex11_points = [
        int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*1/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*0/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*1/16)+hex_y_off]
    hex16_points = [
        int(hex_width*1/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
    hex17_points = [
        int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
    hex18_points = [
        int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
    hex19_points = [
        int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*4/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*3/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*4/16)+hex_y_off]
    hex22_points = [
        int(hex_width*0/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*0/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*0/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
    hex23_points = [
        int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
    hex24_points = [
        int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
    hex25_points = [
        int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
    hex26_points = [
        int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*10/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*10/10)+hex_x_off,int(hex_height*7/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*6/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*7/16)+hex_y_off]
    hex30_points = [
        int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*1/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
    hex31_points = [
        int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
    hex32_points = [
        int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
    hex33_points = [
        int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*9/10)+hex_x_off,int(hex_height*10/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*9/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*10/16)+hex_y_off]
    hex37_points = [
        int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*3/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*2/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]
    hex38_points = [
        int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*5/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*4/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]
    hex39_points = [
        int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*16/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*15/16)+hex_y_off,
        int(hex_width*8/10)+hex_x_off,int(hex_height*13/16)+hex_y_off,
        int(hex_width*7/10)+hex_x_off,int(hex_height*12/16)+hex_y_off,
        int(hex_width*6/10)+hex_x_off,int(hex_height*13/16)+hex_y_off]

    board_canvas.create_rectangle(hex_x_off-water_width,
        hex_y_off-water_width, win_width, win_height, fill="#6680FF")

    tiles[9][0][0] = board_canvas.create_polygon(hex9_points,
        outline=sand_color, fill='white', width=4)
    tiles[10][0][0] = board_canvas.create_polygon(hex10_points,
        outline=sand_color, fill='white', width=4)
    tiles[11][0][0] = board_canvas.create_polygon(hex11_points,
        outline=sand_color, fill='white', width=4)
    tiles[16][0][0] = board_canvas.create_polygon(hex16_points,
        outline=sand_color, fill='white', width=4)
    tiles[17][0][0] = board_canvas.create_polygon(hex17_points,
        outline=sand_color, fill='white', width=4)
    tiles[18][0][0] = board_canvas.create_polygon(hex18_points,
        outline=sand_color, fill='white', width=4)
    tiles[19][0][0] = board_canvas.create_polygon(hex19_points,
        outline=sand_color, fill='white', width=4)
    tiles[22][0][0] = board_canvas.create_polygon(hex22_points,
        outline=sand_color, fill='white', width=4)
    tiles[23][0][0] = board_canvas.create_polygon(hex23_points,
        outline=sand_color, fill='white', width=4)
    tiles[24][0][0] = board_canvas.create_polygon(hex24_points,
        outline=sand_color, fill='white', width=4)
    tiles[25][0][0] = board_canvas.create_polygon(hex25_points,
        outline=sand_color, fill='white', width=4)
    tiles[26][0][0] = board_canvas.create_polygon(hex26_points,
        outline=sand_color, fill='white', width=4)
    tiles[30][0][0] = board_canvas.create_polygon(hex30_points,
        outline=sand_color, fill='white', width=4)
    tiles[31][0][0] = board_canvas.create_polygon(hex31_points,
        outline=sand_color, fill='white', width=4)
    tiles[32][0][0] = board_canvas.create_polygon(hex32_points,
        outline=sand_color, fill='white', width=4)
    tiles[33][0][0] = board_canvas.create_polygon(hex33_points,
        outline=sand_color, fill='white', width=4)
    tiles[37][0][0] = board_canvas.create_polygon(hex37_points,
        outline=sand_color, fill='white', width=4)
    tiles[38][0][0] = board_canvas.create_polygon(hex38_points,
        outline=sand_color, fill='white', width=4)
    tiles[39][0][0] = board_canvas.create_polygon(hex39_points,
        outline=sand_color, fill='white', width=4)


def draw_tiles(tiles):
    """Draws tiles on game board window"""
    global active_tiles
    active_tiles = [9,10,11,16,17,18,19,22,23,24,25,26,30,31,32,33,37,38,39]

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


def draw_stats(stats):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    pass


def player_place_settlement(player_index):
    """Asks player to click hex point on board to place settlement. Returns
    tuple of the placed settlement"""

    return (0,1,2)


def player_place_road(player_index):
    """Asks player to click two hex points on board to place road between them.
    Returns tuples of the placed road"""

    return ((0,1,2),(1,2,3))


def computer_place_settlement(player_index):
    """Has computer place settlement. Returns tuple of the placed settlement"""

    return (0,1,2)


def computer_place_road(player_index):
    """Has computer place road. Returns tuples of the placed road"""

    return ((0,1,2),(1,2,3))


def draw_settlement(point, player_index):
    """Draws a settlement at 'point' owned by player number 'index'"""
    pass


def draw_road(side, player_index):
    """Draws a road on 'side' owned by player number 'index'"""
    pass


def draw_city(point, player_index):
    """Clears the settlement at 'point' and draws a city there owned by player
    number 'index'"""
    pass


def draw_dice(die_1,die_2):
    """Draws dice of values 'die_1' and 'die_2'."""
    pass


def draw_resource_panel(player_index):
    """Draws resources available to player number 'index' in the resource panel
    of the board window. Also activates buttons available to player."""
    pass


def clear_resource_panel():
    """Clears out all resources from the resource panel of the board window.
    Also dims all button states."""
    pass


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    print(version)
