from tkinter import *
from main import version, new_game, load_game
from catan_logic import legal_settlement_placements, legal_road_placements
from catan_logic import build_settlement, build_road, build_city
from player import Player
from tiles import Tile
from point import Point
from road import *


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

        # Create splash window
        global splash
        splash = Toplevel(background=menu_color)
        #splash.geometry("400x300+100+100")
        splash.title("Settlers of Catan - Welcome")
        global splash_canvas
        # splash_canvas = Canvas(splash, background=menu_color)
        # Welcome text
        game_label = Label(splash, text="Settlers of Catan",
            font=(txt_font,36), background=menu_color)
        game_label.pack()
        version_label = Label(splash, text="Version "+version,
            font=(txt_font,18), background=menu_color)
        version_label.pack(pady=30)
        # Buttons
        play_button = Button(splash, font=(txt_font,16), text="New Game",
            command=lambda : new_game(splash, self.parent))
        play_button.configure(width=10, activebackground=active_button_color)
        play_button.pack(pady=10)
        load_button = Button(splash, font=(txt_font,16), text="Load Game",
            command=lambda : load_game(splash, self.parent))
        load_button.configure(width=10, activebackground=active_button_color)
        load_button.pack(pady=10)
        quit_button = Button(splash, font=(txt_font,16), text="Quit",
            command=self.quit)
        quit_button.configure(width=10, activebackground=active_button_color)
        quit_button.pack(pady=10)

        # Create player selection window
        global player_window
        player_window = Toplevel(background=menu_color)
        #player_window.geometry("470x350+300+100")
        player_window.title("Settlers of Catan - Select Players")

        global player_1_type,player_1_name, player_2_type,player_2_name
        global player_3_type,player_3_name, player_4_type,player_4_name
        player_type_options = ["Human","Computer","None"]
        player_1_label = Label(player_window, text="Player 1:",
            font=(txt_font,22), background=menu_color)
        player_1_label.grid(row=0,column=0,padx=20,pady=10)
        player_1_type = StringVar()
        player_1_type.set(player_type_options[1])
        player_1_type_menu = OptionMenu(player_window, player_1_type,
            *player_type_options)
        player_1_type_menu.grid(row=1,column=0,padx=20,pady=10)
        player_1_name = StringVar()
        player_1_name.set("Player 1")
        player_1_name_entry = Entry(player_window, textvariable=player_1_name)
        player_1_name_entry.grid(row=2,column=0,padx=20,pady=5)
        player_2_label = Label(player_window, text="Player 2:",
            font=(txt_font,22), background=menu_color)
        player_2_label.grid(row=0,column=1,padx=20,pady=10)
        player_2_type = StringVar()
        player_2_type.set(player_type_options[1])
        player_2_type_menu = OptionMenu(player_window, player_2_type,
            *player_type_options)
        player_2_type_menu.grid(row=1,column=1,padx=20,pady=10)
        player_2_name = StringVar()
        player_2_name.set("Player 2")
        player_2_name_entry = Entry(player_window, textvariable=player_2_name)
        player_2_name_entry.grid(row=2,column=1,padx=20,pady=5)
        player_3_label = Label(player_window, text="Player 3:",
            font=(txt_font,22), background=menu_color)
        player_3_label.grid(row=3,column=0,padx=20,pady=10)
        player_3_type = StringVar()
        player_3_type.set(player_type_options[1])
        player_3_type_menu = OptionMenu(player_window, player_3_type,
            *player_type_options)
        player_3_type_menu.grid(row=4,column=0,padx=20,pady=10)
        player_3_name = StringVar()
        player_3_name.set("Player 3")
        player_3_name_entry = Entry(player_window, textvariable=player_3_name)
        player_3_name_entry.grid(row=5,column=0,padx=20,pady=5)
        player_4_label = Label(player_window, text="Player 4:",
            font=(txt_font,22), background=menu_color)
        player_4_label.grid(row=3,column=1,padx=20,pady=10)
        player_4_type = StringVar()
        player_4_type.set(player_type_options[1])
        player_4_type_menu = OptionMenu(player_window, player_4_type,
            *player_type_options)
        player_4_type_menu.grid(row=4,column=1,padx=20,pady=10)
        player_4_name = StringVar()
        player_4_name.set("Player 4")
        player_4_name_entry = Entry(player_window, textvariable=player_4_name)
        player_4_name_entry.grid(row=5,column=1,padx=20,pady=5)

        global button_chosen
        button_chosen = IntVar()
        button_chosen.set(-1)

        ready_button = Button(player_window, font=(txt_font,16),
            text="Okay", command=lambda : set_button_chosen(1))
        ready_button.configure(width=10, activebackground=active_button_color)
        ready_button.grid(row=6,pady=30,columnspan=2)

        # Hide player selection window
        player_window.withdraw()


        # Create board window's canvas and items
        global board_canvas
        board_canvas = Canvas(self.parent, background=background_color)
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
            # Get out of any waiting that was happening
            set_button_chosen(-1)
            click_set(Point(0,0,0))  # Just needs to have .x and .y attributes
            # Clear board
            board_canvas.delete(ALL)
            # Close all windows
            close_all(splash,self.parent)

        # Set board bindings & protocols
        board_canvas.bind("<Button-1>", click_set)
        board_canvas.bind("<Configure>", reset_size)
        self.parent.protocol("WM_DELETE_WINDOW", user_closed)

        # Prevent manual closing of player window
        player_window.protocol("WM_DELETE_WINDOW", user_closed)

        # Hide board window
        self.parent.withdraw()


