from random import choice

def computer_choose_settlement(computer,players):
    """Has computer place settlement. Returns tuple of the placed settlement"""

    return Point(0,1,7)


def computer_choose_road(computer,players):
    """Has computer place road. Returns tuples of the placed road"""

    return Road(Point(0,1,7),Point(1,7,8))


def computer_choose_city(computer,players):
    """Has computer place city. Returns tuple of the placed settlement"""

    return Point(0,1,7)
