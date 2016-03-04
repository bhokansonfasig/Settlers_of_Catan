from random import choice
from point import Point
from road import Road
from tiles import Tile


def set_computer(name):
    """Checks the name of the computer against known computer personalities.
        Returns AI level if known, or 0 if unknown."""
    if name.lower()=="idiot" or name.lower()=="ocean":
        return 99
    elif name.lower()=="random":
        return 0
    else:
        return 0


def computer_choose_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""
    from catan_logic import legal_settlement_placements
    if computer.AI_code==99:
        # Place settlement in the ocean
        return Point(0,1,7)
    else:
        # Randomly place settlement
        available_points = legal_settlement_placements(computer,players)
        return choice(available_points)


def computer_choose_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""
    from catan_logic import legal_road_placements
    if computer.AI_code==99:
        # Place road in the ocean
        return Road(Point(0,1,7),Point(1,7,8))
    else:
        # Randomly place road
        available_roads = legal_road_placements(computer,players)
        return choice(available_roads)


def computer_choose_city(computer,players):
    """Has computer place city. Returns tuple of the placed settlement"""
    if computer.AI_code==99:
        # Place city in the ocean
        return Point(0,1,7)
    else:
        # Randomly place city
        available_points = []
        for point in computer.settlements:
            available_points.append(point)
        return choice(available_points)


def computer_place_robber(computer,tiles):
    """Has computer place robber. Returns tile where robber was placed"""
    for tile in tiles:
        if tile.has_robber:
            original_tile = tile
            break
    if computer.AI_code==99:
        # Place robber in ocean
        return Tile(7)
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
        
    if len(stealable_players)==0:
        return

    if computer.AI_code==99:
        pass
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
        if stolen_resource=="brick":
            target_player.brick -= 1
            computer.brick += 1
        if stolen_resource=="sheep":
            target_player.sheep -= 1
            computer.sheep += 1
        if stolen_resource=="wheat":
            target_player.wheat -= 1
            computer.wheat += 1
        if stolen_resource=="stone":
            target_player.stone -= 1
            computer.stone += 1

    write_log(computer.name,"stole a resource from",target_player.name)



def computer_take_turn(computer,players):
    """Defines what the computer does in its turn"""
    from catan_logic import legal_settlement_placements, legal_road_placements
    from catan_logic import build_settlement, build_road, build_city
    if computer.AI_code==99:
        pass
    else:
        # If the computer can place a city, place a city randomly
        available_points = computer.settlements
        if len(available_points)>0 and \
            len(computer.cities)<computer.city_max and \
            computer.wheat>=2 and computer.stone>=3:
            city = build_city(computer,players)
            city_string = "built a city at "+str(city.coordinate)
            return city_string
        # If the computer can place a settlement, place a settlement randomly
        available_points = legal_settlement_placements(computer,players)
        if len(available_points)>0 and \
            len(computer.settlements)<computer.settlement_max and \
            computer.wood>=1 and computer.brick>=1 and computer.sheep>=1 and \
            computer.wheat>=1:
            settlement = build_settlement(computer,players)
            set_string = "built a settlement at "+str(settlement.coordinate)
            return set_string
        # If the computer can place a road, place a road randomly
        available_roads = legal_road_placements(computer,players)
        if len(available_roads)>0 and \
            len(computer.roads)<computer.road_max and \
            computer.wood>=1 and computer.brick>=1:
            road = build_road(computer,players)
            road_string = "built a road at "+str(road.coordinates)
            return road_string
        # If nothing has been done, stop
        return "ended turn"