################################################################################
# Function definitions

def aesthetics(width,height):
    """Defines aesthetic parameters for the GUI"""

    # Define window dimensions and colors
    global win_width, win_height, menu_color, background_color
    global active_button_color, inactive_button_color, sand_color
    global wood_color, brick_color, sheep_color, wheat_color, stone_color

    win_width = width
    win_height = height
    menu_color = set_color("menu")
    background_color = set_color("background")
    active_button_color = set_color("active button")
    inactive_button_color = set_color("inactive button")
    sand_color = set_color("sand")
    wood_color = set_color("wood")
    brick_color = set_color("brick")
    sheep_color = set_color("sheep")
    wheat_color = set_color("wheat")
    stone_color = set_color("stone")

    global txt_font, txt_size
    txt_font = "Helvetica"

    if win_height<167:
        txt_size = 5
    elif win_height>1200:
        txt_size = 36
    else:
        txt_size = int(.03*win_height)

    # Raise errors for strange dimensions
    if 625*win_width>1.1*900*win_height or 625*win_width<.9*900*win_height:
        print("Board dimensions are incorrect, some elements may appear",
            "distorted.")
    if win_width<500 or win_height<500:
        print("Board window too small, some features may not appear properly.")

    # Geometry for board window
    global board_geometry
    board_geometry = "%dx%d" % (win_width,win_height)

    # Set width and height of hexagon section
    global hex_height, hex_width
    if win_width>=win_height:
        hex_height = win_height*.7
        hex_width = hex_height
    else:
        hex_width = win_width*.7
        hex_height = hex_width

    # Set width of water region
    global water_width
    water_width = int(hex_width/10)

    # Set offsets from top right corner for hexagon section (without water)
    global hex_x_off, hex_y_off
    hex_x_off = int(win_width-hex_width-1.75*water_width)
    hex_y_off = int(win_height-hex_height-water_width)

    return width, height


def set_color(element):
    """Returns color of requested element (options: menu, button, sand, wood,
        brick, sheep, wheat, stone)"""
    if element.lower()=="menu":
        return "#EECC8C"
    if element.lower()=="background":
        return "#F7D9B2"
    if element.lower()=="active button":
        return "#FFFFCC"
    if element.lower()=="inactive button":
        return "#F7D9B2"
    if element.lower()=="water":
        return "#6680FF"
    if element.lower()=="sand":
        return "#D7B992"
    if element.lower()=="dock" or element.lower()=="any" or \
        element.lower()=="?":
        return "#996633"
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
    from main import players, loop_index, all_computers
    board_canvas.delete(ALL)
    draw_tile_skeleton(tiles)
    draw_tiles(tiles)
    undraw_log()
    draw_log()
    for player in players:
        for road in player.roads:
            draw_road(road,player)
        for settlement in player.settlements:
            draw_settlement(settlement,player)
        for city in player.cities:
            draw_city(city,player)
    draw_stats(players)
    if loop_index>=0:
        try:
            from main import die_1, die_2
        except:
            return
        draw_dice(die_1,die_2)
        whose_turn = loop_index%len(players) + 1
        if not(all_computers):
            draw_resource_panel(players[whose_turn-1])


