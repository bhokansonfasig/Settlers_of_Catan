class Tile:
    def __init__(self, index):
        self.index = index

        self.tk_hex = None
        self.tk_number = None
        self.vertices = []  # Coordinates of vertices for GUI
        self.visible = False  # Determines whether the tile should be drawn
        if self.index in \
            [9,10,11,16,17,18,19,22,23,24,25,26,30,31,32,33,37,38,39]:
            self.visible = True

        self.resource = 'none'  # Tile's associated resource
        self.roll_number = -1  # Tile's associated dice roll number

        #self.settlements = []  # Players with settlements on the tile
        #self.roads = []  # Players with roads on the tile

    def set_vertices(self, hex_width, hex_height, hex_x_off, hex_y_off):
        """Sets the vertices of the GUI polygon"""
        x_i = 2*(self.index%7)
        y_i = 3*int(self.index/7)
        # Even rows
        if self.index%7==self.index%14:
            self.vertices = [
                int(hex_width*(x_i-3)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off,
                int(hex_width*(x_i-3)/10)+hex_x_off,
                int(hex_height*(y_i)/16)+hex_y_off,
                int(hex_width*(x_i-2)/10)+hex_x_off,
                int(hex_height*(y_i+1)/16)+hex_y_off,
                int(hex_width*(x_i-1)/10)+hex_x_off,
                int(hex_height*(y_i)/16)+hex_y_off,
                int(hex_width*(x_i-1)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off,
                int(hex_width*(x_i-2)/10)+hex_x_off,
                int(hex_height*(y_i-3)/16)+hex_y_off,
                int(hex_width*(x_i-3)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off]
        # Odd rows
        if self.index%7!=self.index%14:
            self.vertices = [
                int(hex_width*(x_i-2)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off,
                int(hex_width*(x_i-2)/10)+hex_x_off,
                int(hex_height*(y_i)/16)+hex_y_off,
                int(hex_width*(x_i-1)/10)+hex_x_off,
                int(hex_height*(y_i+1)/16)+hex_y_off,
                int(hex_width*(x_i)/10)+hex_x_off,
                int(hex_height*(y_i)/16)+hex_y_off,
                int(hex_width*(x_i)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off,
                int(hex_width*(x_i-1)/10)+hex_x_off,
                int(hex_height*(y_i-3)/16)+hex_y_off,
                int(hex_width*(x_i-2)/10)+hex_x_off,
                int(hex_height*(y_i-2)/16)+hex_y_off]

    def draw_skeleton(self, canvas):
        """Draws the outline for the tile on canvas"""
        from catan_graphics import set_colors
        menu_color,button_color,sand_color,wood_color,brick_color,sheep_color, \
            wheat_color,stone_color = set_colors()

        self.tk_hex = canvas.create_polygon(self.vertices, outline=sand_color,
            width=4, fill='white', tags="hex")

    def draw(self, canvas):
        """Draws the tile with appropriate fill color on canvas"""
        from catan_graphics import set_colors
        menu_color,button_color,sand_color,wood_color,brick_color,sheep_color, \
            wheat_color,stone_color = set_colors()
        if self.resource=="wood":
            canvas.itemconfig(self.tk_hex,fill=wood_color)
        elif self.resource=="brick":
            canvas.itemconfig(self.tk_hex,fill=brick_color)
        elif self.resource=="sheep":
            canvas.itemconfig(self.tk_hex,fill=sheep_color)
        elif self.resource=="wheat":
            canvas.itemconfig(self.tk_hex,fill=wheat_color)
        elif self.resource=="stone":
            canvas.itemconfig(self.tk_hex,fill=stone_color)
        else:
            canvas.itemconfig(self.tk_hex,fill=sand_color)

    def draw_number(self, canvas, txt_size):
        """Draws the roll number for the tile on canvas with font size
            txt_size"""
        # Get position of center of tile
        pos_x = (self.vertices[0]+self.vertices[6])/2
        pos_y = (self.vertices[1]+self.vertices[7])/2
        # Draw number in black, or red if a 6 or 8
        if (self.roll_number>0 and self.roll_number<6) or (self.roll_number>8):
            self.tk_number = canvas.create_text(pos_x, pos_y,
                text=self.roll_number, font=("Helvetica", txt_size))
        elif (self.roll_number==6 or self.roll_number==8):
            self.tk_number = canvas.create_text(pos_x, pos_y, fill='red',
                text=self.roll_number, font=("Helvetica", txt_size))
