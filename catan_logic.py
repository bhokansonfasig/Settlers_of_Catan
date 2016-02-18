from random import choice


################################################################################
# Set up logic classes



################################################################################
# Function definitions
def set_players():
    playnum = 0
    compnum = 0

    comp1diff = 0
    comp2diff = 0
    comp3diff = 0
    comp4diff = 0

    while (playnum<=1 or playnum>=5) or (compnum<=-1 or compnum>=5):
        playnum = eval(input("Total number of players: "))
        compnum = eval(input("Number of computer players: "))
        if playnum==compnum:
            comp1diff = eval(input("Computer 1 level: "))
        if playnum<=compnum+1:
            comp2diff = eval(input("Computer 2 level: "))
        if playnum<=compnum+2 and playnum>=3:
            comp3diff = eval(input("Computer 3 level: "))
        if playnum<=compnum+3 and playnum==4:
            comp4diff = eval(input("Computer 4 level: "))



def set_tiles(tiles):
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


################################################################################
# If this file is run itself, do the following
if __name__ == '__main__':
    print(version)
