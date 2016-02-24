from random import choice


################################################################################
# Set up logic classes

# Classes for roads and settlements?


################################################################################
# Function definitions

def randomize(array):
    """Mix the elements of array and return it"""

    return array

def set_tiles(tiles):
    """Takes array of tiles and sets resources and dice roll numbers to the
    appropriate game board tiles"""
    from construction import neighbor_tile

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

    for tile in tiles:
        if tile.visible:
            # Pick a random resource
            tile.resource = choice(resources)
            # Remove one copy of that resource from the remaining choices
            resources.remove(tile.resource)

    acceptable_placement = False
    # Loop through number placement until high numbers are not adjacent
    while not(acceptable_placement):
        print("Placing numbers")
        numbers = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
        for tile in tiles:
            # Pick a random dice value and remove it from the remaining choices
            #  unless the resource is "desert", then set dice value to 0
            if tile.resource!="none" and tile.resource=="desert":
                tile.roll_number = 0
            elif tile.resource!="none":
                tile.roll_number = choice(numbers)
                numbers.remove(tile.roll_number)
        # Assume the placement is good
        acceptable_placement = True
        # Check each tile to be sure tiles with a 6 or 8 are not adjacent
        for tile1 in tiles:
            for tile2 in tiles:
                # If the tiles are not both 6 or 8, just skip
                if not((tile1.roll_number==6 or tile1.roll_number==8) and
                    (tile2.roll_number==6 or tile2.roll_number==8)):
                    continue
                if neighbor_tile(tile1.index,tile2.index):
                    acceptable_placement = False


    return tiles


def set_stats(number_of_players):
    """Doesn't do anything really. Just here to set up the player_stats array"""
    # Player statistics array, one row for each player
    #  0 - Owned settlements
    #  1 - Owned cities
    #  2 - Owned resources (cards)
    #  3 - Owned development cards
    #  4 - Victory points
    global player_stats
    player_stats = []
    for i in range(number_of_players):
        player_stats.append([[], [], [], [], 0])

    return player_stats


#def get_stats():
#    """Returns player statistics array"""
#    return player_stats


def claim_settlement(point,player_index,player_stats):
    """Gives claim of the settlement at 'point' to player number 'index'"""

    return player_stats


def claim_road(side,player_index,player_stats):
    """Gives claim of the road at 'side' to player number 'index'"""

    return player_stats


def give_card(resource,player_index,player_stats):
    """Gives player number 'index' a card of resource type 'resource'"""

    return player_stats


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
