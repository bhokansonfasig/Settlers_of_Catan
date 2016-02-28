# Settlers of Catan
# Created by Ben Hokanson-Fasig, Aman Abhishek, and Alex Scherer?
# Last update 02-24-16
version = "0.0.3"


if __name__ == '__main__':
    from catan_graphics import aesthetics, App
    from tkinter import Tk

    aesthetics(900,600)
    root = Tk()
    app = App(root)
    # Draw window and run app
    root.mainloop()

################################################################################
# Function definitions
def new_game(splash,board):
    from random import shuffle
    from player import Player
    from tiles import Tile
    from catan_logic import set_tiles, roll_dice, check_winner
    from catan_logic import point_resources, distribute_resources
    from catan_logic import build_settlement, build_road, build_city
    from catan_logic import player_building_update
    from catan_graphics import open_board_window, close_board_window, close_all
    from catan_graphics import set_players, get_tiles, draw_tiles, draw_stats
    from catan_graphics import draw_road, draw_dice
    from catan_graphics import draw_resource_panel, clear_resource_panel
    from catan_graphics import draw_intermediate_screen

    print("New game started")

    # Set the number of players, their names, and levels of AI
    global players
    players = set_players()
    # Randomize player order
    shuffle(players)

    # Switch windows
    open_board_window(splash,board)

    # Get the arrangement of tiles, then draw them to the board window
    tiles = get_tiles()
    tiles = set_tiles(tiles)
    draw_tiles(tiles)

    # Draw player stats on board window
    playnum = len(players)
    draw_stats(players)

    # Place two settlements per player for the first turn
    for player in players:
        print(player.name,"build first settlement")
        build_settlement(player,players)
        print(player.name,"build first road")
        build_road(player,players)
        draw_stats(players)
    for player in reversed(players):
        first_round = False
        print(player.name,"build second settlement")
        point = build_settlement(player,players)
        print(player.name,"build second road")
        build_road(player,players)
        resources = point_resources(point,tiles)
        for resource in resources:
            player.give_resource(resource)
        draw_stats(players)

    # Loop through player turns until someone wins!
    loop_index = 0
    whose_turn = 1
    # Additional condition that players can only win on their turn
    while check_winner()!=whose_turn:
        whose_turn = loop_index%playnum + 1
        print(players[whose_turn-1].name,"'s turn", sep='')
        draw_intermediate_screen(players[whose_turn-1].name)


        die_1,die_2 = roll_dice()
        draw_dice(die_1,die_2)
        if die_1+die_2!=7:
            distribute_resources(die_1+die_2)
        else:
            # Robber sequence
            pass
        draw_stats(players)

        draw_resource_panel(players[whose_turn-1],players)

        # Button events should be able to handle what the player really does
        #  during their turn

        clear_resource_panel()
        draw_stats(players)

        loop_index += 1

    winner = check_winner()
    print("*****Congratulations ",players[winner-1].name,"!*****", sep='')

    close_all(splash,board)


def load_game(splash,board):
    from catan_graphics import open_board_window, close_board_window

    print("Old game loaded")

    # Switch windows
    open_board_window(splash,board)

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm end: ")

    close_board_window(splash,board)