def open_board_window(other,board):
    """Hides splash window and reveals board window"""
    other.withdraw()
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
        undraw_log()
        splash.destroy()
        player_window.destroy()
        board.destroy()
    except:
        print("Couldn't close windows")
        pass


def set_players(board):
    """Gets the number and type of players and returns an array of player
        objects"""
    # # Command line implementation; pretty broken honestly...
    # playnum = 0
    # compnum = 0
    # while (playnum<=1 or playnum>=5) or (compnum<=-1 or compnum>=5):
    #     playnum = eval(input("Total number of players: "))
    #     compnum = eval(input("Number of computer players: "))
    # if playnum==compnum:
    #     level = eval(input("Computer 1 level: "))
    #     player = Player(1,"Computer 1",level)
    #     players.append(player)
    # else:
    #     name = input("Player 1 name: ")
    #     player = Player(1,name,-1)
    #     players.append(player)
    # if playnum<=compnum+1:
    #     level = eval(input("Computer 2 level: "))
    #     player = Player(2,"Computer 2",level)
    #     players.append(player)
    # else:
    #     name = input("Player 2 name: ")
    #     player = Player(2,name,-1)
    #     players.append(player)
    # if playnum<=compnum+2 and playnum>=3:
    #     level = eval(input("Computer 3 level: "))
    #     player = Player(3,"Computer 3",level)
    #     players.append(player)
    # elif playnum>=3:
    #     name = input("Player 3 name: ")
    #     player = Player(3,name,-1)
    #     players.append(player)
    # if playnum<=compnum+3 and playnum==4:
    #     level = eval(input("Computer 4 level: "))
    #     player = Player(4,"Computer 4",level)
    #     players.append(player)
    # elif playnum==4:
    #     name = input("Player 4 name: ")
    #     player = Player(4,name,-1)
    #     players.append(player)

    splash.withdraw()
    player_window.update()
    player_window.deiconify()

    players = []
    while len(players)<2:
        players = []

        player_window.wait_variable(button_chosen)

        if player_1_type.get()=="Human":
            players.append(Player(1,player_1_name.get(),-1))
        elif player_1_type.get()=="Computer":
            try:
                players.append(Player(1,"Computer 1",eval(player_1_name.get())))
            except:
                players.append(Player(1,"Computer 1",0))
        if player_2_type.get()=="Human":
            players.append(Player(2,player_2_name.get(),-1))
        elif player_2_type.get()=="Computer":
            try:
                players.append(Player(2,"Computer 2",eval(player_2_name.get())))
            except:
                players.append(Player(2,"Computer 2",0))
        if player_3_type.get()=="Human":
            players.append(Player(3,player_3_name.get(),-1))
        elif player_3_type.get()=="Computer":
            try:
                players.append(Player(3,"Computer 3",eval(player_3_name.get())))
            except:
                players.append(Player(3,"Computer 3",0))
        if player_4_type.get()=="Human":
            players.append(Player(4,player_4_name.get(),-1))
        elif player_4_type.get()=="Computer":
            try:
                players.append(Player(4,"Computer 4",eval(player_4_name.get())))
            except:
                players.append(Player(4,"Computer 4",0))

    open_board_window(player_window,board)

    return players


def draw_log():
    """Adds log to board window"""
    from main import log_file_name
    global log_text, log_file
    log_text = Text(board_canvas, height=2, width=30,
        background=background_color, font=(txt_font,int(txt_size*.8)))
    log_text_window = board_canvas.create_window(
        int((hex_x_off-water_width)/2),int(win_height*5/6),
        height=int(win_height/3), width=hex_x_off-water_width,
        window=log_text, tags="log")
    log_file = open(log_file_name,'a+')
    log_file.seek(0)
    fullfile = log_file.read()
    log_text.insert(END, fullfile)
    log_text.config(state=DISABLED)


def undraw_log():
    """Undraws log from the board window"""
    board_canvas.delete("log")
    log_text.destroy()
    log_file.close()


def write_log(text,*args,sep=" ",end="\n"):
    """Writes text to the log"""
    write_text = str(text)
    for arg in args:
        write_text += sep
        write_text += str(arg)
    write_text += end
    log_text.config(state=NORMAL)
    log_text.insert(END, write_text)
    log_text.yview(MOVETO, 1)
    log_text.config(state=DISABLED)
    log_file.write(write_text)


