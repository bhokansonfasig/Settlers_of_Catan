from tkinter import *
from random import choice

from tiles import Tile
from point import Point
from road import Road

from draw_elements import draw_circle
from draw_menus import draw_stats, draw_resources, disable_buttons, write_log

def turn_loop(player,app):
    from catan_logic import build_settlement, build_road, build_city
    from draw_menus import maritime_trade
    from catan_logic import legal_settlement_placements, legal_road_placements
    from catan_AI import computer_take_turn

    # For human players, draw buttons and get button clicks
    if player.AI_code<0:
        app.button_chosen.set(-1)
        while app.button_chosen.get()!=0:
            draw_stats(app)
            draw_resources(player,app)
            disable_buttons(player,app)
            app.board_canvas.wait_variable(app.button_chosen)
            if app.button_chosen.get()==1:
                build_settlement(player,app)
            elif app.button_chosen.get()==2:
                build_road(player,app)
            elif app.button_chosen.get()==3:
                build_city(player,app)
            elif app.button_chosen.get()==5:
                maritime_trade(player,app)
    # For computer players, reference AI file
    else:
        computer_action = "none"
        while not(computer_action=="ended turn"):
            available_settlement_points = legal_settlement_placements(player,
                app.pieces.players,app.pieces.all_points)
            available_roads = legal_road_placements(player,app.pieces.players,
                app.pieces.all_roads)
            computer_action = computer_take_turn(player,
                available_settlement_points,available_roads,app)
            # write_log(app,player.name,computer_action)


def placement_loop(player,available_points,app):
    """Loops until player chooses a valid vertex, then returns its coordinate"""
    valid_position = False
    app.click_x.set(int(app.style.hex_x_off-app.style.water_width)+1)
    app.click_y.set(int(app.style.hex_y_off-app.style.water_width)+1)

    # Wait for the player to click a valid vertex
    while(not(valid_position)):
        coordinate = []
        # Draw the circles for the valid plays
        #  (after clearing any existing circles)
        app.board_canvas.delete("circle")
        # If the player clicked away from the hexagons, exit the loop early
        #  Only allowed after the initial round of placements!
        if (app.click_x.get()<app.style.hex_x_off-app.style.water_width or
            app.click_y.get()<app.style.hex_y_off-app.style.water_width) and \
            len(player.roads)>1:
            return False
        # Draw circles on available points
        for pt in available_points:
            draw_circle(pt,app)
        # Get the hexagons with vertices near the point clicked
        for tile in app.pieces.tiles:
            for i in range(0,12,2):
                if app.click_x.get()>tile.vertices[i]-10 and \
                    app.click_x.get()<tile.vertices[i]+10 and \
                    app.click_y.get()>tile.vertices[i+1]-10 and \
                    app.click_y.get()<tile.vertices[i+1]+10:
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
            app.board_canvas.wait_variable(app.click_x)

    return coordinate


def player_choose_settlement(player,available_points,app):
    """Asks player to click hex point on board to place settlement.
    Returns tuple of the placed settlement"""
    # # Watch for click events
    # board_canvas.bind("<Button-1>", click_set)

    #print("Choose a vertex to place a settlement")

    coordinate = placement_loop(player,available_points,app)

    # If the placement loop was exited early, exit this loop early too
    if not(coordinate):
        return False

    #print("Chose point",coordinate)

    # # Stop watching for click events
    # board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    app.board_canvas.delete("circle")

    return Point(coordinate[0],coordinate[1],coordinate[2])


def player_choose_road(player,players,app):
    """Asks player to click two hex points on board to place road between them.
    Returns tuples of the placed road"""
    from catan_logic import legal_road_placements

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
        available_roads = legal_road_placements(player,app.pieces.players,
            app.pieces.all_roads)
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
                for guy in app.pieces.players:
                    if Road(road_coordinates[0],point) in guy.roads:
                        points_to_remove.append(point)
            for point in points_to_remove:
                available_points.remove(point)


        # Wait for the player to click a valid vertex
        coordinate = placement_loop(player,available_points,app)

        # If the placement loop was exited early, exit this loop early too
        if not(coordinate):
            return False

        # Add selected vertex to the road coordinates
        road_coordinates.append(Point(coordinate[0],coordinate[1],
            coordinate[2]))

        # Set variables to loop again
        # valid_position = False
        app.click_x.set(0)
        app.click_y.set(0)

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
    app.board_canvas.delete("circle")

    return road


def player_choose_city(player,players,app):
    """Asks player to click hex point on board to place city.
    Returns tuple of the placed settlement"""
    # # Watch for click events
    # board_canvas.bind("<Button-1>", click_set)

    # Determine the places a player can legally play
    available_points = []
    for point in player.settlements:
        available_points.append(point)

    #print("Choose a vertex to place a city")

    coordinate = placement_loop(player,available_points,app)

    # If the placement loop was exited early, exit this loop early too
    if not(coordinate):
        return False

    #print("Chose point",coordinate)

    # # Stop watching for click events
    # board_canvas.unbind("<Button-1>")

    # Get rid of all circles
    app.board_canvas.delete("circle")

    return Point(coordinate[0],coordinate[1],coordinate[2])


