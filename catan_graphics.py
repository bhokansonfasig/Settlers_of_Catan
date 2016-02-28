from tkinter import *
from main import version, new_game, load_game
from catan_logic import legal_settlement_placements, legal_road_placements
from catan_logic import build_settlement, build_road, build_city
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
        self.parent.title("Settlers of Catan - Play")
        self.parent.geometry(board_geometry)
        # self.pack(fill=BOTH, expand=1)

        # global board
        # board = 0

        # Create splash window
        global splash
        splash = Toplevel(background=menu_color)
        splash.geometry("400x300+100+100")
        splash.title("Settlers of Catan - Welcome")
        global splash_canvas
        # splash_canvas = Canvas(splash, background=menu_color)
        # Welcome text
        game_label = Label(splash, text="Settlers of Catan",
            font=("Helvetica", 36), background=menu_color)
        game_label.pack()
        version_label = Label(splash, text="Version "+version,
            font=("Helvetica", 18), background=menu_color)
        version_label.pack(pady=30)
        # Buttons
        play_button = Button(splash, font=("Helvetica", 16), text="New Game",
            command=lambda : new_game(splash, self.parent))
        play_button.configure(width=10, activebackground = button_color)
        play_button.pack(pady=10)
        load_button = Button(splash, font=("Helvetica", 16), text="Load Game",
            command=lambda : load_game(splash, self.parent))
        load_button.configure(width=10, activebackground = button_color)
        load_button.pack(pady=10)
        quit_button = Button(splash, font=("Helvetica", 16), text="Quit",
            command=self.quit)
        quit_button.configure(width=10, activebackground = button_color)
        quit_button.pack(pady=10)

        # Create board window's canvas and items
        global board_canvas
        board_canvas = Canvas(self.parent)
        board_canvas.pack(fill=BOTH, expand=1)

        # Generate 49 tiles
        global tiles
        tiles = []
        for i in range(49):
            tiles.append(Tile(i))

        draw_tile_skeleton(tiles)

        global click_x,click_y
        click_x = IntVar()  # Tkinter variable that can be watched
        click_y = IntVar()  # Tkinter variable that can be watched
        click_x.set(0)
        click_y.set(0)

        # Define board bindings & protocols
        def click_set(event):
            """On click event, sets the x and y coordinates of the click"""
            click_x.set(event.x)
            click_y.set(event.y)
            #print(click_x.get(),click_y.get())

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
            close_all(splash,self.parent)

        # Set board bindings & protocols
        board_canvas.bind("<Button-1>", click_set)
        board_canvas.bind("<Configure>", reset_size)
        self.parent.protocol("WM_DELETE_WINDOW", user_closed)

        # Hide board window
        self.parent.withdraw()


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
    draw_stats(players)


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
        player = Player(4,name,-1)
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


def placement_loop(available_points):
    """Loops until player chooses a valid vertex, then returns its coordinate"""
    valid_position = False
    click_x.set(0)
    click_y.set(0)

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


def player_choose_settlement(player,players):
    """Asks player to click hex point on board to place settlement.
    Returns tuple of the placed settlement"""
    # # Watch for click events
    # board_canvas.bind("<Button-1>", click_set)

    # Determine the places a player can legally play
    available_points = legal_settlement_placements(player,players)

    print("Choose a vertex to place a settlement")

    coordinate = placement_loop(available_points)

    print("Chose point",coordinate)

    # # Stop watching for click events
    # board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    board_canvas.delete("circle")

    return Point(coordinate[0],coordinate[1],coordinate[2])


