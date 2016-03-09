from random import choice
from point import Point
from road import Road
from tiles import Tile

# Larry the lumberjack focuses on monopolizing wood

def larry_take_turn(computer,players,available_settlement_points,
    available_roads,available_city_points):
    from catan_logic import perform_trade
    # Function is called to determine what action the computer should take

    # Should return "build settlement", "build road", "build city", or "ended turn"

    # Check current wood trade ratio
    wood_trade_ratio = 4
    if "any" in computer.ports or "?" in computer.ports:
        wood_trade_ratio = 3
    if "wood" in computer.ports:
        wood_trade_ratio = 2

    # If building a road or settlement is possible and no bricks are available,
    #  trade for brick if possible
    if (len(available_roads)!=0 or len(available_settlement_points)!=0) and \
        len(computer.roads)<computer.road_max and \
        len(computer.settlements)<computer.settlement_max and \
        computer.brick==0 and computer.wood>=wood_trade_ratio+1:
        perform_trade(computer,"wood","brick")
    # If building a settlement is possible and no wheat are available,
    #  trade for wheat if possible
    if len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.wheat==0 and computer.wood>=wood_trade_ratio+1:
        perform_trade(computer,"wood","wheat")
    # If building a settlement is possible and no sheep are available,
    #  trade for sheep if possible
    if len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.sheep==0 and computer.wood>=wood_trade_ratio+1:
        perform_trade(computer,"wood","sheep")
    # If building a road isn't possible but building a settlement is
    #  and no bricks are available, trade for brick if possible
    if (len(computer.roads)==computer.road_max or len(available_roads)==0) and \
        len(available_settlement_points)!=0 and \
        len(computer.settlements)<computer.settlement_max and \
        computer.brick==0 and computer.wood>=wood_trade_ratio+1:
        perform_trade(computer,"wood","brick")
    # If building a city is possible and too little wheat/stone is available,
    #  trade for wheat/stone while it's possible
    if len(available_city_points)!=0 and \
        len(computer.cities)<computer.city_max:
        while computer.wheat<2 and computer.wood>=wood_trade_ratio+1:
            perform_trade(computer,"wood","wheat")
        while computer.stone<3 and computer.wood>=wood_trade_ratio+1:
            perform_trade(computer,"wood","stone")

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


def larry_choose_settlement(computer,players,available_settlement_points):
    # Function is called to determine where the computer should place a settlement

    # Should return the point object where the settlement should be built

    from catan_graphics import get_tiles
    tiles = get_tiles()

    # Make a matrix of all the wood tiles, with their weighted probabilities
    wood_matrix = []
    for tile in tiles:
        if tile.resource=="wood":
            wood_matrix.append([int((7-abs(tile.roll_number-7))**2),
                tile.index])

    # If an available point is on a wood tile, add it to the options a number
    #  of times indicated by the probability from above
    settlement_options = []
    for element in wood_matrix:
        for point in available_settlement_points:
            if element[1] in point.coordinate:
                for i in range(element[0]):
                    settlement_options.append(point)

    # If the wood port is one of the available points, add it a bunch of times
    #  Especially if it's on a wood tile too!
    for point in available_settlement_points:
        if point.is_port:
            if point.port_resource=="wood":
                for element in wood_matrix:
                    if element[1] in point.coordinate:
                        for i in range(50):
                            settlement_options.append(point)
                    else:
                        for i in range(20):
                            settlement_options.append(point)

    # If there are no wood tiles open to play on, play on a non-wood tile,
    #  otherwise choose one of the wood tiles
    if len(settlement_options)==0:
        settlement = choice(available_settlement_points)
    else:
        settlement = choice(settlement_options)

    return settlement


