from random import choice
from road import Road
from point import Point
from player import Player


players = [Player(0,"Aman",-1),Player(1,"Ben",-1)] #for testing
################################################################################
# Function definitions

def set_tiles(tiles):
    """Takes array of tiles and sets resources and dice roll numbers to the
    appropriate game board tiles"""
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
                if tile1.has_neighbor(tile2):
                    acceptable_placement = False

    return tiles

#adds the point to the list of points that a player _already_ has access to via built roads
def add_point(point,player):
    if(point not in player.points):
        player.points.append(point)


def legal_settlement_placements(player,players):
    """Returns an array of points where the player can place a settlement"""
    points = [Point(9,16,17),Point(9,10,17),Point(16,17,23),Point(17,23,24),
        Point(17,18,24),Point(39,40,47)]

    return points


#this function, apart from making a legal road will also return True or False depending on whether it succeeded or not
def legal_road_placements(player,players):
    x1 = int(input("x1:"))
    y1 = int(input("y1:"))
    z1 = int(input("z1:"))

    x2 = int(input("x2:"))
    y2 = int(input("y2:"))
    z2 = int(input("z2:"))

    p1 = Point(x1,y1,z1)
    p2 = Point(x2,y2,z2)
    r = Road(p1,p2)

    if(r.valid):
        #road have to be connected to some structure (road/city/settlement), ie "acccess points"
        connected = (p1 in player.points) or (p2 in player.points)
        #check all the roads to see if the road is not replacing any other road
        new_road = True
        for x in [0,len(players)-1]:
            new_road = new_road and (r not in players[x].roads)
            if(not new_road):
                break

        if (new_road and (connected or len(player.roads)==0)): #let the player build it anywhere if he has no roads in the begining
            player.roads.append(r)
            print(player.name,"'s", "road list appended.")
            add_point(p1,player)
            add_point(p2,player)
            return True
        elif (not new_road):
            print("That edge already has a road.")
            return False
        else:
            print("Can't build a disconnected road.")
            return False
    else:
        print("Invalid road.")
        return False



def give_resource(resource,player):
    """Gives player a card of resource type 'resource'"""
    pass


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

    # Probably want to call give_resource in here

    pass


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    i=0
    while(True):
        print("Turn: ",i+1,"\n")
        legal_road_placements(players[i%2],players)
        for k in [0,len(players)-1]:
            print(players[k].name," has ",len(players[k].roads)," roads and ",len(players[k].points),"access points.")
            # for l in [0,len(players[k].roads)-1]:
            #     print(players[k].name,"\n",players[k].roads[l].coordinates,"\n")
        i += 1