def player_choose_road(player,players):
    """Asks player to click two hex points on board to place road between them.
    Returns tuples of the placed road"""

    # # Watch for click events
    # board_canvas.bind("<Button-1>", click_set)

    # global click_x,click_y
    # click_x = IntVar()  # Tkinter variable that can be watched
    # click_y = IntVar()  # Tkinter variable that can be watched
    # click_x.set(0)
    # click_y.set(0)

    road_coordinates = []
    valid_road = False

    print("Choose two vertices to place a road")

    # Loop until player picks a valid road pair
    while(not(valid_road)):
        print(len(road_coordinates),"vertices chosen so far")

        # Determine the places a player can legally play
        available_roads = legal_road_placements(player,players)
        available_points = []
        for road in available_roads:
            available_points.append(road.point1)
            available_points.append(road.point2)

        # Just draw points where player can connect to first point in the second
        #  loop. Let player click on the initial point to cancel
        if len(road_coordinates)==1:
            points_to_remove = []
            for point in available_points:
                if road_coordinates[0].adjacent_point(point) or \
                    road_coordinates[0]==point:
                    #print("Point",road_coordinates[0].x,road_coordinates[0].y,
                    #    road_coordinates[0].z,"adjacent to",point.x,point.y,point.z)
                    continue
                else:
                    #print("Removing point",point.x,point.y,point.z)
                    points_to_remove.append(point)
            for point in points_to_remove:
                while point in available_points:
                    available_points.remove(point)

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
                    if road==match:
                        valid_road = True
            # If the road is not legal after all, try two new vertices
            if not(valid_road):
                road_coordinates = []

    print("Chose road",road.point1.coordinate,road.point2.coordinate)

    # # Stop watching for click events
    # board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    board_canvas.delete("circle")

    return road


def player_choose_city(player,players):
    """Asks player to click hex point on board to place city.
    Returns tuple of the placed settlement"""
    # # Watch for click events
    # board_canvas.bind("<Button-1>", click_set)

    # Determine the places a player can legally play
    available_points = []
    for point in player.settlements:
        available_points.append(point)

    print("Choose a vertex to place a city")

    coordinate = placement_loop(available_points)

    print("Chose point",coordinate)

    # # Stop watching for click events
    # board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    board_canvas.delete("circle")

    return Point(coordinate[0],coordinate[1],coordinate[2])


def draw_settlement(point, player):
    """Draws a settlement at 'point' owned by player"""
    # Get the index of the point in the player's settlements array that
    #  corresponds to this point
    matching_point = -1
    for i in range(len(player.settlements)):
        if player.settlements[i]==point:
            matching_point = i
    # If there isn't one, the player must not own this point!
    if matching_point==-1:
        return

    point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(hex_height/50)

    player.settlements[i].tk_index = board_canvas.create_polygon([x+size,y-size,
        x+size,y+size, x-size,y+size, x-size,y-size, x,y-int(1.8*size)],
        fill=player.color, outline="black", tags=("settlement",player.index))


def draw_road(road, player):
    """Draws a road owned by player"""
    # Get the index of the road in the player's roads array that
    #  corresponds to this road
    matching_road = -1
    for i in range(len(player.roads)):
        if player.roads[i]==road:
            matching_road = i
    # If there isn't one, the player must not own this road!
    if matching_road==-1:
        return

    road.point1.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    road.point2.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x_1 = road.point1.vertex[0]
    y_1 = road.point1.vertex[1]
    x_2 = road.point2.vertex[0]
    y_2 = road.point2.vertex[1]

    offset = int(hex_height/50)

    player.roads[i].tk_index = board_canvas.create_line(x_1,y_1, x_2,y_2,
        width=7, fill=player.color, tags=("road",player.index))

    board_canvas.tag_raise("settlement")
    board_canvas.tag_raise("city")