def player_place_robber(player,app):
    """Gets click of where player would like to place the robber"""
    # valid_position = False
    app.click_x.set(int(app.style.hex_x_off-app.style.water_width)+1)
    app.click_y.set(int(app.style.hex_y_off-app.style.water_width)+1)

    available_tiles = []
    for tile in app.pieces.tiles:
        if tile.visible and not(tile.has_robber):
            available_tiles.append(tile)

    robber_tile = Tile(0)
    # Wait for the player to click a valid tile for the robber
    while(not(robber_tile in available_tiles)):
        # coordinate = 0
        # Draw the circles for the valid plays
        #  (after clearing any existing circles)
        app.board_canvas.delete("circle")
        # Draw circles on available tiles
        for tile in available_tiles:
            # Get position of center of tile
            pos_x = (tile.vertices[0]+tile.vertices[6])/2
            pos_y = (tile.vertices[1]+tile.vertices[7])/2
            # Set the radius of the circle based on a third the side length
            r = (tile.vertices[3]-tile.vertices[1])/3
            # Draw the circle
            app.board_canvas.create_oval(pos_x-r,pos_y-r, pos_x+r,pos_y+r,
                width=3, tags="circle")
        # Find which tile was clicked
        for tile in available_tiles:
            # Get position of center of tile
            pos_x = (tile.vertices[0]+tile.vertices[6])/2
            pos_y = (tile.vertices[1]+tile.vertices[7])/2
            # Set the radius of the circle based on a third the side length
            r = (tile.vertices[3]-tile.vertices[1])/3
            if app.click_x.get()>pos_x-r and app.click_x.get()<pos_x+r and \
                app.click_y.get()>pos_y-r and app.click_y.get()<pos_y+r:
                robber_tile = tile
                break
        # If the point clicked is not a legal vertex, try again
        if not(robber_tile in available_tiles):
            app.board_canvas.wait_variable(app.click_x)

    app.board_canvas.delete("circle")

    return robber_tile


def player_discard(player,new_resource_count,app):
    """Prompts player for how many of each resource they would like to
        discard. They need to get down to new_resource_count"""
    draw_resources(player,app)
    draw_stats(app)

    starting_resource_count = player.resource_count()

    wood_discard_options = ["Wood","0"]
    brick_discard_options = ["Brick","0"]
    sheep_discard_options = ["Sheep","0"]
    wheat_discard_options = ["Wheat","0"]
    stone_discard_options = ["Stone","0"]
    for i in range(player.wood):
        wood_discard_options.append(str(i+1))
    for i in range(player.brick):
        brick_discard_options.append(str(i+1))
    for i in range(player.sheep):
        sheep_discard_options.append(str(i+1))
    for i in range(player.wheat):
        wheat_discard_options.append(str(i+1))
    for i in range(player.stone):
        stone_discard_options.append(str(i+1))

    discards_needed = starting_resource_count-new_resource_count
    discard_string = "Choose "+str(discards_needed)+" resources to give up:"
    discard_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4), text=discard_string,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="discard")
    wood_discard = StringVar()
    wood_discard.set(wood_discard_options[0])
    wood_discard_menu = OptionMenu(app.board_canvas, wood_discard,
        *wood_discard_options, command=lambda x: app.set_button_chosen(11))
    wood_discard_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=wood_discard_menu, tags="discard")
    brick_discard = StringVar()
    brick_discard.set(brick_discard_options[0])
    brick_discard_menu = OptionMenu(app.board_canvas, brick_discard,
        *brick_discard_options, command=lambda x: app.set_button_chosen(12))
    brick_discard_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+2*app.style.txt_size),
        window=brick_discard_menu, tags="discard")
    sheep_discard = StringVar()
    sheep_discard.set(sheep_discard_options[0])
    sheep_discard_menu = OptionMenu(app.board_canvas, sheep_discard,
        *sheep_discard_options, command=lambda x: app.set_button_chosen(13))
    sheep_discard_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=sheep_discard_menu, tags="discard")
    wheat_discard = StringVar()
    wheat_discard.set(wheat_discard_options[0])
    wheat_discard_menu = OptionMenu(app.board_canvas, wheat_discard,
        *wheat_discard_options, command=lambda x: app.set_button_chosen(14))
    wheat_discard_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*7/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        window=wheat_discard_menu, tags="discard")
    stone_discard = StringVar()
    stone_discard.set(stone_discard_options[0])
    stone_discard_menu = OptionMenu(app.board_canvas, stone_discard,
        *stone_discard_options, command=lambda x: app.set_button_chosen(15))
    stone_discard_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*3/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=stone_discard_menu, tags="discard")
    give_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)),
        text="Give up resources", command=lambda : app.set_button_chosen(0))
    give_button.configure(width=15, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    give_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=give_button, tags="discard")

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0:
        if app.button_chosen.get()!=-1:
            app.board_canvas.delete(total_text)
        try:
            wood_discard_count = int(wood_discard.get())
        except:
            wood_discard_count = 0
        try:
            brick_discard_count = int(brick_discard.get())
        except:
            brick_discard_count = 0
        try:
            sheep_discard_count = int(sheep_discard.get())
        except:
            sheep_discard_count = 0
        try:
            wheat_discard_count = int(wheat_discard.get())
        except:
            wheat_discard_count = 0
        try:
            stone_discard_count = int(stone_discard.get())
        except:
            stone_discard_count = 0
        total_discard_count = wood_discard_count+brick_discard_count+ \
                   sheep_discard_count+wheat_discard_count+stone_discard_count
        total_string = "Total: " + str(total_discard_count)
        if total_discard_count>discards_needed:
            total_string_color = "red"
        elif total_discard_count==discards_needed:
            total_string_color = "#309540"
        else:
            total_string_color = "black"
        total_text = app.board_canvas.create_text(
            int((app.style.hex_x_off-app.style.water_width)*7/10),
            int(app.style.win_height*.4+6*app.style.txt_size),
            text=total_string, fill=total_string_color,
            font=(app.style.txt_font,int(.8*app.style.txt_size)),tags="discard")
        app.board_canvas.wait_variable(app.button_chosen)
    app.button_chosen.set(-1)

    player.wood -= wood_discard_count
    player.brick -= brick_discard_count
    player.sheep -= sheep_discard_count
    player.wheat -= wheat_discard_count
    player.stone -= stone_discard_count

    app.board_canvas.delete("discard")
    wood_discard_menu.destroy()
    give_button.destroy()

    discard_count = starting_resource_count - player.resource_count()
    return discard_count


