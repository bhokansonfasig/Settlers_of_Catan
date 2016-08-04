# Settlers of Catan
# Created by Ben Hokanson-Fasig and Aman Abhishek
# Last update 03-16-16
version = "0.1.0"


if __name__ == '__main__':
    from tkinter import Tk
    from graphics_controller import App
    from aesthetics import Style
    from game_pieces import Pieces
    from display_pieces import Displays

    style = Style(900,625)
    pieces = Pieces()
    displays = Displays()
    root = Tk()
    app = App(root,style,pieces,displays)
    # Draw window and run app
    root.mainloop()

################################################################################
# Function definitions
def new_game(app):
    from random import shuffle
    from player import Player
    from tiles import Tile
    from os.path import isfile
    from catan_logic import set_tiles, roll_dice, check_winner
    from catan_logic import point_resources, distribute_resources
    from catan_logic import build_settlement, build_road, build_city
    from catan_logic import move_robber, discard_resources
    from graphics_controller import open_board_window, close_board_window
    from graphics_controller import close_all, redraw_board, set_players
    from draw_elements import draw_tiles, draw_dice
    from draw_menus import draw_stats, draw_log, write_log
    from draw_menus import draw_resource_panel, clear_resource_panel
    from draw_menus import draw_intermediate_screen, draw_winning_screen
    from turn_manager import turn_loop



    # Set log file name and delete it if it already exists
    log_file_exists = False
    try:
        log_file_exists = isfile(app.pieces.log_file_name)
    except:
        pass
    if log_file_exists:
        from os import remove
        remove(app.pieces.log_file_name)
        print("Deleted old log file",app.pieces.log_file_name)

    # Start drawing log file to the board window
    draw_log(app)

    write_log(app,"*****New game started*****")

    # Set the number of players, their names, and levels of AI
    set_players(app)
    # Randomize player order
    shuffle(app.pieces.players)

    # Check to see if all players are computers
    for guy in app.pieces.players:
        if guy.AI_code<0:
            app.pieces.all_computers = False

    # Arange the tiles, then draw them to the board window
    app.pieces.tiles = set_tiles(app.pieces)
    draw_tiles(app)

    # Draw player stats on board window
    playnum = len(app.pieces.players)
    draw_stats(app)

    # Place two settlements per player for the first turn
    for player in app.pieces.players:
        write_log(app,player.name,"build first settlement")
        build_settlement(player,app)
        write_log(app,player.name,"build first road")
        build_road(player,app)
        draw_stats(app)
    for player in reversed(app.pieces.players):
        # first_round = False
        write_log(app,player.name,"build second settlement")
        point = build_settlement(player,app)
        write_log(app,player.name,"build second road")
        build_road(player,app)
        resources = point_resources(point,app.pieces.tiles)
        for resource in resources:
            player.give_resource(resource)
        draw_stats(app)

    # Loop through player turns until someone wins!
    # Additional condition that players can only win on their turn
    while not(app.pieces.players[app.pieces.turn_index].index \
            in check_winner(app.pieces.players)):
        if app.pieces.loop_index>=0:
            clear_resource_panel(app)
        draw_stats(app)
        app.pieces.loop_index += 1
        app.pieces.turn_index = app.pieces.loop_index%playnum
        write_log(app,"---",app.pieces.players[app.pieces.turn_index].name,
            "'s turn---", sep='')
        # Wait screen for human players, or if all computer players
        if app.pieces.players[app.pieces.turn_index].AI_code<0 or \
                app.pieces.all_computers:
            draw_intermediate_screen(app.pieces.players[app.pieces.turn_index],
                app)

        app.pieces.die = roll_dice(app)
        draw_dice(app)
        if sum(app.pieces.die)!=7:
            distribute_resources(sum(app.pieces.die),
                app.pieces.tiles,app.pieces.players)
        else:
            # Robber sequence. Start with the next player, and loop through
            for player in app.pieces.players[app.pieces.turn_index+1:]:
                if player.robbable():
                    if player.AI_code<0:
                        clear_resource_panel(app)
                        draw_intermediate_screen(player,app,"discard")
                    discard_count = discard_resources(player,app)
                    write_log(app,player.name,"was robbed of",discard_count,
                        "resources.")
            for player in app.pieces.players[:app.pieces.turn_index+1]:
                if player.robbable():
                    if player.AI_code<0:
                        clear_resource_panel(app)
                        draw_intermediate_screen(player,app,"discard")
                    discard_count = discard_resources(player,app)
                    write_log(app,player.name,"was robbed of",discard_count,
                        "resources.")
            clear_resource_panel(app)
            draw_stats(app)
            move_robber(app.pieces.players[app.pieces.turn_index],app)

        draw_stats(app)
        draw_resource_panel(app.pieces.players[app.pieces.turn_index],app)

        turn_loop(app.pieces.players[app.pieces.turn_index],app)

    winner = app.pieces.turn_index
    write_log(app,"*****Congratulations ",app.pieces.players[winner].name,
        "!*****", sep='')

    clear_resource_panel(app)
    draw_stats(app)
    draw_winning_screen(app.pieces.players[winner],app)

    close_all(app)

# def save_game():
#     import pickle
#     data = [players,tiles]
#     with open(game.soc,'wb') as f:
#           pickle.dump(data,game.soc)
#     f.close()

# def remote_game(splash,board):
#     from random import shuffle
#     from player import Player
#     from tiles import Tile
#     from os.path import isfile
#     from catan_logic import set_tiles, roll_dice, check_winner
#     from catan_logic import point_resources, distribute_resources
#     from catan_logic import build_settlement, build_road, build_city
#     from catan_logic import move_robber, discard_resources
#     from catan_graphics import open_board_window, close_board_window, close_all
#     from catan_graphics import set_players, get_tiles, draw_tiles, draw_stats
#     from catan_graphics import draw_log, write_log, draw_dice, turn_loop
#     from catan_graphics import draw_resource_panel, clear_resource_panel
#     from catan_graphics import draw_intermediate_screen, draw_winning_screen
#     from catan_graphics import redraw_board

#     # Set log file name and delete it if it already exists
#     global log_file_name
#     log_file_name = "catan_game_log.txt"
#     log_file_exists = False
#     try:
#         log_file_exists = isfile(log_file_name)
#     except:
#         pass
#     if log_file_exists:
#         from os import remove
#         remove(log_file_name)
#         print("Deleted old log file",log_file_name)

#     # Start drawing log file to the board window
#     draw_log()

#     write_log(app,"*****New game started*****")

#     global loop_index, die_1, die_2
#     loop_index = -1

#     # Set the number of players, their names, and levels of AI
#     global players
#     players = set_players(board)
#     # Randomize player order
#     shuffle(players)

#     # Check to see if all players are computers
#     global all_computers
#     all_computers = True
#     for guy in players:
#         if guy.AI_code<0:
#             all_computers = False

#     # Get the arrangement of tiles, then draw them to the board window
#     tiles = get_tiles()
#     tiles = set_tiles(tiles)
#     draw_tiles(tiles)

#     # Draw player stats on board window
#     playnum = len(players)
#     draw_stats(players)



def load_game(app):
    from catan_graphics import open_board_window, close_board_window

    print("Old game loaded")

    # Switch windows
    open_board_window(splash,board)

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm end: ")

    close_board_window(splash,board)