def get_tiles():
    """Returns tile array"""
    return tiles


def draw_tile_skeleton(tiles):
    """Draws the outlines for the hexagon tiles"""
    # Water base
    water_color = set_color("water")
    board_canvas.create_rectangle(hex_x_off-water_width, hex_y_off-water_width,
        win_width, win_height, fill=water_color)

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

    draw_ports(tiles)


def draw_ports(tiles):
    """Draws the ports on the game board window"""
    from catan_logic import all_points
    dock_color = set_color("dock")
    for tile in tiles:
        for point in all_points:
            if not(tile.index in point.coordinate):
                continue
            if point.is_port and tile.dock:
                point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
                # Center of tile
                tile_x = (tile.vertices[0]+tile.vertices[6])/2
                tile_y = (tile.vertices[1]+tile.vertices[7])/2
                board_canvas.create_line(point.vertex[0],point.vertex[1],
                    tile_x,tile_y, fill=dock_color, width=5)
                dock_resource = point.port_resource
                dock_ratio = point.port_ratio
        if tile.dock:
            tile.draw_dock(board_canvas, int(.8*txt_size), dock_resource,
                dock_ratio)
    board_canvas.tag_raise("hex")


def draw_circle(point):
    """Draws a circle around the vertex at point, as long as the point is
        valid"""
    r = int(hex_height/25)
    if point.valid:
        point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
        board_canvas.create_oval(point.vertex[0]-r,point.vertex[1]-r,
            point.vertex[0]+r,point.vertex[1]+r, width=3, tags="circle")


def placement_loop(player,available_points):
    """Loops until player chooses a valid vertex, then returns its coordinate"""
    valid_position = False
    click_x.set(int(hex_x_off-water_width)+1)
    click_y.set(int(hex_y_off-water_width)+1)

    # Wait for the player to click a valid vertex
    while(not(valid_position)):
        coordinate = []
        # Draw the circles for the valid plays
        #  (after clearing any existing circles)
        board_canvas.delete("circle")
        # If the player clicked away from the hexagons, exit the loop early
        #  Only allowed after the initial round of placements!
        if (click_x.get()<hex_x_off-water_width or
            click_y.get()<hex_y_off-water_width) and \
            len(player.roads)>1:
            return False
        # Draw circles on available points
        for pt in available_points:
            draw_circle(pt)
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

    #print("Choose a vertex to place a settlement")

    coordinate = placement_loop(player,available_points)

    # If the placement loop was exited early, exit this loop early too
    if not(coordinate):
        return False

    #print("Chose point",coordinate)

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

    #print("Choose two vertices to place a road")

    # Loop until player picks a valid road pair
    while(not(valid_road)):
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
            points_to_remove = []
            for point in available_points:
                for guy in players:
                    if Road(road_coordinates[0],point) in guy.roads:
                        points_to_remove.append(point)
            for point in points_to_remove:
                available_points.remove(point)


        # Wait for the player to click a valid vertex
        coordinate = placement_loop(player,available_points)

        # If the placement loop was exited early, exit this loop early too
        if not(coordinate):
            return False

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
            # road_unowned = True
            # for player in players:
            #     if road in player.roads:
            #         road_unowned = False
            if road.valid:
                for match in available_roads:
                    if road==match:
                        valid_road = True
            # If the road is not legal after all, try two new vertices
            if not(valid_road):
                road_coordinates = []

    #print("Chose road",road.point1.coordinate,road.point2.coordinate)

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

    #print("Choose a vertex to place a city")

    coordinate = placement_loop(player,available_points)

    # If the placement loop was exited early, exit this loop early too
    if not(coordinate):
        return False

    #print("Chose point",coordinate)

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