def player_steal_resource(player,robber_tile,app):
    """Prompts player for which player they would like to steal from"""
    stealable_players = []
    for guy in app.pieces.players:
        guy_added = False
        for point in guy.settlements:
            if robber_tile.index in point.coordinate:
                stealable_players.append(guy)
                guy_added = True
                break
        if guy_added:
            continue
        for point in guy.cities:
            if robber_tile.index in point.coordinate:
                stealable_players.append(guy)
                break
    if player in stealable_players:
        stealable_players.remove(player)
    for guy in stealable_players:
        if guy.resource_count()==0:
            stealable_players.remove(guy)

    if len(stealable_players)==0:
        return

    player_options = []
    for guy in stealable_players:
        player_options.append(guy.name)

    player_choice_text = app.board_canvas.create_text(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+4*app.style.txt_size),
        text="Take a resource from:",
        font=(app.style.txt_font,int(.8*app.style.txt_size)), tags="steal")
    player_choice = StringVar()
    player_choice.set("Choose a player to steal from")
    player_choice_menu = OptionMenu(app.board_canvas, player_choice,
        *player_options)
    player_choice_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+6*app.style.txt_size),
        window=player_choice_menu, tags="steal")
    steal_button = Button(app.board_canvas,
        font=(app.style.txt_font,int(.8*app.style.txt_size)), text="Steal",
        command=lambda : app.set_button_chosen(0))
    steal_button.configure(width=10, height=1, padx=0, pady=0)
        #background=inactive_button_color, activebackground=active_button_color)
    steal_button_window = app.board_canvas.create_window(
        int((app.style.hex_x_off-app.style.water_width)*5/10),
        int(app.style.win_height*.4+8*app.style.txt_size),
        window=steal_button, tags="steal")

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0 or \
        player_choice.get()=="Choose a player to steal from":
        app.board_canvas.wait_variable(app.button_chosen)
    app.button_chosen.set(-1)

    target_player_name = player_choice.get()
    for guy in stealable_players:
        if guy.name==target_player_name:
            target_player = guy
            break
    target_resources = []
    for i in range(target_player.wood):
        target_resources.append("wood")
    for i in range(target_player.brick):
        target_resources.append("brick")
    for i in range(target_player.sheep):
        target_resources.append("sheep")
    for i in range(target_player.wheat):
        target_resources.append("wheat")
    for i in range(target_player.stone):
        target_resources.append("stone")
    stolen_resource = choice(target_resources)
    if stolen_resource=="wood":
        target_player.wood -= 1
        player.wood += 1
    if stolen_resource=="brick":
        target_player.brick -= 1
        player.brick += 1
    if stolen_resource=="sheep":
        target_player.sheep -= 1
        player.sheep += 1
    if stolen_resource=="wheat":
        target_player.wheat -= 1
        player.wheat += 1
    if stolen_resource=="stone":
        target_player.stone -= 1
        player.stone += 1

    write_log(app,player.name,"stole a resource from",target_player.name)

    app.board_canvas.delete("steal")
    player_choice_menu.destroy()
    steal_button.destroy()
