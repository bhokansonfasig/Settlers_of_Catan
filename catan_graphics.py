from tkinter import *
from main import version, new_game, load_game
from catan_logic import legal_settlement_placements, legal_road_placements
from player import Player
from tiles import Tile
from point import Point
from road import Road


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

        global splash_canvas
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
            redraw_board()


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
    menu_color = set_color("menu")
    button_color = set_color("button")
    sand_color = set_color("sand")
    wood_color = set_color("wood")
    brick_color = set_color("brick")
    sheep_color = set_color("sheep")
    wheat_color = set_color("wheat")
    stone_color = set_color("stone")

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


def set_color(element):
    """Returns color of requested element (options: menu, button, sand, wood,
        brick, sheep, wheat, stone)"""
    if element.lower()=="menu":
        return "#EECC8C"
    if element.lower()=="button":
        return "#FFFFCC"
    if element.lower()=="sand":
        return "#D7B992"
    if element.lower()=="wood":
        return "#2C8236"
    if element.lower()=="brick":
        return "#8B0000"
    if element.lower()=="sheep":
        return "#A6FFA6"
    if element.lower()=="wheat":
        return "#F5B800"
    if element.lower()=="stone":
        return "#686868"


def redraw_board():
    from main import players
    board_canvas.delete(ALL)
    draw_tile_skeleton(tiles)
    draw_tiles(tiles)
    for player in players:
        for road in player.roads:
            draw_road(road,player)
        for settlement in player.settlements:
            draw_settlement(settlement,player)
        for city in player.cities:
            draw_city(city,player)


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
    # players = [[1,"nobody",0],[2,"nobody",0],[3,"nobody",0],[4,"nobody",0]]
    players = []
    playnum = 0
    compnum = 0

    # Command line implementation; pretty broken honestly...
    while (playnum<=1 or playnum>=5) or (compnum<=-1 or compnum>=5):
        playnum = eval(input("Total number of players: "))
        compnum = eval(input("Number of computer players: "))
    if playnum==compnum:
        level = eval(input("Computer 1 level: "))
        player = Player(1,"Computer 1",level)
        players.append(player)
    else:
        name = input("Player 1 name: ")
        player = Player(1,name,-1)
        players.append(player)
    if playnum<=compnum+1:
        level = eval(input("Computer 2 level: "))
        player = Player(2,"Computer 2",level)
        players.append(player)
    else:
        name = input("Player 2 name: ")
        player = Player(2,name,-1)
        players.append(player)
    if playnum<=compnum+2 and playnum>=3:
        level = eval(input("Computer 3 level: "))
        player = Player(3,"Computer 3",level)
        players.append(player)
    elif playnum>=3:
        name = input("Player 3 name: ")
        player = Player(3,name,-1)
        players.append(player)
    if playnum<=compnum+3 and playnum==4:
        level = eval(input("Computer 4 level: "))
        player = Player(4,"Computer 4",level)
        players.append(player)
    elif playnum==4:
        name = input("Player 4 name: ")
        player = Player(3,name,-1)
        players.append(player)

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


def draw_tiles(tiles):
    """Draws tiles on game board window"""
    for tile in tiles:
        if tile.visible:
            tile.draw(board_canvas)
            tile.draw_number(board_canvas,txt_size)


def draw_circle(point):
    """Draws a circle around the vertex at point, as long as the point is
        valid"""
    r = int(hex_height/25)
    if point.valid:
        point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
        board_canvas.create_oval(point.vertex[0]-r,point.vertex[1]-r,
            point.vertex[0]+r,point.vertex[1]+r, width=3, tags="circle")


def draw_stats(players):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    pass


def click_set(event):
    """On click event, sets the x and y coordinates of the click"""
    click_x.set(event.x)
    click_y.set(event.y)
    #print(click_x.get(),click_y.get())


def placement_loop(available_points):
    """Loops until player chooses a valid vertex, then returns its coordinate"""
    global click_x,click_y
    click_x = IntVar()  # Tkinter variable that can be watched
    click_y = IntVar()  # Tkinter variable that can be watched
    click_x.set(0)
    click_y.set(0)

    valid_position = False

    # Wait for the player to click a valid vertex
    while(not(valid_position)):
        coordinate = []
        # Draw the circles for the valid plays
        #  (after clearing any existing circles)
        board_canvas.delete("circle")
        for pt in available_points:
            draw_circle(pt)
        print("\tClick on a valid vertex (circled)")
        # Get the hexagons with vertices near the point clicked
        for tile in tiles:
            for i in range(0,12,2):
                if click_x.get()>tile.vertices[i]-10 and \
                    click_x.get()<tile.vertices[i]+10 and \
                    click_y.get()>tile.vertices[i+1]-10 and \
                    click_y.get()<tile.vertices[i+1]+10:
                    coordinate.append(tile.index)
                    break
        # Check that the vertex is a legal one
        if len(coordinate)==3:
            coordinate.sort()
            for match in available_points:
                if coordinate==match.coordinate:
                    valid_position = True
        # If the point clicked is not a legal vertex, try again
        if not(valid_position):
            board_canvas.wait_variable(click_x)

    return coordinate


