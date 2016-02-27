class Tile:
    def __init__(self, index):
        self.index = index

        self.tk_hex = None
        self.tk_number = None
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

        self.resource = 'none'  # Tile's associated resource
        self.roll_number = -1  # Tile's associated dice roll number


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

    def draw_skeleton(self, canvas):
        """Draws the outline for the tile on canvas"""
        from catan_graphics import set_color
        sand_color = set_color("sand")

        self.tk_hex = canvas.create_polygon(self.vertices, outline=sand_color,
            width=4, fill='white', tags="hex")

    def draw(self, canvas):
        """Draws the tile with appropriate fill color on canvas"""
        from catan_graphics import set_color
        sand_color = set_color("sand")
        wood_color = set_color("wood")
        brick_color = set_color("brick")
        sheep_color = set_color("sheep")
        wheat_color = set_color("wheat")
        stone_color = set_color("stone")
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
