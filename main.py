# Settlers of Catan
# Created by Ben Hokanson-Fasig and Aman Abhishek
# Last update 02-29-16
version = "0.0.6"


if __name__ == '__main__':
    from catan_graphics import aesthetics, App
    from tkinter import Tk

    aesthetics(900,625)
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
    from os.path import isfile
    from catan_logic import set_tiles, roll_dice, check_winner
    from catan_logic import point_resources, distribute_resources
    from catan_logic import build_settlement, build_road, build_city
    from catan_logic import player_building_update
    from catan_graphics import open_board_window, close_board_window, close_all
    from catan_graphics import set_players, get_tiles, draw_tiles, draw_stats
    from catan_graphics import draw_log, write_log, draw_dice, turn_loop
    from catan_graphics import draw_resource_panel, clear_resource_panel
    from catan_graphics import draw_intermediate_screen, draw_winning_screen

    # Set log file name and delete it if it already exists
    global log_file_name
    log_file_name = "catan_game_log.txt"
    log_file_exists = False
    try:
        log_file_exists = isfile(log_file_name)
    except:
        pass
    if log_file_exists:
        from os import remove
        remove(log_file_name)
        print("Deleted old log file",log_file_name)

    # Start drawing log file to the board window
    draw_log()

    write_log("-----New game started-----")

    global loop_index, die_1, die_2
    loop_index = -1

    # Set the number of players, their names, and levels of AI
    global players
    players = set_players(board)
    # Randomize player order
    shuffle(players)

    # Check to see if all players are computers
    all_computers = True
    for guy in players:
        if guy.AI_code<0:
            all_computers = False

    # Get the arrangement of tiles, then draw them to the board window
    tiles = get_tiles()
    tiles = set_tiles(tiles)
    draw_tiles(tiles)

    # Draw player stats on board window
    playnum = len(players)
    draw_stats(players)

    # Place two settlements per player for the first turn
    for player in players:
        write_log(player.name,"build first settlement")
        build_settlement(player,players)
        write_log(player.name,"build first road")
        build_road(player,players)
        draw_stats(players)
    for player in reversed(players):
        first_round = False
        write_log(player.name,"build second settlement")
        point = build_settlement(player,players)
        write_log(player.name,"build second road")
        build_road(player,players)
        resources = point_resources(point,tiles)
        for resource in resources:
            player.give_resource(resource)
        draw_stats(players)

    # Loop through player turns until someone wins!
    whose_turn = 0
    # Additional condition that players can only win on their turn
    while not(players[whose_turn-1].index in check_winner(players)):
        if loop_index>=0:
            clear_resource_panel()
        draw_stats(players)
        loop_index += 1
        whose_turn = loop_index%playnum + 1
        write_log(players[whose_turn-1].name,"'s turn:", sep='')
        # Wait screen for human players, or if all computer players
        if players[whose_turn-1].AI_code<0 or all_computers:
            draw_intermediate_screen(players[whose_turn-1])

        die_1,die_2 = roll_dice()
        draw_dice(die_1,die_2)
        if die_1+die_2!=7:
            distribute_resources(die_1+die_2,tiles,players)
        else:
            # Robber sequence. Start with the current player, and loop through
            for player in players[whose_turn-1:]:
                if player.robbable():
                    write_log(player.name,"got robbed!")
            for player in players[:whose_turn-1]:
                if player.robbable():
                    write_log(player.name,"got robbed!")

        draw_stats(players)
        draw_resource_panel(players[whose_turn-1],players)

        turn_loop(players[whose_turn-1],players)

    winner = whose_turn
    write_log("*****Congratulations ",players[winner-1].name,"!*****", sep='')

    clear_resource_panel()
    draw_winning_screen(players[winner-1])

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
