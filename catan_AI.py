from random import choice
from point import Point
from road import Road
from tiles import Tile


def set_computer(name):
    """Checks the name of the computer against known computer personalities.
        Returns AI level if known, or 0 if unknown."""
    if name.lower()=="idiot" or name.lower()=="ocean":
        return 99
    # Template for adding new AI:
    # elif name.lower()=="AIname":
    #     return AIcode
    elif name.lower()=="larry" or name.lower()=="larry the lumberjack" or \
        name.lower()=="wood":
        return 1
    elif name.lower()=="random":
        return 0
    else:
        return 0


def computer_choose_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""
    from catan_logic import legal_settlement_placements
    # from AIname_file import AIname_choose_settlement
    from larry_AI import larry_choose_settlement

    available_points = legal_settlement_placements(computer,players)

    if computer.AI_code==99:
        # Place settlement in the ocean
        settlement = Point(0,1,7)
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     settlement = AIname_choose_settlement(computer,players,
    #         available_points)
    elif computer.AI_code==1:
        settlement = larry_choose_settlement(computer,players,available_points)
    else:
        # Randomly place settlement
        settlement = choice(available_points)

    return settlement


def computer_choose_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""
    from catan_logic import legal_road_placements
    # from AIname_file import AIname_choose_road
    from larry_AI import larry_choose_road

    available_roads = legal_road_placements(computer,players)

    if computer.AI_code==99:
        # Place road in the ocean
        road = Road(Point(0,1,7),Point(1,7,8))
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     road = AIname_choose_road(computer,players,available_roads)
    elif computer.AI_code==1:
        road = larry_choose_road(computer,players,available_roads)
    else:
        # Randomly place road
        road = choice(available_roads)

    return road


def computer_choose_city(computer,players):
    """Has computer place city. Returns tuple of the placed settlement"""
    # from AIname_file import AIname_choose_city
    from larry_AI import larry_choose_city

    available_points = []
    for point in computer.settlements:
        available_points.append(point)

    if computer.AI_code==99:
        # Place city in the ocean
        city = Point(0,1,7)
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     city = AIname_choose_city(computer,players,available_points)
    elif computer.AI_code==1:
        city = larry_choose_city(computer,players,available_points)
    else:
        # Randomly place city
        city = choice(available_points)

    return city


def computer_discard(computer,new_resource_count):
    """Computer must discard to get down to new_resource_count"""
    # from AIname_file import AIname_discard
    from larry_AI import larry_discard

    starting_resource_count = computer.resource_count()

    if computer.AI_code==99:
        # Get rid of all cards
        computer.wood = 0
        computer.brick = 0
        computer.sheep = 0
        computer.wheat = 0
        computer.stone = 0
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     AIname_discard(computer,new_resource_count)
    elif computer.AI_code==1:
        larry_discard(computer,new_resource_count)
    else:
        # Radomly get rid of resources
        while computer.resource_count()>new_resource_count:
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

    discard_count = starting_resource_count - computer.resource_count()
    return discard_count


def computer_place_robber(computer,players,tiles):
    """Has computer place robber. Returns tile where robber was placed"""
    # from AIname_file import AIname_place_robber
    from larry_AI import larry_place_robber

    for tile in tiles:
        if tile.has_robber:
            original_tile = tile
            break
    if computer.AI_code==99:
        # Place robber in ocean
        robber_tile = Tile(7)
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     robber_tile = AIname_place_robber(computer,players,tiles,original_tile)
    elif computer.AI_code==1:
        robber_tile = larry_place_robber(computer,players,tiles,original_tile)
    else:
        # Place robber randomly
        robber_tile = Tile(0)
        while not(robber_tile.visible):
            robber_tile = choice(tiles)
            if robber_tile==original_tile:
                robber_tile = Tile(0)

    return robber_tile


def computer_steal_resource(computer,players,robber_tile):
    """Has computer select a player to steal from"""
    from catan_graphics import write_log
    # from AIname_file import AIname_choose_target
    from larry_AI import larry_choose_target

    stealable_players = []
    for guy in players:
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
    if computer in stealable_players:
        stealable_players.remove(computer)
    for guy in stealable_players:
        if guy.resource_count()==0:
            stealable_players.remove(guy)

    if len(stealable_players)==0:
        return

    if computer.AI_code==99:
        return
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     target_player = \
    #         AIname_choose_target(computer,players,stealable_players)
    elif computer.AI_code==1:
        target_player = larry_choose_target(computer,players,stealable_players)
    else:
        target_player = choice(stealable_players)

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
        computer.wood += 1
    elif stolen_resource=="brick":
        target_player.brick -= 1
        computer.brick += 1
    elif stolen_resource=="sheep":
        target_player.sheep -= 1
        computer.sheep += 1
    elif stolen_resource=="wheat":
        target_player.wheat -= 1
        computer.wheat += 1
    elif stolen_resource=="stone":
        target_player.stone -= 1
        computer.stone += 1

    write_log(computer.name,"stole a resource from",target_player.name)



def computer_take_turn(computer,players):
    """Defines what the computer does in its turn"""
    from catan_logic import legal_settlement_placements, legal_road_placements
    from catan_logic import build_settlement, build_road, build_city
    # from AIname_file import AIname_take_turn
    from larry_AI import larry_take_turn

    available_settlement_points = legal_settlement_placements(computer,players)
    available_roads = legal_road_placements(computer,players)
    available_city_points = computer.settlements

    if computer.AI_code==99:
        pass
    # Template for adding new AI:
    # elif computer.AI_code==AIcode:
    #     action_string = AIname_take_turn(computer,players,
    #         available_settlement_points,available_roads,available_city_points)
    elif computer.AI_code==1:
        action_string = larry_take_turn(computer,players,
            available_settlement_points,available_roads,available_city_points)
    else:
        action_options = []
        # If the computer can place a road, add that as an option
        if len(available_roads)>0 and \
            len(computer.roads)<computer.road_max and \
            computer.wood>=1 and computer.brick>=1:
            action_options.append("build road")
        # If the computer can place a settlement, add that as an option
        if len(available_settlement_points)>0 and \
            len(computer.settlements)<computer.settlement_max and \
            computer.wood>=1 and computer.brick>=1 and computer.sheep>=1 and \
            computer.wheat>=1:
            action_options.append("build settlement")
        # If the computer can place a city, add that as an option
        if len(available_city_points)>0 and \
            len(computer.cities)<computer.city_max and \
            computer.wheat>=2 and computer.stone>=3:
            action_options.append("build city")
        # Choose from the options
        if len(action_options)==0:
            action_string = "ended turn"
        else:
            action_string = choice(action_options)


    if action_string.lower()=="build city":
        city = build_city(computer,players)
        city_string = "built a city at "+str(city.coordinate)
        return city_string
    elif action_string.lower()=="build settlement":
        settlement = build_settlement(computer,players)
        set_string = "built a settlement at "+str(settlement.coordinate)
        return set_string
    elif action_string.lower()=="build road":
        road = build_road(computer,players)
        road_string = "built a road at "+str(road.coordinates)
        return road_string
    else:
        return "ended turn"
