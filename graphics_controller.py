from tkinter import *
from main import version, new_game, load_game
from aesthetics import Style
from display_pieces import Displays

from tiles import Tile
from player import Player
from point import Point
from catan_AI import set_computer
from draw_elements import draw_tile_skeleton, redraw_board


# App screen class
class App(Frame):

    def __init__(self,parent,style,pieces):
        Frame.__init__(self,parent)
        # self.parent = parent
        self.board = parent
        self.style = style
        self.pieces = pieces
        self.displays = Displays()
        self.initUI()

    def set_button_chosen(self,integer):
        """Sets the button_chosen variable to value 'integer'"""
        self.button_chosen.set(integer)

    def initUI(self):
        self.board.title("Settlers of Catan - Play")
        self.board.geometry(self.style.board_geometry)

        # Create splash window
        # global splash
        self.splash = Toplevel(background=self.style.menu_color)
        #splash.geometry("400x300+100+100")
        self.splash.title("Settlers of Catan - Welcome")
        # global splash_canvas
        # splash_canvas = Canvas(self.splash, background=menu_color)
        # Welcome text
        game_label = Label(self.splash, text="Settlers of Catan",
            font=(self.style.txt_font,36), background=self.style.menu_color)
        game_label.pack()
        version_label = Label(self.splash, text="Version "+version,
            font=(self.style.txt_font,18), background=self.style.menu_color)
        version_label.pack(pady=30)
        # Buttons
        play_button = Button(self.splash, font=(self.style.txt_font,16),
            text="Local Game",
            command=lambda : new_game(self))
        play_button.configure(width=20,
            activebackground=self.style.active_button_color)
        play_button.pack(pady=10)
        start_button = Button(self.splash, font=(self.style.txt_font,16),
            text="New Remote Game",
            command=lambda : remote_game(self))
        start_button.configure(width=20,
            activebackground=self.style.active_button_color)
        start_button.pack(pady=10)
        load_button = Button(self.splash, font=(self.style.txt_font,16),
            text="Load Remote Game",
            command=lambda : load_game(self))
        load_button.configure(width=20,
            activebackground=self.style.active_button_color)
        load_button.pack(pady=10)
        quit_button = Button(self.splash, font=(self.style.txt_font,16),
            text="Quit", command=self.quit)
        quit_button.configure(width=10,
            activebackground=self.style.active_button_color)
        quit_button.pack(pady=10)

        # Create player selection window
        # global player_window
        self.player_window = Toplevel(background=self.style.menu_color)
        #self.player_window.geometry("470x350+300+100")
        self.player_window.title("Settlers of Catan - Select Players")

        # global player_1_type,player_1_name, player_2_type,player_2_name
        # global player_3_type,player_3_name, player_4_type,player_4_name
        player_type_options = ["Human","Computer","None"]
        player_1_label = Label(self.player_window, text="Player 1:",
            font=(self.style.txt_font,22), background=self.style.menu_color)
        player_1_label.grid(row=0,column=0,padx=20,pady=10)
        self.player_1_type = StringVar()
        self.player_1_type.set(player_type_options[1])
        player_1_type_menu = OptionMenu(self.player_window, self.player_1_type,
            *player_type_options)
        player_1_type_menu.grid(row=1,column=0,padx=20,pady=10)
        self.player_1_name = StringVar()
        self.player_1_name.set("Player 1")
        player_1_name_entry = Entry(self.player_window,
            textvariable=self.player_1_name)
        player_1_name_entry.grid(row=2,column=0,padx=20,pady=5)
        player_2_label = Label(self.player_window, text="Player 2:",
            font=(self.style.txt_font,22), background=self.style.menu_color)
        player_2_label.grid(row=0,column=1,padx=20,pady=10)
        self.player_2_type = StringVar()
        self.player_2_type.set(player_type_options[1])
        player_2_type_menu = OptionMenu(self.player_window, self.player_2_type,
            *player_type_options)
        player_2_type_menu.grid(row=1,column=1,padx=20,pady=10)
        self.player_2_name = StringVar()
        self.player_2_name.set("Player 2")
        player_2_name_entry = Entry(self.player_window,
            textvariable=self.player_2_name)
        player_2_name_entry.grid(row=2,column=1,padx=20,pady=5)
        player_3_label = Label(self.player_window, text="Player 3:",
            font=(self.style.txt_font,22), background=self.style.menu_color)
        player_3_label.grid(row=3,column=0,padx=20,pady=10)
        self.player_3_type = StringVar()
        self.player_3_type.set(player_type_options[1])
        player_3_type_menu = OptionMenu(self.player_window, self.player_3_type,
            *player_type_options)
        player_3_type_menu.grid(row=4,column=0,padx=20,pady=10)
        self.player_3_name = StringVar()
        self.player_3_name.set("Player 3")
        player_3_name_entry = Entry(self.player_window,
            textvariable=self.player_3_name)
        player_3_name_entry.grid(row=5,column=0,padx=20,pady=5)
        player_4_label = Label(self.player_window, text="Player 4:",
            font=(self.style.txt_font,22), background=self.style.menu_color)
        player_4_label.grid(row=3,column=1,padx=20,pady=10)
        self.player_4_type = StringVar()
        self.player_4_type.set(player_type_options[1])
        player_4_type_menu = OptionMenu(self.player_window, self.player_4_type,
            *player_type_options)
        player_4_type_menu.grid(row=4,column=1,padx=20,pady=10)
        self.player_4_name = StringVar()
        self.player_4_name.set("Player 4")
        player_4_name_entry = Entry(self.player_window,
            textvariable=self.player_4_name)
        player_4_name_entry.grid(row=5,column=1,padx=20,pady=5)

        # global button_chosen
        self.button_chosen = IntVar()
        self.button_chosen.set(-1)

        ready_button = Button(self.player_window, font=(self.style.txt_font,16),
            text="Okay", command=lambda : self.set_button_chosen(1))
        ready_button.configure(width=10,
            activebackground=self.style.active_button_color)
        ready_button.grid(row=6,pady=30,columnspan=2)

        # Hide player selection window
        self.player_window.withdraw()

        # Create board window's canvas and items
        # global board_canvas
        self.board_canvas = Canvas(self.board,
            background=self.style.background_color)
        self.board_canvas.pack(fill=BOTH, expand=1)

        # Generate 49 tiles
        # global tiles
        self.pieces.tiles = []
        for i in range(49):
            self.pieces.tiles.append(Tile(i))

        draw_tile_skeleton(self)

        # global click_x,click_y
        self.click_x = IntVar()  # Tkinter variable that can be watched
        self.click_y = IntVar()  # Tkinter variable that can be watched
        self.click_x.set(0)
        self.click_y.set(0)

        # Define board bindings & protocols
        def click_set(event):
            """On click event, sets the x and y coordinates of the click"""
            self.click_x.set(event.x)
            self.click_y.set(event.y)
            #print(click_x.get(),click_y.get())

        def reset_size(event):
            """Resizes board elements when the window size is changed."""
            win_width = event.width
            win_height = event.height
            self.style = Style(win_width,win_height)
            redraw_board(self)

        def user_closed():
            """Closes board window nicely if user manually closes it."""
            # Later may use this to create saves
            # Get out of any waiting that was happening
            self.set_button_chosen(-1)
            click_set(Point(0,0,0))  # Just needs to have .x and .y attributes
            # Clear board
            self.board_canvas.delete(ALL)
            # Close all windows
            close_all(self)

        # Set board bindings & protocols
        self.board_canvas.bind("<Button-1>", click_set)
        self.board_canvas.bind("<Configure>", reset_size)
        self.board.protocol("WM_DELETE_WINDOW", user_closed)

        # Prevent manual closing of player window
        self.player_window.protocol("WM_DELETE_WINDOW", user_closed)

        # Hide board window
        self.board.withdraw()