def maritime_trade(player,players):
    """Clears buttons and draws trading screen for player"""
    undraw_buttons()

    res_give_options = []
    res_get_options = ["1 wood","1 brick","1 sheep","1 wheat","1 stone"]

    # for res in res_get_options:
    #     if res[2:] in player.ports:
    #         res_give_options.append("2 "+res[2:])
    if "any" in player.ports or "?" in player.ports:
        trade_ratio = 3
    else:
        trade_ratio = 4

    if ("wood" in player.ports) and player.wood>=2:
        res_give_options.append("2 wood")
    elif player.wood>=trade_ratio:
        res_give_options.append(str(trade_ratio)+" wood")
    if ("brick" in player.ports) and player.brick>=2:
        res_give_options.append("2 brick")
    elif player.brick>=trade_ratio:
        res_give_options.append(str(trade_ratio)+" brick")
    if ("sheep" in player.ports) and player.sheep>=2:
        res_give_options.append("2 sheep")
    elif player.sheep>=trade_ratio:
        res_give_options.append(str(trade_ratio)+" sheep")
    if ("wheat" in player.ports) and player.wheat>=2:
        res_give_options.append("2 wheat")
    elif player.wheat>=trade_ratio:
        res_give_options.append(str(trade_ratio)+" wheat")
    if ("stone" in player.ports) and player.stone>=2:
        res_give_options.append("2 stone")
    elif player.stone>=trade_ratio:
        res_give_options.append(str(trade_ratio)+" stone")

    if len(res_give_options)!=0:
        res_give_text = board_canvas.create_text(
            int((hex_x_off-water_width)*5/10),int(win_height*.4),
            text="Trade the resources:",
            font=(txt_font, int(.8*txt_size)), tags="trade")
        res_give = StringVar()
        res_give.set("Choose a resource to give")
        res_give_menu = OptionMenu(board_canvas, res_give, *res_give_options)
        res_give_window = board_canvas.create_window(
            int((hex_x_off-water_width)*5/10),int(win_height*.4+2*txt_size),
            window=res_give_menu, tags="trade")
        res_get_text = board_canvas.create_text(
            int((hex_x_off-water_width)*5/10),int(win_height*.4+4*txt_size),
            text="for the resource:",
            font=(txt_font, int(.8*txt_size)), tags="trade")
        res_get = StringVar()
        res_get.set("Choose a resource to receive")
        res_get_menu = OptionMenu(board_canvas, res_get, *res_get_options)
        res_get_window = board_canvas.create_window(
            int((hex_x_off-water_width)*5/10),int(win_height*.4+6*txt_size),
            window=res_get_menu, tags="trade")
        trade_button = Button(board_canvas,
            font=(txt_font, int(.8*txt_size)), text="Trade",
            command=lambda : set_button_chosen(0))
        trade_button.configure(width=10, height=1, padx=0, pady=0,
            background=inactive_button_color, activebackground=active_button_color)
        trade_button_window = board_canvas.create_window(
            int((hex_x_off-water_width)*5/10),int(win_height*.4+8*txt_size),
            window=trade_button, tags="trade")
    else:
        res_give_text = board_canvas.create_text(
            int((hex_x_off-water_width)*5/10),int(win_height*.4),
            text="Not enough resources to trade!",
            font=(txt_font, int(.8*txt_size)), tags="trade")
        trade_button = Button(board_canvas,
            font=(txt_font, int(.8*txt_size)), text="Cancel",
            command=lambda : set_button_chosen(0))
        trade_button.configure(width=10, height=1, padx=0, pady=0,
            background=inactive_button_color, activebackground=active_button_color)
        trade_button_window = board_canvas.create_window(
            int((hex_x_off-water_width)*5/10),int(win_height*.4+8*txt_size),
            window=trade_button, tags="trade")

    while button_chosen.get()!=0:
        draw_stats(players)
        draw_resources(player)
        board_canvas.wait_variable(button_chosen)

    button_chosen.set(-1)

    if len(res_give_options)!=0:
        if res_give.get()!="Choose a resource to give" and \
            res_get.get()!="Choose a resource to receive":
            given_resource = res_give.get()[2:]
            given_number = int(res_give.get()[0])
            gotten_resource = res_get.get()[2:]
            gotten_number = int(res_get.get()[0])
            if given_resource=="wood":
                player.wood -= given_number
            if given_resource=="brick":
                player.brick -= given_number
            if given_resource=="sheep":
                player.sheep -= given_number
            if given_resource=="wheat":
                player.wheat -= given_number
            if given_resource=="stone":
                player.stone -= given_number
            if gotten_resource=="wood":
                player.wood += gotten_number
            if gotten_resource=="brick":
                player.brick += gotten_number
            if gotten_resource=="sheep":
                player.sheep += gotten_number
            if gotten_resource=="wheat":
                player.wheat += gotten_number
            if gotten_resource=="stone":
                player.stone += gotten_number
            write_log(player.name,"traded",given_number,given_resource,"for",
                gotten_number,gotten_resource)
        res_give_menu.destroy()
        res_get_menu.destroy()

    board_canvas.delete("trade")
    trade_button.destroy()

    draw_buttons(player)


