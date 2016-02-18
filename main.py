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
    from catan_graphics import get_tiles, draw_tiles
    from catan_logic import set_tiles
    # Switch windows
    print("New game started")
    splash.withdraw()
    board.update()
    board.deiconify()

    # Get the arrangement of tiles, then draw them to the board window
    tiles = get_tiles()
    tiles = set_tiles(tiles)
    draw_tiles(tiles)

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")

    close_game(splash,board)


def load_game(splash,board):
    # Switch windows
    print("Old game loaded")
    splash.withdraw()
    board.update()
    board.deiconify()

    # Temporary pause
    string = ""
    while string=="":
        string = input("Type anything to confirm exit: ")

    close_game(splash,board)


def close_game(splash,board):
    # Resets window
    board.withdraw()
    splash.update()
    splash.deiconify()
