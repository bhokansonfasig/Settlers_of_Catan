class Point:
    def __init__(self, hex1, hex2, hex3):
        self.coordinate = sorted([hex1,hex2,hex3])
        self.x = self.coordinate[0]
        self.y = self.coordinate[1]
        self.z = self.coordinate[2]

        #self.settlement_owner = 0  # Owner of settlement on point
        #self.city_owner = 0  # Owner of city on point

        # Check whether point is valid on board
        from construction import neighbor_tile
        hidden_tiles = [0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,
            28,21,14,7,8,12,13,29,36,40]

        if (neighbor_tile(self.x,self.y) and neighbor_tile(self.y,self.z) and
            neighbor_tile(self.x,self.z)):
            if ((self.x in hidden_tiles) and (self.y in hidden_tiles) and
                (self.z in hidden_tiles)):
                #like 40,47,48
                #print("Point lies in the sea!")
                self.valid = False
            else:
                self.valid = True
        else:
    		#print("Invalid point.")
            self.valid = False

    def link_vertex(self, hex_width, hex_height, hex_x_off, hex_y_off):
        # Vertex at top of lone-row hexagon (e.g. point 9,10,17)
        if self.y-self.x==1:
            x_i = 2*(self.z%7)
            y_i = 3*int(self.z/7)
            if self.z%7==self.z%14:
                self.vertex = [int(hex_width*(x_i-2)/10)+hex_x_off,
                    int(hex_height*(y_i-3)/16)+hex_y_off]
            else:
                self.vertex = [int(hex_width*(x_i-1)/10)+hex_x_off,
                    int(hex_height*(y_i-3)/16)+hex_y_off]
        # Vertex at bottom of lone hexagon (e.g. point 2,8,9)
        elif self.z-self.y==1:
            x_i = 2*(self.x%7)
            y_i = 3*int(self.x/7)
            if self.x%7!=self.x%14:
                self.vertex = [int(hex_width*(x_i-1)/10)+hex_x_off,
                    int(hex_height*(y_i+1)/16)+hex_y_off]
            else:
                self.vertex = [int(hex_width*(x_i-2)/10)+hex_x_off,
                    int(hex_height*(y_i+1)/16)+hex_y_off]