def draw_dice(die_1,die_2):
    """Undraws previous dice and draws dice of values 'die_1' and 'die_2'"""
    board_canvas.delete("dice")

    die_height = int((hex_y_off-water_width)*.5)
    die_width = die_height
    die_x_off = int((hex_x_off-water_width-2*die_width)*2/5)
    die_y_off = int((hex_y_off-water_width-die_height)/3)
    die_sep = int(die_x_off/2)
    board_canvas.create_rectangle(die_x_off,die_y_off,
        die_x_off+die_width,die_y_off+die_height,
        fill="red", tags="dice")
    board_canvas.create_rectangle(die_x_off+die_width+die_sep,die_y_off,
        die_x_off+die_width+die_sep+die_width,die_y_off+die_height,
        fill="yellow", tags="dice")

    die=[die_1,die_2]
    dot_r = int(die_height/10)
    for i in range(2):
        # Top left and bottom right dots
        if die[i]!=1:
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center left and right dots
        if die[i]==6:
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Bottom left and top right dots
        if die[i]>=4:
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center dot
        if die[i]%2==1:
            board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(2*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(2*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")


def draw_intermediate_screen(player):
    """Draws a screen with player name between turns"""
    text_string = player.name+"'s turn!"
    intermediate_text_1 = board_canvas.create_text(
        int((hex_x_off-water_width)/2),int(win_height/3),
        text=text_string, font=(txt_font,int(1.5*txt_size)), fill=player.color,
        width=int(.9*(hex_x_off-water_width)))
    intermediate_text_2 = board_canvas.create_text(
        int((hex_x_off-water_width)/2),int(win_height/3)+2*txt_size,
        text="Click to continue", font=(txt_font,txt_size), fill= player.color,
        width=int(.9*(hex_x_off-water_width)))
    board_canvas.wait_variable(click_x)
    board_canvas.delete(intermediate_text_1)
    board_canvas.delete(intermediate_text_2)


def draw_stats(players):
    """Draws player statistics such as victory points, total resources, etc.
    to game board window"""
    board_canvas.delete("stats")

    portion = (win_width-hex_x_off+water_width)/len(players)
    for i in range(len(players)):
        player = players[i]
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int((hex_y_off-water_width)/4), text=player.name, fill=player.color,
            font=(txt_font, int(.9*txt_size)), tags="stats")
        vp_string = "Victory points: "+str(player.score)
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int(2*(hex_y_off-water_width)/4), text=vp_string, fill=player.color,
            font=(txt_font, int(.7*txt_size)), tags="stats")
        resource_string = "Resources: "+str(player.wood+player.brick+ \
            player.wheat+player.sheep+player.stone)
        board_canvas.create_text(hex_x_off-water_width+int((i+.5)*portion),
            int(3*(hex_y_off-water_width)/4), text=resource_string,
            fill=player.color, font=(txt_font, int(.7*txt_size)),
            tags="stats")