def larry_choose_city(computer,players,available_city_points):
    # Function is called to determine where the computer should place a city

    # Should return the point object where the city should be built

    from catan_graphics import get_tiles
    tiles = get_tiles()

    # Make a matrix of all the wood tiles, with their weighted probabilities
    wood_matrix = []
    for tile in tiles:
        if tile.resource=="wood":
            wood_matrix.append([int((7-abs(tile.roll_number-7))**2),
                tile.index])

    # If an available point is on a wood tile, add it to the options a number
    #  of times indicated by the probability from above
    city_options = []
    for element in wood_matrix:
        for point in available_city_points:
            if element[1] in point.coordinate:
                for i in range(element[0]):
                    city_options.append(point)

    # If there are no wood tiles open to play on, play on a non-wood tile,
    #  otherwise choose one of the wood tiles
    if len(city_options)==0:
        city = choice(available_city_points)
    else:
        city = choice(city_options)

    return city


def larry_choose_road(computer,players,available_roads):
    # Function is called to determine where the computer should place a road

    # Should return the road object where the road should be built

    from catan_graphics import get_tiles
    tiles = get_tiles()

    # Make a matrix of all the wood tiles, with their weighted probabilities
    wood_matrix = []
    for tile in tiles:
        if tile.resource=="wood":
            wood_matrix.append([int((7-abs(tile.roll_number-7))**2),
                tile.index])

    # If an available road has both points on a wood tile, add it to the options
    #  a number of times indicated by the probability from above
    road_options = []
    for element1 in wood_matrix:
        for element2 in wood_matrix:
            for rd in available_roads:
                if element1[1] in rd.point1.coordinate and \
                    element2[1] in rd.point2.coordinate:
                    for i in range(element1[0]+element2[0]):
                        road_options.append(rd)

    # If no roads have both points on a wood tile, find roads with just one
    #  point on a wood tile and add it to the options a number of times
    #  indicated by the probability from above
    if len(road_options)==0:
        for element in wood_matrix:
            for rd in available_roads:
                if element[1] in rd.point1.coordinate or \
                    element[1] in rd.point2.coordinate:
                    for i in range(element[0]):
                        road_options.append(rd)

    # If there are no wood tiles open to play on, play on a non-wood tile,
    #  otherwise choose one of the wood tiles
    if len(road_options)==0:
        road = choice(available_roads)
    else:
        road = choice(road_options)

    return road


def larry_discard(computer,new_resource_count):
    # Function is called for computer to discard resources down to new_resource_count

    # Doesn't return anything, just needs to update the computer's resources

    while computer.resource_count()>new_resource_count:
        # Get rid of wood first, should be easy to get more!
        if computer.wood!=0:
            discarded_resource = "wood"
        # If there's no more wood, get rid of a random resource
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


def larry_place_robber(computer,players,tiles,original_tile):
    # Function is called to determine where the computer should place the robber tile
    #  Can't place the robber where he already is (original_tile)

    # Should return the tile object (from tiles) where the robber should be placed

    # Form a list of the tiles with players on them
    occupied_tiles = []
    for tile in tiles:
        for player in players:
            for settlement in player.settlements:
                if tile.index in settlement.coordinate and tile.visible and \
                    not(tile in occupied_tiles):
                    occupied_tiles.append(tile)
            for city in player.cities:
                if tile.index in city.coordinate and tile.visible and \
                    not(tile in occupied_tiles):
                    occupied_tiles.append(tile)

    # Remove tiles that the computer is on from the list
    for tile in occupied_tiles:
        for settlement in computer.settlements:
            if tile.index in settlement.coordinate and \
                tile in occupied_tiles:
                occupied_tiles.remove(tile)
        for city in computer.cities:
            if tile.index in city.coordinate and \
                tile in occupied_tiles:
                occupied_tiles.remove(tile)

    if original_tile in occupied_tiles:
        occupied_tiles.remove(original_tile)

    robber_tile = Tile(0)
    # If there are no more tiles in the list, choose from all the tiles
    #  Otherwise, choose from the list
    if len(occupied_tiles)==0:
        while not(robber_tile.visible):
            robber_tile = choice(tiles)
            if robber_tile==original_tile:
                robber_tile = Tile(0)
    else:
        while not(robber_tile.visible):
            robber_tile = choice(occupied_tiles)
            if robber_tile==original_tile:
                robber_tile = Tile(0)

    return robber_tile


def larry_choose_target(computer,players,stealable_players):
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