# Board window control

def open_board_window(app):
    """Hides splash window and reveals board window"""
    app.splash.withdraw()
    app.board.update()
    app.board.deiconify()


def close_board_window(app):
    """Hides board window and reveals splash window"""
    app.board.withdraw()
    app.splash.update()
    app.splash.deiconify()


def close_all(app):
    """Closes all windows to quit app"""
    print("Closing all windows...")
    try:
        undraw_log(app)
    except:
        print("  Error in undrawing log")
    try:
        app.splash.destroy()
        app.player_window.destroy()
        app.board.destroy()
    except:
        print("  Error in closing windows")



# Player setup window control

def set_players(app):
    """Gets the number and type of players and returns an array of player
        objects"""
    app.pieces.turn_phase = "player selection"
    
    app.splash.withdraw()
    app.player_window.update()
    app.player_window.deiconify()

    while len(app.pieces.players)<2:
        app.pieces.players = []

        app.player_window.wait_variable(app.button_chosen)

        if app.player_1_type.get()=="Human":
            app.pieces.players.append(Player(1,app.player_1_name.get(),-1))
        elif app.player_1_type.get()=="Computer":
            comp_name = app.player_1_name.get()
            if comp_name=="Player 1":
                comp_name = "Computer 1"
            comp_name,comp_level = set_computer(comp_name)
            app.pieces.players.append(Player(1,comp_name,comp_level))
        if app.player_2_type.get()=="Human":
            app.pieces.players.append(Player(2,app.player_2_name.get(),-1))
        elif app.player_2_type.get()=="Computer":
            comp_name = app.player_2_name.get()
            if comp_name=="Player 2":
                comp_name = "Computer 2"
            comp_name,comp_level = set_computer(comp_name)
            app.pieces.players.append(Player(2,comp_name,comp_level))
        if app.player_3_type.get()=="Human":
            app.pieces.players.append(Player(3,app.player_3_name.get(),-1))
        elif app.player_3_type.get()=="Computer":
            comp_name = app.player_3_name.get()
            if comp_name=="Player 3":
                comp_name = "Computer 3"
            comp_name,comp_level = set_computer(comp_name)
            app.pieces.players.append(Player(3,comp_name,comp_level))
        if app.player_4_type.get()=="Human":
            app.pieces.players.append(Player(4,app.player_4_name.get(),-1))
        elif app.player_4_type.get()=="Computer":
            comp_name = app.player_4_name.get()
            if comp_name=="Player 4":
                comp_name = "Computer 4"
            comp_name,comp_level = set_computer(comp_name)
            app.pieces.players.append(Player(4,comp_name,comp_level))

    open_board_window(app)