def draw_city(point, player):
    """Clears settlement at 'point' and draws a city there owned by player"""
    # Get the index of the point in the player's cities array that
    #  corresponds to this point
    matching_city = -1
    for i in range(len(player.cities)):
        if player.cities[i]==point:
            matching_city = i
    # If there isn't one, the player must not own this point!
    if matching_city==-1:
        return

    # Undraw the settlement from that point
    all_settlements = board_canvas.find_withtag("settlement")
    owned_settlements = []
    for settlement in all_settlements:
        if str(player.index) in board_canvas.gettags(settlement):
            owned_settlements.append(settlement)
    point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    size = int(hex_height/50)
    for match in owned_settlements:
        if point.vertex[0]+size in board_canvas.coords(match) and \
            point.vertex[1]+size in board_canvas.coords(match):
            board_canvas.delete(match)

    board_canvas.tag_raise("settlement")

    #point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(hex_height/50)

    player.cities[i].tk_index = board_canvas.create_polygon([
        x+2*size,y-int(1.8*size), x+2*size,y+size, x-2*size,y+size,
        x-2*size,y-size, x-size,y-int(1.8*size), x,y-size, x,y-int(1.8*size),
        x+size,y-int(3*size)], fill=player.color, outline="black",
        tags=("city",player.index))


def draw_dice(die_1,die_2):
    """Undraws previous dice and draws dice of values 'die_1' and 'die_2'"""
    board_canvas.delete("dice")

    die_width = 50
    die_height = die_width
    die_x_off = 10
    die_y_off = 10
    board_canvas.create_rectangle(die_x_off,die_y_off,
        die_x_off+die_width,die_y_off+die_height,
        fill="red", tags="dice")
    board_canvas.create_rectangle(die_x_off+die_width+20,die_y_off,
        die_x_off+die_width+20+die_width,die_y_off+die_height,
        fill="yellow", tags="dice")

    die=[die_1,die_2]
    dot_r = 5
    for i in range(2):
        # Top left and bottom right dots
        if die[i]!=1:
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center left and right dots
        if die[i]==6:
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Bottom left and top right dots
        if die[i]>=4:
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(3*die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center dot
        if die[i]%2==1:
            board_canvas.create_oval(
                die_x_off+i*(die_x_off+die_width+10)+int(2*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_x_off+die_width+10)+int(2*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")


def draw_intermediate_screen(name):
    """Draws a screen with player name between turns"""
    text_string = name+"'s turn!"
    intermediate_text_1 = board_canvas.create_text(
        int((win_width-hex_width-2*water_width)/2),int(win_height/2),
        text=text_string, width=int(.9*(win_width-hex_width-2*water_width)),
        font=("Helvetica",2*txt_size))
    intermediate_text_2 = board_canvas.create_text(
        int((win_width-hex_width-2*water_width)/2),int(win_height/2)+2*txt_size,
        text="Click to continue", font=("Helvetica",txt_size),
        width=int(.9*(win_width-hex_width-2*water_width)))
    board_canvas.wait_variable(click_x)
    board_canvas.delete(intermediate_text_1)
    board_canvas.delete(intermediate_text_2)


def draw_stats(players):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    board_canvas.delete("stats")

    portion = (win_width-hex_x_off)/len(players)
    for i in range(len(players)):
        player = players[i]
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int((hex_y_off-water_width)/4), text=player.name, fill=player.color,
            font=("Helvetica", int(.9*txt_size)), tags="stats")
        vp_string = "Victory points: "+str(player.score)
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int(2*(hex_y_off-water_width)/4), text=vp_string, fill=player.color,
            font=("Helvetica", int(.7*txt_size)), tags="stats")
        resource_string = "Resources: "+str(player.wood+player.brick+ \
            player.wheat+player.sheep+player.stone)
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int(3*(hex_y_off-water_width)/4), text=resource_string,
            fill=player.color, font=("Helvetica", int(.7*txt_size)),
            tags="stats")


