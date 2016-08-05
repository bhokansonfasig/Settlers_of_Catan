from draw_menus import draw_log, undraw_log, draw_stats, draw_status_box
from draw_menus import draw_resource_panel, trade_menu

def redraw_board(app):
    app.board_canvas.delete('all')
    draw_tile_skeleton(app)
    draw_tiles(app)
    undraw_log(app)
    draw_log(app)
    for player in app.pieces.players:
        for road in player.roads:
            draw_road(road,player,app)
        for settlement in player.settlements:
            draw_settlement(settlement,player,app)
        for city in player.cities:
            draw_city(city,player,app)
    draw_stats(app)
    draw_status_box(app)
    if app.pieces.phase_index()>5:
        draw_dice(app)
    if app.pieces.turn_phase=="make decisions":
        draw_resource_panel(app.pieces.players[app.pieces.turn_index],app)
    elif app.pieces.turn_phase=="discard":
        # Draw discard screen in a nice way...
        pass
    elif app.pieces.turn_phase=="trade":
        # Draw trade info in a nice way...
        # Just using trade_menu causes it to stall since it has to wait for the
        # button press
        #trade_menu(app.pieces.players[app.pieces.turn_index],app)
        pass


def draw_tile_skeleton(app):
    """Draws the outlines for the hexagon tiles"""
    # Water base
    water_color = app.style.get_color("water")
    app.board_canvas.create_rectangle(app.style.hex_x_off-app.style.water_width,
        app.style.hex_y_off-app.style.water_width,
        app.style.win_width, app.style.win_height, fill=water_color)

    for tile in app.pieces.tiles:
        tile.set_vertices(app.style.hex_width, app.style.hex_height,
            app.style.hex_x_off, app.style.hex_y_off)
        if tile.visible:
            tile.draw_skeleton(app.board_canvas,app.style)


def draw_tiles(app):
    """Draws tiles on game board window"""
    for tile in app.pieces.tiles:
        if tile.visible:
            tile.draw(app.board_canvas,app.style)
            tile.draw_number(app.board_canvas,app.style)

    draw_ports(app)
    redraw_robber(app)


def draw_ports(app):
    """Draws the ports on the game board window"""
    dock_color = app.style.get_color("dock")
    for tile in app.pieces.tiles:
        for point in app.pieces.all_points:
            if not(tile.index in point.coordinate):
                continue
            if point.is_port and tile.dock:
                point.link_vertex(app.style.hex_width, app.style.hex_height,
                    app.style.hex_x_off, app.style.hex_y_off)
                # Center of tile
                tile_x = (tile.vertices[0]+tile.vertices[6])/2
                tile_y = (tile.vertices[1]+tile.vertices[7])/2
                app.board_canvas.create_line(point.vertex[0],point.vertex[1],
                    tile_x,tile_y, fill=dock_color, width=5)
                dock_resource = point.port_resource
                dock_ratio = point.port_ratio
        if tile.dock:
            tile.draw_dock(app.board_canvas,app.style,dock_resource,dock_ratio)
    app.board_canvas.tag_raise("hex")


def redraw_robber(app):
    """Redraws the robber onto his current tile"""
    app.board_canvas.delete("robber")
    for tile in app.pieces.tiles:
        if tile.has_robber:
            tile.draw_robber(app.board_canvas)
            break


def draw_circle(point,app):
    """Draws a circle around the vertex at point, as long as the point is
        valid"""
    r = int(app.style.hex_height/25)
    if point.valid:
        point.link_vertex(app.style.hex_width, app.style.hex_height,
            app.style.hex_x_off, app.style.hex_y_off)
        app.board_canvas.create_oval(point.vertex[0]-r,point.vertex[1]-r,
            point.vertex[0]+r,point.vertex[1]+r, width=3, tags="circle")


