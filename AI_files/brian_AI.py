from random import choice
from point import Point
from road import Road
from tiles import Tile

# Brian the bricklayer focuses on monopolizing brick

def get_code():
    return 2

def get_aliases():
    return ['brick','brian','brian the bricklayer',
            'brenda','brenda the bricklayer']

def get_difficulty():
    # Should return the difficulty level of this AI
    #  Return 0 to not be included when an AI is randomly assigned
    return 1


def take_turn(computer,available_settlement_points,available_roads,
        available_city_points,app):
    from catan_logic import perform_trade
    # Function is called to determine what action the computer should take

    # Should return "build settlement", "build road", "build city", or "ended turn"

    # Check current brick trade ratio
    brick_trade_ratio = 4
    if "any" in computer.ports or "?" in computer.ports:
        brick_trade_ratio = 3
    if "brick" in computer.ports:
        brick_trade_ratio = 2

    # If building a road or settlement is possible and no wood is available,
    #  trade for wood if possible
    if (len(available_roads)!=0 or len(available_settlement_points)!=0) and \
        len(computer.roads)<computer.road_max and \
        len(computer.settlements)<computer.settlement_max and \
        computer.wood==0 and computer.brick>=brick_trade_ratio+1:
        perform_trade(computer,"brick","wood",app)
    # If building a settlement is possible and no wheat are available,
    #  trade for wheat if possible
    if len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.wheat==0 and computer.brick>=brick_trade_ratio+1:
        perform_trade(computer,"brick","wheat",app)
    # If building a settlement is possible and no sheep are available,
    #  trade for sheep if possible
    if len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.sheep==0 and computer.brick>=brick_trade_ratio+1:
        perform_trade(computer,"brick","sheep",app)
    # If building a road isn't possible but building a settlement is
    #  and no wood is available, trade for wood if possible
    if (len(computer.roads)==computer.road_max or len(available_roads)==0) and \
        len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.wood==0 and computer.brick>=brick_trade_ratio+1:
        perform_trade(computer,"brick","wood",app)
    # If building a city is possible and too little wheat/stone is available,
    #  trade for wheat/stone while it's possible
    if len(available_city_points)!=0 and \
        len(computer.cities)<computer.city_max:
        while computer.wheat<2 and computer.brick>=brick_trade_ratio+1:
            perform_trade(computer,"brick","wheat",app)
        while computer.stone<3 and computer.brick>=brick_trade_ratio+1:
            perform_trade(computer,"brick","stone",app)

    # Assume the computer can't do anything and just passes
    action_string = "ended turn"
    # If the computer can place a road, do that
    if len(available_roads)>0 and \
        len(computer.roads)<computer.road_max and \
        computer.wood>=1 and computer.brick>=1:
        action_string = "build road"
    # If the computer can place a settlement, do that instead
    if len(available_settlement_points)>0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.wood>=1 and computer.brick>=1 and computer.sheep>=1 and \
        computer.wheat>=1:
        action_string = "build settlement"
    # If the computer can place a city, do that instead
    if len(available_city_points)>0 and \
        len(computer.cities)<computer.city_max and \
        computer.wheat>=2 and computer.stone>=3:
        action_string = "build city"

    return action_string


