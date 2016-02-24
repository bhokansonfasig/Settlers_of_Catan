from tkinter import *
from main import version, new_game, load_game
from tiles import Tile


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

        # Generate 49 tiles
        global tiles
        tiles = []
        for i in range(49):
            tiles.append(Tile(i))

        draw_tile_skeleton(tiles)

        # Define board bindings & protocols
        def reset_size(event):
            """Resizes board elements when the window size is changed."""
            win_width = event.width
            win_height = event.height
            aesthetics(win_width,win_height)
            board_canvas.delete(ALL)
            draw_tile_skeleton(tiles)
            draw_tiles(tiles)

        def user_closed():
            """Closes board window nicely if user manually closes it."""
            # Later may use this to create saves
            board_canvas.delete(ALL)
            close_board_window(self.parent,board)

        # def click_return_circles(event):
        #     """Returns tags of circles near clicked pixel."""
        #     objects = board_canvas.find_enclosed(event.x-35, event.y-35,
        #         event.x+35, event.y+35)
        #     for obj in objects:
        #         print(board_canvas.gettags(obj))


        # Set board bindings & protocols
        board_canvas.bind("<Configure>", reset_size)
        #board_canvas.bind("<Button-1>", click_return_circles)
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
    menu_color,button_color,sand_color,wood_color,brick_color,sheep_color, \
        wheat_color,stone_color = set_colors()

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
    if win_width>=win_height:
        hex_height = win_height*75/100
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


def set_colors():
    """Returns menu, button, sand, wood, brick, sheep, wheat, and stone colors
        in that order"""
    # menu_color = "#EECC8C"
    # button_color = "#FFFFCC"
    # sand_color = "#D7B992"
    # wood_color = "#2C8236"
    # brick_color = "#8B0000"
    # sheep_color = "#A6FFA6"
    # wheat_color = "#F5B800"
    # stone_color = "#686868"
    return "#EECC8C","#FFFFCC","#D7B992","#2C8236","#8B0000","#A6FFA6", \
        "#F5B800","#686868"


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


def close_all(splash,board):
    """Closes all windows to quit app"""
    print("Closing all windows")
    try:
        splash.destroy()
        board.destroy()
    except:
        pass


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


def draw_tile_skeleton(tiles):
    """Draws the outlines for the hexagon tiles"""
    # Water base
    board_canvas.create_rectangle(hex_x_off-water_width,
        hex_y_off-water_width, win_width, win_height, fill="#6680FF")

    for tile in tiles:
        tile.set_vertices(hex_width, hex_height, hex_x_off, hex_y_off)
        if tile.visible:
            tile.draw_skeleton(board_canvas)
            tile.draw(board_canvas)
            tile.draw_number(board_canvas,txt_size)

    #     # Circles at hexagon vertices for settlement / road placement
    #     r = int(hex_height/25)
    #     for j in [0,2,4,6,8,10]:
    #         board_canvas.create_oval(vertices[j]-r,vertices[j+1]-r,
    #             vertices[j]+r,vertices[j+1]+r, width=3, tags=("circle",i))
    #
    # board_canvas.tag_lower("circle")


def draw_tiles(tiles):
    """Draws tiles on game board window"""
    for tile in tiles:
        tile.set_vertices(hex_width, hex_height, hex_x_off, hex_y_off)
        if tile.visible:
            tile.draw_skeleton(board_canvas)
            tile.draw(board_canvas)
            tile.draw_number(board_canvas,txt_size)


def draw_stats(stats):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    pass


def click_return_coordinate(event):
    global coordinate
    coordinate = []
    objects = board_canvas.find_enclosed(event.x-35, event.y-35,
        event.x+35, event.y+35)
    for obj in objects:
        tags = board_canvas.gettags(obj)
        for tag in tags:
            if eval(tag)>0 and eval(tag)<50:
                coordinate.append(eval(tag))


def player_place_settlement(player_index):
    """Asks player to click hex point on board to place settlement. Returns
    tuple of the placed settlement"""
    board_canvas.tag_raise("circle")

    board_canvas.bind("<Button-1>", click_return_coordinate)

    coordinate = []

    # valid_coordinate = False
    # while valid_coordinate==False:
    #     print(coordinate)
    #     if len(coordinate)==3:
    #         valid_coordinate = True
    #
    # print(coordinate)

    board_canvas.unbind("<Button-1>")

    board_canvas.tag_lower("circle")

    return coordinate


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
    aesthetics(900,600)
    print(wood_color)