def draw_settlement(point, player, app):
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

    point.link_vertex(app.style.hex_width, app.style.hex_height,
        app.style.hex_x_off, app.style.hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(app.style.hex_height/50)

    player.settlements[i].tk_index = app.board_canvas.create_polygon([x+size,
        y-size, x+size,y+size, x-size,y+size, x-size,y-size, x,y-int(1.8*size)],
        fill=player.color, outline="black", tags=("settlement",player.index))


def draw_road(road, player, app):
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

    road.point1.link_vertex(app.style.hex_width, app.style.hex_height,
        app.style.hex_x_off, app.style.hex_y_off)
    road.point2.link_vertex(app.style.hex_width, app.style.hex_height,
        app.style.hex_x_off, app.style.hex_y_off)
    x_1 = road.point1.vertex[0]
    y_1 = road.point1.vertex[1]
    x_2 = road.point2.vertex[0]
    y_2 = road.point2.vertex[1]

    offset = int(app.style.hex_height/50)

    player.roads[i].tk_index = app.board_canvas.create_line(x_1,y_1, x_2,y_2,
        width=7, fill=player.color, tags=("road",player.index))

    app.board_canvas.tag_raise("settlement")
    app.board_canvas.tag_raise("city")


def draw_city(point, player, app):
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
    all_settlements = app.board_canvas.find_withtag("settlement")
    owned_settlements = []
    for settlement in all_settlements:
        if str(player.index) in app.board_canvas.gettags(settlement):
            owned_settlements.append(settlement)
    point.link_vertex(app.style.hex_width, app.style.hex_height,
        app.style.hex_x_off, app.style.hex_y_off)
    size = int(app.style.hex_height/50)
    for match in owned_settlements:
        if point.vertex[0]+size in app.board_canvas.coords(match) and \
                point.vertex[1]+size in app.board_canvas.coords(match):
            app.board_canvas.delete(match)

    app.board_canvas.tag_raise("settlement")

    #point.link_vertex(hex_width, hex_height, hex_x_off, hex_y_off)
    x = point.vertex[0]
    y = point.vertex[1]

    size = int(app.style.hex_height/50)

    player.cities[i].tk_index = app.board_canvas.create_polygon([
        x+2*size,y-int(1.8*size), x+2*size,y+size, x-2*size,y+size,
        x-2*size,y-size, x-size,y-int(1.8*size), x,y-size, x,y-int(1.8*size),
        x+size,y-int(3*size)], fill=player.color, outline="black",
        tags=("city",player.index))


def draw_dice(app):
    """Undraws previous dice and draws dice of values 'die_1' and 'die_2'"""
    app.board_canvas.delete("dice")

    die_height = int((app.style.hex_y_off-app.style.water_width)*.5)
    die_width = die_height
    die_x_off = int((app.style.hex_x_off-app.style.water_width-2*die_width)*1/5)
    die_y_off = int((app.style.hex_y_off-app.style.water_width-die_height)/3)
    die_sep = int(die_x_off/2)
    app.board_canvas.create_rectangle(die_x_off,die_y_off,
        die_x_off+die_width,die_y_off+die_height,
        fill="red", tags="dice")
    app.board_canvas.create_rectangle(die_x_off+die_width+die_sep,die_y_off,
        die_x_off+die_width+die_sep+die_width,die_y_off+die_height,
        fill="yellow", tags="dice")

    dot_r = int(die_height/10)
    for i in range(2):
        # Top left and bottom right dots
        if app.pieces.dice[i]!=1:
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center left and right dots
        if app.pieces.dice[i]==6:
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
        # Bottom left and top right dots
        if app.pieces.dice[i]>=4:
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(die_width/4)-dot_r,
                die_y_off+int(3*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(die_width/4)+dot_r,
                die_y_off+int(3*die_width/4)+dot_r,
                fill="black", tags="dice")
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)-dot_r,
                die_y_off+int(die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(3*die_width/4)+dot_r,
                die_y_off+int(die_width/4)+dot_r,
                fill="black", tags="dice")
        # Center dot
        if app.pieces.dice[i]%2==1:
            app.board_canvas.create_oval(
                die_x_off+i*(die_width+die_sep)+int(2*die_width/4)-dot_r,
                die_y_off+int(2*die_width/4)-dot_r,
                die_x_off+i*(die_width+die_sep)+int(2*die_width/4)+dot_r,
                die_y_off+int(2*die_width/4)+dot_r,
                fill="black", tags="dice")