def choose_settlement(computer,available_settlement_points,app):
    # Function is called to determine where the computer should place a settlement

    # Should return the point object where the settlement should be built

    tiles = app.pieces.tiles

    # Make a matrix of all the brick tiles
    brick_matrix = []
    for tile in tiles:
        if tile.resource=="brick":
            brick_matrix.append(tile.index)

    # If an available point is on a brick tile, add it to the options
    settlement_options = []
    for element in brick_matrix:
        for point in available_settlement_points:
            if element in point.coordinate:
                settlement_options.append(point)

    # If the brick port is one of the available points, add it to the options
    for point in available_settlement_points:
        if point.is_port:
            if point.port_resource=="brick":
                settlement_options.append(point)

    # If there are no brick tiles open to play on, play on a non-brick tile
    if len(settlement_options)==0:
        settlement_options = available_settlement_points

    # Choose a point with the highest total probabilities to play on
    #  Brick port adds 8, plus an extra 2 for each brick tile it's on
    #  3:1 port adds 4
    best_positions = []
    highest_probability = 18
    while len(best_positions)==0:
        for point in settlement_options:
            point_probability = 0
            for i in point.coordinate:
                point_probability += 7-abs(tiles[i].roll_number-7)
            if point.is_port:
                if point.port_resource=="brick":
                    point_probability += 8
                    for i in point.coordinate:
                        if tiles[i].resource=="brick":
                            point_probability += 2
                elif point.port_resource=="any" or point.port_resource=="?":
                    point_probability += 4
            if point_probability>=highest_probability:
                best_positions.append(point)
        highest_probability -= 1

    settlement = choice(best_positions)

    return settlement


def choose_city(computer,available_city_points,app):
    # Function is called to determine where the computer should place a city

    # Should return the point object where the city should be built

    tiles = app.pieces.tiles

    # Make a matrix of all the brick tiles
    brick_matrix = []
    for tile in tiles:
        if tile.resource=="brick":
            brick_matrix.append(tile.index)

    # If an available point is on a brick tile, add it to the options
    city_options = []
    for element in brick_matrix:
        for point in available_city_points:
            if element in point.coordinate:
                city_options.append(point)

    # If there are no brick tiles open to play on, play on a non-brick tile
    if len(city_options)==0:
        city_options = available_city_points

    # Choose a point with the highest total probabilities to play on
    best_positions = []
    highest_probability = 18
    while len(best_positions)==0:
        for point in city_options:
            point_probability = 0
            for i in point.coordinate:
                point_probability += 7-abs(tiles[i].roll_number-7)
            if point_probability>=highest_probability:
                best_positions.append(point)
        highest_probability -= 1

    city = choice(best_positions)

    return city


def choose_road(computer,available_roads,app):
    # Function is called to determine where the computer should place a road

    # Should return the road object where the road should be built

    tiles = app.pieces.tiles

    # Make a matrix of all the brick tiles
    brick_matrix = []
    for tile in tiles:
        if tile.resource=="brick":
            brick_matrix.append(tile.index)

    # If an available road has both points on a brick tile, add it to options
    road_options = []
    for element1 in brick_matrix:
        for element2 in brick_matrix:
            for rd in available_roads:
                if element1 in rd.point1.coordinate and \
                    element2 in rd.point2.coordinate:
                    road_options.append(rd)

    # If no roads have both points on a brick tile, find roads with just one
    #  point on a brick tile and add it to the options
    if len(road_options)==0:
        for element in brick_matrix:
            for rd in available_roads:
                if element in rd.point1.coordinate or \
                    element in rd.point2.coordinate:
                    road_options.append(rd)

    # If there are no brick tiles open to play on, play on a non-brick tile,
    if len(road_options)==0:
        road_options = available_roads

    # Choose a point with the highest total probabilities to build to
    best_positions = []
    highest_probability = 18
    while len(best_positions)==0:
        for road in road_options:
            point_probability = 0
            # Choose the point that the road is building towards
            if not(road.point1 in computer.points):
                for i in road.point1.coordinate:
                    point_probability += 7-abs(tiles[i].roll_number-7)
            elif not(road.point2 in computer.points):
                for i in road.point2.coordinate:
                    point_probability += 7-abs(tiles[i].roll_number-7)
            # If the computer owns both points, choose the higher probability
            #  to encourage connecting of roads
            else:
                point1_probability = 0
                point2_probability = 0
                for i in road.point1.coordinate:
                    point1_probability += 7-abs(tiles[i].roll_number-7)
                for i in road.point2.coordinate:
                    point2_probability += 7-abs(tiles[i].roll_number-7)
                if point1_probability<point2_probability:
                    point_probability = point1_probability
                else:
                    point_probability = point2_probability
            if point_probability>=highest_probability:
                best_positions.append(road)
        highest_probability -= 1

    road = choice(best_positions)

    return road