def player_place_settlement(player,players):
    """Asks player to click hex point on board to place settlement. Returns
    tuple of the placed settlement"""
    # Watch for click events
    board_canvas.bind("<Button-1>", click_set)

    # Determine the places a player can legally play
    available_points = legal_settlement_placements(player,players)

    print("Choose a vertex to place a settlement")

    coordinate = placement_loop(available_points)

    print("Chose point",coordinate)

    # Stop watching for click events
    board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    board_canvas.delete("circle")

    return Point(coordinate[0],coordinate[1],coordinate[2])


def player_place_road(player,players):
    """Asks player to click two hex points on board to place road between them.
    Returns tuples of the placed road"""

    # Watch for click events
    board_canvas.bind("<Button-1>", click_set)

    # Determine the places a player can legally play
    available_roads = legal_road_placements(player,players)
    available_points = []
    for road in available_roads:
        available_points.append(road.point1)
        available_points.append(road.point2)

    global click_x,click_y
    click_x = IntVar()  # Tkinter variable that can be watched
    click_y = IntVar()  # Tkinter variable that can be watched
    click_x.set(0)
    click_y.set(0)

    road_coordinates = []
    valid_road = False

    print("Choose two vertices to place a road")

    # Loop until player picks a valid road pair
    while(not(valid_road)):
        print(len(road_coordinates),"vertices chosen so far")
        # Wait for the player to click a valid vertex
        coordinate = placement_loop(available_points)

        # Add selected vertex to the road coordinates
        road_coordinates.append(Point(coordinate[0],coordinate[1],
            coordinate[2]))

        # Set variables to loop again
        valid_position = False
        click_x.set(0)
        click_y.set(0)

        # If there are two road coordinates, check if they make a valid road
        if len(road_coordinates)==2:
            road = Road(road_coordinates[0],road_coordinates[1])
            if road.valid:
                for match in available_roads:
                    if road.point1.coordinate==match.point1.coordinate and \
                        road.point2.coordinate==match.point2.coordinate:
                        valid_road = True
            # If the road is not legal after all, try two new vertices
            if not(valid_road):
                road_coordinates = []

    print("Chose road",road.point1.coordinate,road.point2.coordinate)

    # Stop watching for click events
    board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    board_canvas.delete("circle")

    return road


def computer_place_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""

    return Point(0,1,7)


def computer_place_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""

    return Road(Point(0,1,7),Point(1,7,8))


def draw_settlement(point, player):
    """Draws a settlement at 'point' owned by player"""
    # Make sure the player actually owns the point
    #if player.settlements[-1].coordinate!=point.coordinate:
    #    return

    point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(hex_height/50)

    board_canvas.create_polygon([x+size,y-size, x+size,y+size, x-size,y+size,
        x-size,y-size, x,y-int(1.8*size)], fill=player.color, outline="black",
        tags=("settlement",player.index))


def draw_road(road, player):
    """Draws a road owned by player"""
    # Make sure the player actually owns the road
    #if player.roads[-1].coordinates!=road.coordinates:
    #    return

    road.point1.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    road.point2.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x_1 = road.point1.vertex[0]
    y_1 = road.point1.vertex[1]
    x_2 = road.point2.vertex[0]
    y_2 = road.point2.vertex[1]

    offset = int(hex_height/50)

    board_canvas.create_line(x_1,y_1, x_2,y_2, width=7, fill=player.color,
        tags=("road",player.index))

    board_canvas.tag_raise("settlement")
    board_canvas.tag_raise("city")


def draw_city(point, player):
    """Clears the settlement at 'point' and draws a city there owned by player
    number 'index'"""
    # Make sure the player actually owns the point
    #if player.cities[-1].coordinate!=point.coordinate:
    #    return

    point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(hex_height/50)

    board_canvas.create_polygon([x+2*size,y-int(1.8*size), x+2*size,y+size,
        x-2*size,y+size, x-2*size,y-size, x-size,y-int(1.8*size), x,y-size,
        x,y-int(1.8*size), x+size,y-int(3*size)], fill=player.color,
        outline="black", tags=("settlement",player.index))


def draw_dice(die_1,die_2):
    """Draws dice of values 'die_1' and 'die_2'."""
    pass


def draw_resource_panel(player):
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
