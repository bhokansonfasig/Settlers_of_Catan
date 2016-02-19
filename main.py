# Settlers of Catan
# Created by Ben Hokanson-Fasig, Aman Abhishek, and Alex Scherer?
# Last update 02-18-16
version = "0.0.2"


if __name__ == '__main__':
    from catan_graphics import aesthetics, App
    from tkinter import Tk

    aesthetics()
    root = Tk()
    app = App(root)
    # Draw splash window and run app
    root.geometry("400x300+100+100")
    root.mainloop()

################################################################################
# Function definitions
def new_game(splash,board):
    from catan_logic import randomize, set_tiles, claim_settlement, claim_road
    from catan_logic import give_card, point_resources
    from catan_graphics import open_board_window, close_board_window
    from catan_graphics import set_players, get_tiles, draw_tiles
    from catan_graphics import player_place_settlement, player_place_road
    from catan_graphics import computer_place_settlement, computer_place_road
    from catan_graphics import draw_settlement, draw_road


    print("New game started")

    # Set the number of players, their names, and levels of AI
    players = set_players()
    # Randomize player order
    players = randomize(players)

    # Switch windows
    open_board_window(splash,board)

    # Get the arrangement of tiles, then draw them to the board window
    tiles = get_tiles()
    tiles = set_tiles(tiles)
    draw_tiles(tiles)

    # Place two settlements per player for the first turn
    for player in players:
        if player[2]<0:
            settlement = player_place_settlement(player[0])
            claim_settlement(settlement,player[0])
            draw_settlement(settlement,player[0])
            road = player_place_road(player[0])
            claim_road(road,player[0])
            draw_road(road,player[0])
        else:
            settlement = computer_place_settlement(player[0])
            claim_settlement(settlement,player[0])
            draw_settlement(settlement,player[0])
            road = computer_place_road(player[0])
            claim_road(road,player[0])
            draw_road(road,player[0])
    for player in reversed(players):
        if player[2]<0:
            settlement = player_place_settlement(player[0])
            claim_settlement(settlement,player[0])
            draw_settlement(settlement,player[0])
            road = player_place_road(player[0])
            claim_road(road,player[0])
            draw_road(road,player[0])
        else:
            settlement = computer_place_settlement(player[0])
            claim_settlement(settlement,player[0])
            draw_settlement(settlement,player[0])
            road = computer_place_road(player[0])
            claim_road(road,player[0])
            draw_road(road,player[0])
        resources = point_resources(settlement)
        for resource in resources:
            give_card(resource,player[0])

    # Loop through player turns until someone wins!

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm end: ")

    close_board_window(splash,board)


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
