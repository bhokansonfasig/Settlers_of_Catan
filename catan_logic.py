from random import choice
from road import *
from point import Point
from player import Player


################################################################################
# Function definitions

def set_tiles(tiles):
    """Takes array of tiles and sets resources and dice roll numbers to the
    appropriate game board tiles"""

    # Prepare all_points and all_roads for later use
    #the leftmost points on the grid, which are used to generate the rest
    seed_points = [[0,1,7],[1,7,8],[7,8,15],[7,14,15],[14,15,21],[15,21,22],[21,28,29],[21,22,29],[28,29,35],[29,35,36],[35,42,43],[35,36,43]]
    global all_points, all_roads
    all_points = []
    all_roads = []

    generate_points_and_roads(seed_points)

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
        #print("Placing numbers")
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

    docks = ["wood","brick","sheep","wheat","stone","any","any","any","any"]
    # Assign ports randomly (positions are already fixed)
    for tile in tiles:
        if tile.dock:
            dock_resource = choice(docks)
            docks.remove(dock_resource)
            for point in all_points:
                if (tile.index in point.coordinate) and point.is_port:
                    point.make_port(dock_resource)

    return tiles


def generate_points_and_roads(seed_points):
    """Generates all the points on the grid and stores them in all_points"""

    for s in seed_points: #generate points
        i = 0
        while(i<6):
            p = Point(s[0]+i,s[1]+i,s[2]+i)
            if(p.valid):
                all_points.append(p)
            i += 1

    for p1 in all_points: #generate roads
        for p2 in all_points:
            r = Road(p1,p2)
            if(r not in all_roads and r.valid):
                all_roads.append(r)


def build_settlement(player,players):
    from catan_graphics import player_choose_settlement, draw_settlement
    from catan_graphics import write_log
    from catan_AI import computer_choose_settlement
    # If the player can't build a settlement, exit without building anything
    available_points = legal_settlement_placements(player,players)
    if len(available_points)==0:
        print("Nowhere to build a new settlement!")
        return
    if len(player.settlements)>=player.settlement_max:
        print("Already built maximum number of settlements!")
        return

    # Unless it's the first round of placements, take resources away
    if len(player.roads)>1:
        # Make sure the player has the necessary resources first
        if player.wood<1 or player.brick<1 or player.sheep<1 or player.wheat<1:
            print("Not enough resources to build a settlement!")
            return
        player.wood -= 1
        player.brick -= 1
        player.wheat -= 1
        player.sheep -= 1
    # Get the point for the settlement to be built
    if player.AI_code<0:
        settlement = player_choose_settlement(player,players)
    else:
        settlement = computer_choose_settlement(player,players)
    # If the player didn't choose a settlement, refund resources and exit
    if not(settlement):
        player.wood += 1
        player.brick += 1
        player.wheat += 1
        player.sheep += 1
        return
    # Update the player's building list
    player_building_update(settlement,1,player)
    # Draw the settlement on the board
    draw_settlement(settlement,player)
    # Write to log where player built settlement
    write_log(player.name,"built a settlement at",settlement.coordinate)
    # Recalculate the player's score
    player.calculate_score()

    return settlement


def build_road(player,players):
    from catan_graphics import player_choose_road, draw_road, write_log
    from catan_AI import computer_choose_road
    # If the player can't build a road, exit without building anything
    available_roads = legal_road_placements(player,players)
    if len(available_roads)==0:
        print("Nowhere to build a new road!")
        return
    if len(player.roads)>=player.road_max:
        print("Already built maximum number of roads!")
        return

    # Unless it's the first round of placements, take resources away
    if len(player.roads)>1:
        # Make sure the player has the necessary resources first
        if player.wood<1 or player.brick<1:
            print("Not enough resources to build a road!")
            return
        player.wood -= 1
        player.brick -= 1
    # Get the points for the road to be built
    if player.AI_code<0:
        road = player_choose_road(player,players)
    else:
        road = computer_choose_road(player,players)
    # If the player didn't choose a road, refund resources and exit
    if not(road):
        player.wood += 1
        player.brick += 1
        return
    # Update the player's road and point lists
    player.roads.append(road)
    player.points.append(road.point1)
    player.points.append(road.point2)
    # Draw the road on the board
    draw_road(road,player)
    # Write to log where player built road
    write_log(player.name,"built a road at",road.coordinates)
    # Recalculate the player's score
    player.calculate_score()

    player.isolate_loops()
    player.find_complex_edges()

    return road


