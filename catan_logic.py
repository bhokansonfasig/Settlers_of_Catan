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
            #  unless the resource is "desert", then set dice value to 0 and put
            #  the robber there
            if tile.resource=="desert":
                tile.roll_number = 0
                tile.has_robber = True
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



def vague_location(obj):
    """Returns a vague location string for a point, road, or tile given"""
    coast_tiles = [2,3,4,5,8,9,10,11,12,
                   15,16,19,20,21,22,26,27,29,30,33,34,
                   36,37,38,39,40,44,45,46,47]

    if str(type(obj))=="<class 'point.Point'>":
        on_coast = True
        for index in obj.coordinate:
            on_coast = on_coast and index in coast_tiles
        location = "here"
        for index in obj.coordinate:
            location = tile_location(index,location)
            if location[0]=="c":
                break

    elif str(type(obj))=="<class 'road.Road'>":
        on_coast = True
        for coordinate in obj.coordinates:
            for index in coordinate:
                on_coast = on_coast and index in coast_tiles
        location1 = "here"
        location2 = "here"
        for index in obj.coordinates[0]:
            location1 = tile_location(index,location1)
            if location1[0]=="c":
                break
        for index in obj.coordinates[1]:
            location2 = tile_location(index,location2)
            if location2[0]=="c":
                break
        if location1==location2:
            location = location1
        elif location1[2:4]=="st":
            location = location1
        elif location2[2:4]=="st":
            location = location2
        elif location1[-2:]=="st":
            location = location1
        elif location2[-2:]=="st":
            location = location2
        elif location1[0]=="c":
            location = location2
        else:
            location = location1

    elif str(type(obj))=="<class 'tiles.Tile'>":
        on_coast = obj.index in coast_tiles
        location = tile_location(obj.index)

    else:
        return ""

    if on_coast:
        location_string = "on the "
    else:
        location_string = "in the "
    location_string += location
    if on_coast:
        location_string += " coast"

    return location_string

def tile_location(index,location="here"):
    center_tiles = [24]
    north_tiles = [2,3,4,5,8,9,10,11,12,17,18]
    south_tiles = [31,32,36,37,38,39,40,44,45,46,47]
    east_tiles = [12,19,20,25,26,27,33,34,40]
    west_tiles = [8,13,16,21,22,23,29,30,36]
    if index in center_tiles:
        location = "center of the island"
    if index in north_tiles:
        if location[1]=="o":
            pass
        elif location[-2:]=="st":
            location = "north"+location
        else:
            location = "north"
    if index in east_tiles:
        if location[-2:]=="st":
            pass
        elif location[1]=="o":
            location = location+"east"
        else:
            location = "east"
    if index in west_tiles:
        if location[-2:]=="st":
            pass
        elif location[1]=="o":
            location = location+"west"
        else:
            location = "west"
    if index in south_tiles:
        if location[1]=="o":
            pass
        elif location[-2:]=="st":
            location = "south"+location
        else:
            location = "south"

    return location


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
    write_log(player.name,"built a settlement",vague_location(settlement))
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
    player_road_update(road,player)
    # Draw the road on the board
    draw_road(road,player)
    # Write to log where player built road
    write_log(player.name,"built a road",vague_location(road))
    # Recalculate the player's score
    player.calculate_score()

    player.road_length = check_road_length(player.roads)
    for guy in players:
        if guy.has_longest_road:
            break
    if player.road_length>guy.road_length and player.road_length>=5:
        player.has_longest_road = True
        guy.has_longest_road = False
        if player.road_length==5:
            write_log(player.name,"got the longest road bonus")
        elif player.road_length>5:
            write_log(player.name,"took longest road from",guy.name)
    player.calculate_score()
    guy.calculate_score()

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
    write_log(player.name,"built a city",vague_location(city))
    # Recalculate the player's score
    player.calculate_score()

    return city


#adds the point to the list of points that a player _already_ has access to via built roads
def add_point(point,player):
    if (point not in player.points):
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
        if (dice_value == tile.roll_number) and not(tile.has_robber):
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



#updates the player obj with the building info
def player_building_update(point,build_type,player):
    for a_point in all_points:
        if point==a_point:
            point = a_point

    point.building = build_type

    found = False
    for p in player.points:
        if(point == p):
            p.building = build_type
            found = True
            if(build_type == 1):
                player.settlements.append(p)
                if p.is_port:
                    player.ports.append(p.port_resource)
            else:
                player.cities.append(p)
                player.settlements.remove(p)
            break
    if not found:
        player.points.append(point)
        if(build_type == 1):
            player.settlements.append(point)
            if point.is_port:
                player.ports.append(point.port_resource)
        else:
            player.cities.append(point)
            player.settlements.remove(point)


