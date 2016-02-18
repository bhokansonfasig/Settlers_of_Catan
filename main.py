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
    from catan_logic import set_tiles
    from catan_graphics import set_players, get_tiles, draw_tiles
    from catan_graphics import open_board_window, close_board_window


    print("New game started")

    # Set the number of players, their names, and levels of AI
    players = set_players()

    # Switch windows
    open_board_window(splash,board)

    # Get the arrangement of tiles, then draw them to the board window
    tiles = get_tiles()
    tiles = set_tiles(tiles)
    draw_tiles(tiles)

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")

    close_board_window(splash,board)


def load_game(splash,board):
    from catan_graphics import open_board_window, close_board_window

    print("Old game loaded")

    # Switch windows
    open_board_window(splash,board)

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")

    close_board_window(splash,board)