def build_city(player,players):
    from catan_graphics import player_choose_city, draw_city, write_log
    from catan_AI import computer_choose_city
    # If the player can't build a city, exit without building anything
    available_points = player.settlements
    if len(available_points)==0:
        print("Nowhere to build a new city!")
        return
    if len(player.cities)>=player.city_max:
        print("Already built maximum number of cities!")
        return
    if player.wheat<2 or player.stone<3:
        print("Not enough resources to build a city!")
        return

    # Take resources away
    player.stone -= 3
    player.wheat -= 2
    # Get the point for the city to be built
    if player.AI_code<0:
        city = player_choose_city(player,players)
    else:
        city = computer_choose_city(player,players)
    # If the player didn't choose a city, refund resources and exit
    if not(city):
        player.stone += 3
        player.wheat += 2
        return
    # Update the player's building list
    player_building_update(city,2,player)
    # Draw the city on the board
    draw_city(city,player)
    # Write to log where player built city
    write_log(player.name,"built a city at",city.coordinate)
    # Recalculate the player's score
    player.calculate_score()

    return city


#adds the point to the list of points that a player _already_ has access to via built roads
def add_point(point,player):
    if(point not in player.points):
        player.points.append(point)


def legal_settlement_placements(player,players):
    """Returns an array of points where the player can place a settlement"""
    points = []
    occupied_points = occupied_points_on_board(players)

    if(len(player.roads)<2 and len(player.settlements)<2): #first turn
        for p in all_points:
            if((not p.locate_point(occupied_points)) and (not p.adjacent_point_list(occupied_points))):
                points.append(p)

        if(len(points) == 0):#first guy to place something on the board, there are no occupied points so points.append(p) never happens
            return all_points
        else:
            return points

    else:
        for p in player.points:
            if (p.locate_point(occupied_points) or p.adjacent_point_list(occupied_points)):
                continue
            else:
                points.append(p)
        return points



def legal_road_placements(player,players):
    road_options = []

    if(len(player.roads)==1):#force the second road with the second settlement when the game starts
        for road in all_roads:
            if(road.point1 == player.settlements[1] or road.point2 == player.settlements[1]):
                road_options.append(road)
        return road_options

    for road in all_roads:
        #road has to be connected to some structure (road/city/settlement), ie "acccess points"
        connected = (road.point1 in player.points) or (road.point2 in player.points)
        #check all the roads to see if the road is not replacing any other road
        new_road = True
        for x in range(0,len(players)):
            new_road = new_road and (road not in players[x].roads)
            if(not new_road):
                break

        if (new_road and connected): #its assumed that the first object the player puts on the board is a settlement
            road_options.append(road)

    return road_options


def point_resources(point,tiles):
    """Gets resources on hexagons connected to 'point'"""
    output = []
    for hexagon in point.coordinate:
        for tile in tiles:
            if(hexagon == tile.index):
                output.append(tile.resource)
    return output


def check_winner(players):
    """Checks winning condition for all players. Returns list of player indices
        of players who have won, empty list otherwise."""

    # # Temporary way of breaking out of loop
    # winner = eval(input("Who won? "))

    winners = []

    for player in players:
        player.calculate_score()
        if player.score>=10:
            winners.append(player.index)

    return winners


def roll_dice():
    from catan_graphics import write_log
    """Rolls two six sided dice and returns their values."""
    die_values = [1,2,3,4,5,6]
    die_1 = choice(die_values)
    die_2 = choice(die_values)
    write_log("Rolled",die_1,"+",die_2,"=",die_1+die_2)
    return die_1, die_2


def distribute_resources(dice_value,tiles,players):
    """Distributes the appropriate resources to players with settlements on
    hexagons with number 'dice_value'"""

    hexes = []

    for tile in tiles:
        if(dice_value == tile.roll_number):
            hexes.append(tile)


    for tile in hexes:
        for player in players:
            #resource from settlement
            for settlement in player.settlements:
                if (tile.index in settlement.coordinate):
                    player.give_resource(tile.resource)
            #resources from city
            for city in player.cities:
                if(tile.index in city.coordinate):
                    player.give_resource(tile.resource)
                    player.give_resource(tile.resource)



def find_vertices(tile):
    vertices = []
    for p in all_points:
        if(tile.index in p.coordinate):
            vertices.append(p)
    return vertices



#updates the player obj with the buidling info
def player_building_update(point,build_type,player):
    point.building = build_type

    found = False
    for p in player.points:
        if(point == p):
            p.building = build_type
            found = True
            if(build_type == 1):
                player.settlements.append(p)
            else:
                player.cities.append(p)
                player.settlements.remove(p)
            break
    if not found:
        player.points.append(point)
        if(build_type == 1):
            player.settlements.append(point)
        else:
            player.cities.append(point)
            player.settlements.remove(point)

def occupied_points_on_board(players):
    points = []
    for player in players:
        for settlement in player.settlements:
            points.append(settlement)
        for city in player.cities:
            points.append(city)
    return points


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    # i=0
    while(True):
        print("Turn: ",i+1,"\n")
        legal_road_placements(players[i%2],players)
        for k in range[0,len(players)-1]:
            print(players[k].name," has ",len(players[k].roads)," roads.")
            # for l in [0,len(players[k].roads)-1]:
            #     print(players[k].name,"\n",players[k].roads[l].coordinates,"\n")
        i += 1
    print(len(all_roads))