def discard(computer,new_resource_count):
    # Function is called for computer to discard resources down to new_resource_count

    # Doesn't return anything, just needs to update the computer's resources

    while computer.resource_count()>new_resource_count:
        # Get rid of brick first, should be easy to get more!
        if computer.brick!=0:
            discarded_resource = "brick"
        # If there's no more brick, get rid of a random resource
        else:
            all_resources = []
            for i in range(computer.wood):
                all_resources.append("wood")
            for i in range(computer.brick):
                all_resources.append("brick")
            for i in range(computer.sheep):
                all_resources.append("sheep")
            for i in range(computer.wheat):
                all_resources.append("wheat")
            for i in range(computer.stone):
                all_resources.append("stone")
            discarded_resource = choice(all_resources)
        if discarded_resource=="wood":
            computer.wood -= 1
        elif discarded_resource=="brick":
            computer.brick -= 1
        elif discarded_resource=="sheep":
            computer.sheep -= 1
        elif discarded_resource=="wheat":
            computer.wheat -= 1
        elif discarded_resource=="stone":
            computer.stone -= 1


def place_robber(computer,original_tile,app):
    # Function is called to determine where the computer should place the robber tile
    #  Can't place the robber where he already is (original_tile)

    # Should return the tile object (from tiles) where the robber should be placed

    # Form a list of the tiles with players on them
    occupied_tiles = []
    for tile in app.pieces.tiles:
        for player in app.pieces.players:
            for settlement in player.settlements:
                if tile.index in settlement.coordinate and tile.visible and \
                    not(tile in occupied_tiles):
                    occupied_tiles.append(tile)
            for city in player.cities:
                if tile.index in city.coordinate and tile.visible and \
                    not(tile in occupied_tiles):
                    occupied_tiles.append(tile)

    # Remove tiles that the computer is on from the list
    tiles_to_remove = []
    for tile in occupied_tiles:
        for settlement in computer.settlements:
            if tile.index in settlement.coordinate and \
                not(tile in tiles_to_remove):
                tiles_to_remove.append(tile)
        for city in computer.cities:
            if tile.index in city.coordinate and \
                not(tile in tiles_to_remove):
                tiles_to_remove.append(tile)

    for tile in tiles_to_remove:
        occupied_tiles.remove(tile)

    if original_tile in occupied_tiles:
        occupied_tiles.remove(original_tile)

    robber_tile = Tile(0)
    # If there are no more tiles in the list, choose from all the tiles
    #  Should only rarely happen!
    if len(occupied_tiles)==0:
        occupied_tiles = app.pieces.tiles

    # Choose the tile(s) producing the most resources
    best_positions = []
    highest_resources = 36
    # If there are brick tiles not occupied by computer, but by other players,
    #  prioritize those
    for tile in occupied_tiles:
        if tile.resource=="brick":
            best_positions.append(tile)
    if len(best_positions)!=0:
        occupied_tiles = list(best_positions)
        best_positions = []
    while len(best_positions)==0:
        for tile in occupied_tiles:
            generation_count = 0
            for player in app.pieces.players:
                for settlement in player.settlements:
                    if tile.index in settlement.coordinate:
                        generation_count += 7-abs(tile.roll_number-7)
                for city in player.cities:
                    if tile.index in city.coordinate:
                        generation_count += 2*(7-abs(tile.roll_number-7))
            if generation_count>=highest_resources:
                best_positions.append(tile)
        highest_resources -= 1

    while not(robber_tile.visible):
        robber_tile = choice(best_positions)
        if robber_tile==original_tile:
            robber_tile = Tile(0)

    return robber_tile


def choose_target(computer,stealable_players):
    # Function is called to pick a player from stealable_players to take a random resource from

    # Should return the player chosen

    # Steal from the player with the most resources
    players_to_steal_from = []
    max_resources = 0
    for player in stealable_players:
        if player.resource_count()>=max_resources:
            players_to_steal_from.append(player)
            max_resources = player.resource_count()

    target_player = choice(players_to_steal_from)

    return target_player
