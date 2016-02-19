from random import choice


################################################################################
# Set up logic classes



################################################################################
# Function definitions

def randomize(array):
    """Mix the elements of array and return it"""

    return array

def set_tiles(tiles):
    """Takes array of tiles and sets resources and dice roll numbers to the
    appropriate game board tiles"""

    global active_tiles
    active_tiles = [9,10,11,16,17,18,19,22,23,24,25,26,30,31,32,33,37,38,39]

    # Suggested preset:
    # tiles[1][1] = "wood"
    # tiles[1][2] = 11
    # tiles[2][1] = "sheep"
    # tiles[2][2] = 12
    # tiles[3][1] = "wheat"
    # tiles[3][2] = 9
    # tiles[5][1] = "brick"
    # tiles[5][2] = 4
    # tiles[6][1] = "stone"
    # tiles[6][2] = 6
    # tiles[7][1] = "brick"
    # tiles[7][2] = 5
    # tiles[8][1] = "sheep"
    # tiles[8][2] = 10
    # tiles[10][1] = "desert"
    # tiles[10][2] = 0
    # tiles[11][1] = "wood"
    # tiles[11][2] = 3
    # tiles[12][1] = "wheat"
    # tiles[12][2] = 11
    # tiles[13][1] = "wood"
    # tiles[13][2] = 4
    # tiles[14][1] = "wheat"
    # tiles[14][2] = 8
    # tiles[15][1] = "brick"
    # tiles[15][2] = 8
    # tiles[16][1] = "sheep"
    # tiles[16][2] = 10
    # tiles[17][1] = "sheep"
    # tiles[17][2] = 9
    # tiles[18][1] = "stone"
    # tiles[18][2] = 3
    # tiles[21][1] = "stone"
    # tiles[21][2] = 5
    # tiles[22][1] = "wheat"
    # tiles[22][2] = 2
    # tiles[23][1] = "wood"
    # tiles[23][2] = 6

    # Random layout
    resources = ["wood","wood","wood","wood","brick","brick","brick","sheep",
        "sheep","sheep","sheep","wheat","wheat","wheat","wheat","stone","stone",
        "stone","desert"]

    for i in active_tiles:
        # Pick a random resource
        tiles[i][1] = choice(resources)
        # Remove one copy of that resource from the remaining choices
        resources.remove(tiles[i][1])

    acceptable_placement = False
    # Loop through number placement until high numbers are not adjacent
    while not(acceptable_placement):
        print("Placing numbers")
        numbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        for i in active_tiles:
            # Pick a random dice value and remove it from the remaining choices
            #  unless the resource is "desert", then set dice value to 0
            if tiles[i][1]!="desert":
                tiles[i][2] = choice(numbers)
                numbers.remove(tiles[i][2])
            else:
                tiles[i][2] = 0
        # Assume the placement is good
        acceptable_placement = True
        # Check each tile to be sure tiles with a 6 or 8 are not adjacent
        for i in active_tiles:
            # Note there are two ways adjacent tiles relate, depending on the
            #  offset of the row
            # These can be differentiated by checking if #%7 = #%14
            if (tiles[i][2]==6 or tiles[i][2]==8) and (i%7==i%14):
                if tiles[i-8][2]==6 or tiles[i-8][2]==8:
                    acceptable_placement = False
                if tiles[i-7][2]==6 or tiles[i-7][2]==8:
                    acceptable_placement = False
                if tiles[i-1][2]==6 or tiles[i-1][2]==8:
                    acceptable_placement = False
                if tiles[i+1][2]==6 or tiles[i+1][2]==8:
                    acceptable_placement = False
                if tiles[i+6][2]==6 or tiles[i+6][2]==8:
                    acceptable_placement = False
                if tiles[i+7][2]==6 or tiles[i+7][2]==8:
                    acceptable_placement = False
            if (tiles[i][2]==6 or tiles[i][2]==8) and (i%7!=i%14):
                if tiles[i-7][2]==6 or tiles[i-7][2]==8:
                    acceptable_placement = False
                if tiles[i-6][2]==6 or tiles[i-6][2]==8:
                    acceptable_placement = False
                if tiles[i-1][2]==6 or tiles[i-1][2]==8:
                    acceptable_placement = False
                if tiles[i+1][2]==6 or tiles[i+1][2]==8:
                    acceptable_placement = False
                if tiles[i+7][2]==6 or tiles[i+7][2]==8:
                    acceptable_placement = False
                if tiles[i+8][2]==6 or tiles[i+8][2]==8:
                    acceptable_placement = False

    return tiles


def claim_settlement(point,player_index):
    """Gives claim of the settlement at 'point' to player number 'index'"""
    pass
    # Maybe return array or whatever variable player data is stored in


def claim_road(side,player_index):
    """Gives claim of the road at 'side' to player number 'index'"""
    pass
    # Maybe return array or whatever variable player data is stored in


def give_card(resource,player_index):
    """Gives player number 'index' a card of resource type 'resource'"""
    pass
    # Maybe return list of cards player has?


def point_resources(point):
    """Gets resources on hexagons connected to 'point'"""

    return ["sheep","wheat","stone"]


def check_winner():
    """Checks winning condition for all players. Returns player index if someone
    has won, 0 otherwise."""

    # Temporary way of breaking out of loop
    winner = eval(input("Who won? "))

    return winner


def roll_dice():
    """Rolls two six sided dice and returns their values."""

    return 1,2


def distribute_resources(dice_value):
    """Distributes the appropriate resources to players with settlements on
    hexagons with number 'dice_value'"""

    # Probably want to call give_card in here

    pass


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    print(version)
