class Style():
    def __init__(self,width,height):
        self.adjust_size(width,height)
        self.menu_color = "#EECC8C"
        self.background_color = "#F7D9B2"
        self.active_button_color = "#FFFFCC"
        self.inactive_button_color = "#F7D9B2"
        self.water_color = "#6680FF"
        self.sand_color = "#D7B992"
        self.dock_color = "#996633"
        self.wood_color = "#2C8236"
        self.brick_color = "#8B0000"
        self.sheep_color = "#A6FFA6"
        self.wheat_color = "#F5B800"
        self.stone_color = "#686868"

    def adjust_size(self,width,height):
        self.win_width = width
        self.win_height = height

        self.txt_font = "Helvetica"

        if height<167:
            self.txt_size = 5
        elif height>1200:
            self.txt_size = 36
        else:
            self.txt_size = int(.03*height)

        # Raise errors for strange dimensions
        if 625*width>1.1*900*height or 625*width<.9*900*height:
            print("Board dimensions are incorrect, some elements may appear",
                "distorted.")
        if width<500 or height<500:
            print("Board window too small, some features may not appear properly.")

        # Geometry for board window
        self.board_geometry = str(int(width))+"x"+str(int(height))
        # self.board_geometry = "%dx%d" % (win_width,win_height)

        # Set width and height of hexagon section
        # global hex_height, hex_width
        if width>=height:
            self.hex_height = height*.7
            self.hex_width = self.hex_height
        else:
            self.hex_width = width*.7
            self.hex_height = self.hex_width

        # Set width of water region
        # global water_width
        self.water_width = int(self.hex_width/10)

        # Set offsets from top right corner for hexagon section (without water)
        # global hex_x_off, hex_y_off
        self.hex_x_off = int(width-self.hex_width-1.75*self.water_width)
        self.hex_y_off = int(height-self.hex_height-self.water_width)

    def get_color(self,element):
        """Returns color of requested element"""
        if element.lower()=="menu":
            return self.menu_color
        if element.lower()=="background":
            return self.background_color
        if element.lower()=="active button":
            return self.active_button_color
        if element.lower()=="inactive button":
            return self.inactive_button_color
        if element.lower()=="water":
            return self.water_color
        if element.lower()=="sand":
            return self.sand_color
        if element.lower()=="dock" or element.lower()=="any" or \
            element.lower()=="?":
            return self.dock_color
        if element.lower()=="wood":
            return self.wood_color
        if element.lower()=="brick":
            return self.brick_color
        if element.lower()=="sheep":
            return self.sheep_color
        if element.lower()=="wheat":
            return self.wheat_color
        if element.lower()=="stone":
            return self.stone_color
