from tkinter import *
from random import choice

from tiles import Tile
from point import Point
from road import Road

from draw_elements import draw_circle
from draw_menus import draw_stats, draw_resources
from draw_menus import draw_resource_panel, clear_resource_panel
from draw_menus import draw_discard_screen, write_log

def turn_loop(player,app):
    from catan_logic import build_settlement, build_road, build_city
    from catan_logic import buy_development_card
    from catan_logic import legal_settlement_placements, legal_road_placements
    from catan_AI import computer_take_turn

    draw_stats(app)
    clear_resource_panel(app)
    draw_resource_panel(app.pieces.players[app.pieces.turn_index],app)

    # For human players, draw buttons and get button clicks
    if player.AI_code<0:
        app.button_chosen.set(-1)
        while app.button_chosen.get()!=0:
            app.pieces.turn_phase = "make decisions"
            draw_stats(app)
            clear_resource_panel(app)
            draw_resource_panel(app.pieces.players[app.pieces.turn_index],app)

            app.board_canvas.wait_variable(app.button_chosen)
            if app.button_chosen.get()==1:
                build_settlement(player,app)
            elif app.button_chosen.get()==2:
                build_road(player,app)
            elif app.button_chosen.get()==3:
                build_city(player,app)
            elif app.button_chosen.get()==4:
                buy_development_card(player,app)
            elif app.button_chosen.get()==5:
                app.pieces.turn_phase = "trade"
                trade_menu(player,app)
            elif app.button_chosen.get()==6:
                app.pieces.turn_phase = "development"
                development_menu(player,app)
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


def player_discard(player,app):
    """Prompts player for how many of each resource they would like to
        discard. They need to get down to new_resource_count"""

    starting_resource_count = player.resource_count()

    clear_resource_panel(app)
    draw_resource_panel(player,app)

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0:
        total_discard_count = app.displays.get_wood_discard() + \
            app.displays.get_brick_discard() + app.displays.get_sheep_discard() + \
            app.displays.get_wheat_discard() + app.displays.get_stone_discard()
        total_string = "Total: " + str(total_discard_count)
        if total_discard_count>player.rob_count():
            total_string_color = "red"
        elif total_discard_count==player.rob_count():
            total_string_color = "#309540" #green
        else:
            total_string_color = "black"
        app.board_canvas.itemconfig(app.displays.total_text,
            text=total_string, fill=total_string_color)

        app.board_canvas.wait_variable(app.button_chosen)
    app.button_chosen.set(-1)

    player.wood -= app.displays.get_wood_discard()
    player.brick -= app.displays.get_brick_discard()
    player.sheep -= app.displays.get_sheep_discard()
    player.wheat -= app.displays.get_wheat_discard()
    player.stone -= app.displays.get_stone_discard()

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


def trade_menu(player,app):
    """Runs trading screen for player"""
    from catan_logic import perform_trade, evaluate_port_trade

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0:
        clear_resource_panel(app)
        draw_resource_panel(player,app)

        app.board_canvas.wait_variable(app.button_chosen)

        if app.button_chosen.get()==1:
            given_resource = app.displays.port_give_text.get()
            gotten_resource = app.displays.port_get_text.get()

            sell_resource_type = given_resource.split()[1]
            sell_resource_copies = int(given_resource.split()[0])
            buy_resource_type = gotten_resource.split()[1]
            buy_resource_copies = int(gotten_resource.split()[0])

            trade_successful, mul, trade_ratio = evaluate_port_trade(player,sell_resource_copies,
                sell_resource_type,buy_resource_copies,buy_resource_type)

            if trade_successful:
                perform_trade(player,sell_resource_type,buy_resource_type,
                    app,mul,False,trade_ratio)

    app.button_chosen.set(-1)


def development_menu(player,app):
    """Runs development card screen for player"""
    from catan_logic import move_robber, build_road

    app.button_chosen.set(-1)
    while app.button_chosen.get()!=0:
        clear_resource_panel(app)
        draw_resource_panel(player,app)

        app.board_canvas.wait_variable(app.button_chosen)

        # Implement use of development cards here
        if app.button_chosen.get()==1 and player.development_cards["victory point"]!=0:
            player.score += player.development_cards["victory point"]
            player.development_cards["victory point"] = 0
        elif app.button_chosen.get()==2 and player.development_cards["knight"]!=0:
            move_robber(player,app)
            player.development_cards["knight"]-=1
            player.knight_count += 1
        elif app.button_chosen.get()==3 and player.development_cards["road building"]!=0:
            build_road(player,app)
            build_road(player,app)
            player.development_cards["road building"]-=1
        elif app.button_chosen.get()==4 and player.development_cards["year of plenty"]!=0:
            player.development_cards["year of plenty"]-=1
            pass
        elif app.button_chosen.get()==5 and player.development_cards["monopoly"]!=0:
            player.development_cards["monopoly"]-=1
            pass

    app.button_chosen.set(-1)
