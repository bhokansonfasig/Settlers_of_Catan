from random import choice
from point import Point
from road import Road

def computer_choose_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""
    if computer.AI_code==1:
        # Randomly place settlement
        available_points = legal_settlement_placements(computer,players)
        return choice(available_points)
    else:
        # Place settlement in the ocean
        return Point(0,1,7)


def computer_choose_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""
    if computer.AI_code==1:
        # Randomly place road
        available_roads = legal_road_placements(player,players)
        return choice(available_roads)
    else:
        # Place road in the ocean
        return Road(Point(0,1,7),Point(1,7,8))


def computer_choose_city(computer,players):
    """Has computer place city. Returns tuple of the placed settlement"""
    if computer.AI_code==1:
        # Randomly place city
        available_points = []
        for point in computer.settlements:
            available_points.append(point)
        return choice(available_points)
    else:
        # Place city in the ocean
        return Point(0,1,7)