def draw_buttons(player):
    """Draws buttons for player actions on the board window"""
    global build_settlement_button, build_road_button, build_city_button
    global buy_dev_button, maritime_trade_button, trading_post_button
    global end_turn_button

    # Create buttons on board window
    build_settlement_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Build Settlement",
        command=lambda : set_button_chosen(1))
    build_settlement_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    build_settlement_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*3/10),int(win_height*.4),
        window=build_settlement_button, tags="button")
    settlement_cost_text = board_canvas.create_text(
        int((hex_x_off-water_width)*3/10),int(win_height*.4+1.25*txt_size),
        text="(1 wood, 1 brick, 1 sheep, 1 wheat)",
        font=(txt_font, int(.5*txt_size)), tags="button")
    build_road_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Build Road",
        command=lambda : set_button_chosen(2))
    build_road_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    build_road_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*7/10),int(win_height*.4),
        window=build_road_button, tags="button")
    road_cost_text = board_canvas.create_text(
        int((hex_x_off-water_width)*7/10),int(win_height*.4+1.25*txt_size),
        text="(1 wood, 1 brick)",
        font=(txt_font, int(.5*txt_size)), tags="button")
    build_city_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Build City",
        command=lambda : set_button_chosen(3))
    build_city_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    build_city_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*3/10),int(win_height*.4+3*txt_size),
        window=build_city_button, tags="button")
    city_cost_text = board_canvas.create_text(
        int((hex_x_off-water_width)*3/10),int(win_height*.4+4.25*txt_size),
        text="(2 wheat, 3 stone)",
        font=(txt_font, int(.5*txt_size)), tags="button")
    buy_dev_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Development",
        command=lambda : set_button_chosen(4))
    buy_dev_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    buy_dev_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*7/10),int(win_height*.4+3*txt_size),
        window=buy_dev_button, tags="button")
    dev_cost_text = board_canvas.create_text(
        int((hex_x_off-water_width)*7/10),int(win_height*.4+4.25*txt_size),
        text="(1 sheep, 1 wheat, 1 stone)",
        font=(txt_font, int(.5*txt_size)), tags="button")
    maritime_trade_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Port Trade",
        command=lambda : set_button_chosen(5))
    maritime_trade_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    maritime_trade_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*3/10),int(win_height*.4+6*txt_size),
        window=maritime_trade_button, tags="button")
    trading_post_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="Player Trade",
        command=lambda : set_button_chosen(6))
    trading_post_button.configure(width=13, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    trading_post_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*7/10),int(win_height*.4+6*txt_size),
        window=trading_post_button, tags="button")
    end_turn_button = Button(board_canvas,
        font=(txt_font, int(.8*txt_size)), text="End Turn",
        command=lambda : set_button_chosen(0))
    end_turn_button.configure(width=10, height=1, padx=0, pady=0,
        background=inactive_button_color, activebackground=active_button_color)
    end_turn_button_window = board_canvas.create_window(
        int((hex_x_off-water_width)*5/10),int(win_height*.4+8*txt_size),
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
    buy_dev_button.destroy()
    maritime_trade_button.destroy()
    trading_post_button.destroy()
    end_turn_button.destroy()


def draw_resources(player):
    """Undraws any current resources shown and draws resources of player"""
    board_canvas.delete("resources")

    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width, text=player.name, fill=player.color,
        font=(txt_font, int(1.5*txt_size)), tags="resources")

    wood_text = "Wood: "+str(player.wood)
    brick_text = "Brick: "+str(player.brick)
    sheep_text = "Sheep: "+str(player.sheep)
    wheat_text = "Wheat: "+str(player.wheat)
    stone_text = "Stone: "+str(player.stone)

    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width+int(1.8*txt_size), text=wood_text,# anchor=NW,
        font=(txt_font, int(.8*txt_size)), #fill=wood_color,
        tags="resources")
    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width+int(2.9*txt_size), text=brick_text,# anchor=NW,
        font=(txt_font, int(.8*txt_size)), #fill=brick_color,
        tags="resources")
    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width+int(4.0*txt_size), text=sheep_text,# anchor=NW,
        font=(txt_font, int(.8*txt_size)), #fill=sheep_color,
        tags="resources")
    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width+int(5.1*txt_size), text=wheat_text,# anchor=NW,
        font=(txt_font, int(.8*txt_size)), #fill=wheat_color,
        tags="resources")
    board_canvas.create_text(int((hex_x_off-water_width)/2),
        hex_y_off-water_width+int(6.2*txt_size), text=stone_text,# anchor=NW,
        font=(txt_font, int(.8*txt_size)), #fill=stone_color,
        tags="resources")


def draw_resource_panel(player):
    """Draws resources available to player number 'index' in the resource panel
    of the board window. Also activates buttons available to player."""

    draw_buttons(player)

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
    # For human players, draw buttons and get button clicks
    if player.AI_code<0:
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
            elif button_chosen.get()==5:
                maritime_trade(player,players)
    # For computer players, reference AI file
    else:
        from catan_AI import computer_take_turn
        computer_action = "none"
        while not(computer_action=="ended turn"):
            computer_action = computer_take_turn(player,players)
            write_log(player.name,computer_action)


def draw_winning_screen(player):
    """Draws a congratulatory screen for the winning player"""
    text_string = player.name+" wins!"
    winning_text = board_canvas.create_text(
        int((hex_x_off-water_width)/2),int(win_height/3),
        text=text_string, font=(txt_font,3*txt_size), fill=player.color,
        width=int(.9*(hex_x_off-water_width)))
    board_canvas.wait_window(board_canvas)


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    aesthetics(900,600)
    print(wood_color)
