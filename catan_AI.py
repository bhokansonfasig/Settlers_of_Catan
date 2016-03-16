from random import choice
from point import Point
from road import Road
from tiles import Tile
from importlib import import_module


def set_computer(name):
    """Checks the name of the computer against known computer personalities.
        Returns AI level if known, or 0 if unknown."""
    from os import listdir
    from os.path import isfile, join

    AI_files = [f[:-3] for f in listdir('./AI_files') \
        if isfile(join('./AI_files',f)) and 'AI' in f and not('template' in f)]
    global AI_modules
    AI_modules = []
    for AI_file in AI_files:
        AI_modules.append(import_module("AI_files."+AI_file))

    if len(AI_modules)==0:
        print("No AI modules found. All computers will play randomly.")
        name = 'Random'

    random_play_aliases = ["random","randy","randy the random",
                            "rachel","rachel the random"]

    # If the name is one of the random play names, set to random AI
    if name.lower() in random_play_aliases:
        return name,0

    all_aliases = []
    all_codes = []
    for AI in AI_modules:
        aliases = AI.get_aliases()
        code = AI.get_code()
        for alias in aliases:
            if alias in all_aliases:
                print("Caution: name",alias,"exists in two AI files.\n",
                        "May cause unexpected behavior")
                break
            all_aliases.append(alias)
        if code in all_codes:
            print("Caution: AI code",code,"refers to two different AI files.\n",
                    "May cause unexpected behavior")
        all_codes.append(code)
        if name.lower() in aliases:
            return name,code

    valid_AI = False
    while not(valid_AI):
        # If the name is not found, give it one of the known AI personalities
        code = choice(all_codes)
        # Print a note of which AI was chosen
        for AI in AI_modules:
            match = AI.get_code()
            if match==code:
                # Ignore AIs with difficulty level 0
                if AI.get_difficulty()>0:
                    aliases = AI.get_aliases()
                    print("Computer with name",name,"set to AI",aliases[0])
                    valid_AI = True
                break
    # # Changes the name of the computer
    # return aliases[0].capitalize(),code
    # Doesn't change the name of the computer
    return name,code


def computer_choose_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""
    from catan_logic import legal_settlement_placements

    available_points = legal_settlement_placements(computer,players)

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            settlement = AI.choose_settlement(computer,players,available_points)
            found = True
            break
    if not(found):
        # Randomly place settlement
        settlement = choice(available_points)

    return settlement


def computer_choose_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""
    from catan_logic import legal_road_placements

    available_roads = legal_road_placements(computer,players)

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            road = AI.choose_road(computer,players,available_roads)
            found = True
            break
    if not(found):
        # Randomly place road
        road = choice(available_roads)

    return road


def computer_choose_city(computer,players):
    """Has computer place city. Returns tuple of the placed settlement"""

    available_points = []
    for point in computer.settlements:
        available_points.append(point)

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            city = AI.choose_city(computer,players,available_points)
            found = True
            break
    if not(found):
        # Randomly place road
        city = choice(available_points)

    return city


def computer_discard(computer,new_resource_count):
    """Computer must discard to get down to new_resource_count"""

    starting_resource_count = computer.resource_count()

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            AI.discard(computer,new_resource_count)
            found = True
            break
    if not(found):
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

    for tile in tiles:
        if tile.has_robber:
            original_tile = tile
            break

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            robber_tile = AI.place_robber(computer,players,tiles,original_tile)
            found = True
            break
    if not(found):
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

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            target_player = AI.choose_target(computer,players,stealable_players)
            found = True
            break
    if not(found):
        # Choose target randomly
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

    available_settlement_points = legal_settlement_placements(computer,players)
    available_roads = legal_road_placements(computer,players)
    available_city_points = computer.settlements

    found = False
    for AI in AI_modules:
        if computer.AI_code==AI.get_code():
            action_string = AI.take_turn(computer,players,
                available_settlement_points,available_roads,
                available_city_points)
            found = True
            break
    if not(found):
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


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    print(set_computer('Ben'))