def player_road_update(road,player):
    for a_point in all_points:
        if road.point1==a_point:
            point1 = a_point
        if road.point2==a_point:
            point2 = a_point

    player.points.append(point1)
    player.points.append(point2)
    player.roads.append(Road(point1,point2))

    # Search for point 1 and add it if it isn't found
    found = False
    for p in player.points:
        if(point1 == p):
            found = True
            break
    if not found:
        player.points.append(point1)

    # Search for point 2 and add it if it isn't found
    found = False
    for p in player.points:
        if(point2 == p):
            found = True
            break
    if not found:
        player.points.append(point2)


def occupied_points_on_board(players):
    points = []
    for player in players:
        for settlement in player.settlements:
            points.append(settlement)
        for city in player.cities:
            points.append(city)
    return points



def perform_trade(player,give_resource,get_resource):
    """For player, trades the necessary number of give_resource for
        get_resource"""
    from catan_graphics import write_log

    if "any" in player.ports or "?" in player.ports:
        trade_ratio = 3
    else:
        trade_ratio = 4

    if give_resource in player.ports:
        trade_ratio = 2

    trade_allowed = False
    if give_resource=="wood" and player.wood>=trade_ratio:
        trade_allowed = True
        player.wood -= trade_ratio
    elif give_resource=="brick" and player.brick>=trade_ratio:
        trade_allowed = True
        player.brick -= trade_ratio
    elif give_resource=="sheep" and player.sheep>=trade_ratio:
        trade_allowed = True
        player.sheep -= trade_ratio
    elif give_resource=="wheat" and player.wheat>=trade_ratio:
        trade_allowed = True
        player.wheat -= trade_ratio
    elif give_resource=="stone" and player.stone>=trade_ratio:
        trade_allowed = True
        player.stone -= trade_ratio

    if trade_allowed:
        if get_resource=="wood":
            player.wood += 1
        elif get_resource=="brick":
            player.brick += 1
        elif get_resource=="sheep":
            player.sheep += 1
        elif get_resource=="wheat":
            player.wheat += 1
        elif get_resource=="stone":
            player.stone += 1
        write_log(player.name,"traded",trade_ratio,give_resource,"for 1",
            get_resource)


def move_robber(player,players):
    """Depending on human or computer, should move robber to new space and steal
        random card from player on that space"""
    from catan_graphics import player_place_robber, redraw_robber, get_tiles
    from catan_graphics import player_steal_resource, write_log
    from catan_AI import computer_place_robber, computer_steal_resource
    tiles = get_tiles()
    # Get the tile for the robber to be placed
    if player.AI_code<0:
        robber_tile = player_place_robber(player,tiles)
    else:
        robber_tile = computer_place_robber(player,players,tiles)
    for tile in tiles:
        if tile.has_robber:
            tile.has_robber = False
            break
    for tile in tiles:
        if tile==robber_tile:
            tile.has_robber = True
    # Write to log where player put the robber
    write_log(player.name,"placed the robber",vague_location(robber_tile))
    # Redraw the robber on the board
    redraw_robber(tiles)
    # Take a resource from a player on the tile where the robber was placed
    if player.AI_code<0:
        player_steal_resource(player,players,robber_tile)
    else:
        computer_steal_resource(player,players,robber_tile)


def discard_resources(player,players):
    """Depending on human or computer, should discard resources to get down to
        half the current value (rounded up; e.g. player with 9 cards dicards to
        get down to 5)"""
    from catan_graphics import player_discard
    from catan_AI import computer_discard
    # Find out the number of resources the player needs to get down to
    new_resource_count = int((player.resource_count()+1)/2)
    # Just in case, loop through until the player discards enough resources
    while player.resource_count()>new_resource_count:
        if player.AI_code<0:
            discard_count = player_discard(player,players,new_resource_count)
        else:
            discard_count = computer_discard(player,new_resource_count)

    return discard_count

################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    apoint = Point(2,5,6)
    bpoint = Point(2,5,7)
    aroad = Road(apoint,bpoint)
    print(str(type(apoint)))
    print(str(type(aroad)))
