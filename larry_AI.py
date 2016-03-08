from random import choice
from point import Point
from road import Road
from tiles import Tile

# Larry the lumberjack focuses on monopolizing wood

def larry_take_turn(computer,players,available_settlement_points,
    available_roads,available_city_points):
    # Function is called to determine what action the computer should take

    # Should return "build settlement", "build road", "build city", or "ended turn"

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

    settlement = choice(available_settlement_points)

    return settlement


def larry_choose_city(computer,players,available_city_points):
    # Function is called to determine where the computer should place a city

    # Should return the point object where the city should be built

    city = choice(available_city_points)

    return city


def larry_choose_road(computer,players,available_roads):
    # Function is called to determine where the computer should place a road

    # Should return the road object where the road should be built

    road = choice(available_roads)

    return road


def larry_discard(computer,new_resource_count):
    # Function is called for computer to discard resources down to new_resource_count

    # Doesn't return anything, just needs to update the computer's resources

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


def larry_place_robber(computer,tiles,original_tile):
    # Function is called to determine where the computer should place the robber tile
    #  Can't place the robber where he already is (original_tile)

    # Should return the tile object (from tiles) where the robber should be placed

    robber_tile = Tile(0)
    while not(robber_tile.visible):
        robber_tile = choice(tiles)
        if robber_tile==original_tile:
            robber_tile = Tile(0)

    return robber_tile


def larry_choose_target(computer,players,stealable_players):
    # Function is called to pick a player from stealable_players to take a random resource from

    # Should return the player chosen

    target_player = choice(stealable_players)

    return target_player