def draw_buttons(player,players):
    """Draws buttons for player actions on the board window"""
    global build_settlement_button, build_road_button, build_city_button

    # Create buttons on board window
    build_settlement_button = Button(board_canvas,
        font=("Helvetica", int(.5*txt_size)), text="Build Settlement",
        command=lambda : set_button_chosen(1))
    build_settlement_button.configure(width=15, activebackground = button_color)
    build_settlement_button_window = board_canvas.create_window(100, 100,
        window=build_settlement_button, tags="button")
    build_road_button = Button(board_canvas,
        font=("Helvetica", int(.5*txt_size)), text="Build Road",
        command=lambda : set_button_chosen(2))
    build_road_button.configure(width=15, activebackground = button_color)
    build_road_button_window = board_canvas.create_window(100, 125,
        window=build_road_button, tags="button")
    build_city_button = Button(board_canvas,
        font=("Helvetica", int(.5*txt_size)), text="Build City",
        command=lambda : set_button_chosen(3))
    build_city_button.configure(width=15, activebackground = button_color)
    build_city_button_window = board_canvas.create_window(100, 150,
        window=build_city_button, tags="button")
    end_turn_button = Button(board_canvas,
        font=("Helvetica", int(.5*txt_size)), text="End Turn",
        command=lambda : set_button_chosen(0))
    end_turn_button.configure(width=15, activebackground = button_color)
    end_turn_button_window = board_canvas.create_window(100, 175,
        window=end_turn_button, tags="button")


def set_button_chosen(integer):
    """Sets the button_chosen variable to value 'integer'"""
    button_chosen.set(integer)


def undraw_buttons():
    """Undraws and deletes all player action buttons from window"""
    board_canvas.delete("button")
    build_settlement_button.destroy()
    build_road_button.destroy()
    build_city_button.destroy()


def draw_resources(player):
    """Undraws any current resources shown and draws resources of player"""
    board_canvas.delete("resources")

    wood_text = "Wood: "+str(player.wood)
    brick_text = "Brick: "+str(player.brick)
    sheep_text = "Sheep: "+str(player.sheep)
    wheat_text = "Wheat: "+str(player.wheat)
    stone_text = "Stone: "+str(player.stone)

    board_canvas.create_text(100,250, text=wood_text,
        font=("Helvetica", int(.7*txt_size)), tags="resources")
    board_canvas.create_text(100,275, text=brick_text,
        font=("Helvetica", int(.7*txt_size)), tags="resources")
    board_canvas.create_text(100,300, text=sheep_text,
        font=("Helvetica", int(.7*txt_size)), tags="resources")
    board_canvas.create_text(100,325, text=wheat_text,
        font=("Helvetica", int(.7*txt_size)), tags="resources")
    board_canvas.create_text(100,350, text=stone_text,
        font=("Helvetica", int(.7*txt_size)), tags="resources")



def draw_resource_panel(player,players):
    """Draws resources available to player number 'index' in the resource panel
    of the board window. Also activates buttons available to player."""

    draw_buttons(player,players)

    draw_resources(player)

    # # Temporary terminal actions for player
    # action = input("What would you like to do? ")
    # if action=="build settlement" or action=="bs":
    #     if legal_settlement_placements(player,players):
    #         build_settlement(player,players)
    #     else:
    #         print("Nowhere to legally build a new settlement!")
    # elif action=="build road" or action=="br":
    #     if legal_road_placements(player,players):
    #         build_road(player,players)
    #     else:
    #         print("Nowhere to legally build a new road!")
    # elif action=="build city" or action=="bc":
    #     if len(player.settlements)>0:
    #         build_city(player,players)
    #     else:
    #         print("Nowhere to legally build a new city!")
    # else:
    #     pass


def clear_resource_panel():
    """Clears out all resources from the resource panel of the board window.
    Also dims all button states."""

    undraw_buttons()
    board_canvas.delete("resources")


def turn_loop(player,players):
    global button_chosen
    button_chosen = IntVar()
    button_chosen.set(-1)
    while button_chosen.get()!=0:
        draw_stats(players)
        draw_resources(player)
        board_canvas.wait_variable(button_chosen)
        if button_chosen.get()==1:
            build_settlement(player,players)
        elif button_chosen.get()==2:
            build_road(player,players)
        elif button_chosen.get()==3:
            build_city(player,players)


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    aesthetics(900,600)
    print(wood_color)
