class Tile:
    def __init__(self, index):
        self.index = index

        self.tk_hex = None
        self.tk_number = None
        self.tk_number_disk = None
        self.tk_dock = None
        self.tk_dock_ratio = None
        self.tk_robber = None
        # self.tk_robber_2 = None
        self.vertices = []  # Coordinates of vertices for GUI

        board_tiles = [9,10,11,
                      16,17,18,19,
                     22,23,24,25,26,
                      30,31,32,33,
                       37,38,39]
        # Determines whether the tile should be drawn
        if self.index in board_tiles:
            self.visible = True
        else:
            self.visible = False

        edge_tiles = [0,1,2,3,4,5,6,
                      13,20,27,34,41,
                      48,47,46,45,44,43,
                      42,35,28,21,14,7]
        # Determines if tile is on edge
        if self.index in edge_tiles:
            self.edge = True
        else:
            self.edge = False

        dock_tiles = [2,4,12,15,27,29,40,44,46]
        # Determines if a dock is to be drawn on the tile
        if self.index in dock_tiles:
            self.dock = True
        else:
            self.dock = False

        self.resource = 'none'  # Tile's associated resource
        self.roll_number = -1  # Tile's associated dice roll number
        self.has_robber = False


    def __eq__(self,other):
        return(self.index == other.index)


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

    def draw_skeleton(self, canvas, style):
        """Draws the outline for the tile on canvas"""
        sand_color = style.get_color("sand")

        self.tk_hex = canvas.create_polygon(self.vertices, outline=sand_color,
            width=4, fill='white', tags="hex")

    def draw(self, canvas, style):
        """Draws the tile with appropriate fill color on canvas"""
        sand_color = style.get_color("sand")
        wood_color = style.get_color("wood")
        brick_color = style.get_color("brick")
        sheep_color = style.get_color("sheep")
        wheat_color = style.get_color("wheat")
        stone_color = style.get_color("stone")
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

    def draw_number(self, canvas, style):
        """Draws the roll number for the tile on canvas with font size
            txt_size"""
        sand_color = style.get_color("sand")
        # Get position of center of tile
        pos_x = (self.vertices[0]+self.vertices[6])/2
        pos_y = (self.vertices[1]+self.vertices[7])/2
        # Draw number disk based on text size
        r = style.txt_size*4/5
        if self.roll_number>0:
            self.tk_number_disk = canvas.create_oval(pos_x-r,pos_y-r,
                pos_x+r,pos_y+r, fill=sand_color, tags="hex")
        # Draw number in black, or red if a 6 or 8
        if (self.roll_number>0 and self.roll_number<6) or (self.roll_number>8):
            self.tk_number = canvas.create_text(pos_x, pos_y,
                text=self.roll_number, font=("Helvetica", style.txt_size),
                tags="hex")
        elif (self.roll_number==6 or self.roll_number==8):
            self.tk_number = canvas.create_text(pos_x, pos_y, fill="#F22222",
                text=self.roll_number, font=("Helvetica", style.txt_size),
                tags="hex")

    def draw_robber(self, canvas):
        """Draws the robber at the center of the tile"""
        # Get position of center of tile
        pos_x = (self.vertices[0]+self.vertices[6])/2
        pos_y = (self.vertices[1]+self.vertices[7])/2
        # Set the radius of the circle based on a third the side length
        r = (self.vertices[3]-self.vertices[1])/3
        # Draw the robber circle
        self.tk_robber = canvas.create_oval(pos_x-r,pos_y-r, pos_x+r,pos_y+r,
            fill="black", tags="robber")
        # Draw a smaller circle with the color given
        # self.tk_robber_2 = canvas.create_oval(int(pos_x-r/2),int(pos_y-r/2),
        #     int(pos_x+r/2),int(pos_y+r/2), fill=extra_color, tags="robber")


    def draw_dock(self, canvas, style, resource, ratio):
        """Draws a dock on the tile for trading resource at ratio"""
        # Get the color for the dock
        dock_color = style.get_color(resource)
        # Get position of center of tile
        pos_x = (self.vertices[0]+self.vertices[6])/2
        pos_y = (self.vertices[1]+self.vertices[7])/2
        # Get half the side length of the dock rectangle
        side = (self.vertices[3]-self.vertices[1])/5
        # Draw the dock rectangle
        self.tk_dock = canvas.create_rectangle(pos_x-2*side,pos_y-side,
            pos_x+2*side,pos_y+side, fill=dock_color, outline=dock_color,
            tags="dock")
        ratio_text = str(ratio)+":1"
        # Draw the ratio
        self.tk_dock_ratio = canvas.create_text(pos_x,pos_y,
            text=ratio_text, font=("Helvetica", int(.8*style.txt_size)),
            tags="dock")

    def has_neighbor(self,neighbor):
        hex1 = self.index
        hex2 = neighbor.index

        if (hex1>hex2):
            # If the hexagons are ordered wrong, just switch them
            hex1,hex2 = hex2,hex1

        if hex1==hex2:
            return False

        if(abs(hex1-hex2)>8): #tiles are too far apart to be neighbors
            # print("Too far apart")
            return False

        elif(abs(hex1-hex2)==1):
            # print("Could be in the same row")
            if(self.edge and neighbor.edge):
                if(hex1%7==6):
                    return False #eg: tile 13 and 14 are not neighbors
                else:
                    return True	#tiles 3 and 4 are both edge tiles but are neighbors
            else:
                return True

        elif((hex1//7)%2 == 0): #odd numbered row
            # print("Odd numbered row")
            if(abs(hex1-hex2)==6 or abs(hex1-hex2)==7):
                return True
            else:
                return False

        elif((hex1//7)%2 == 1): #even numbered row
            # print("Odd numbered row")
            if(abs(hex1-hex2)==7 or abs(hex1-hex2)==8):
                return True
            else:
                return False

        else:
            return False




if __name__ == '__main__':
    i = eval(input("Tile 1: "))
    j = eval(input("Tile 2: "))
    tile_i = Tile(i)
    tile_j = Tile(j)

    if tile_i==tile_j:
        print("These are the same tile.")
    else:
        print("These are not the same tile,",end=' ')
    if tile_i.has_neighbor(tile_j):
       print("but they are neighbors.")
    else:
        print("and they are not neighbors.")
