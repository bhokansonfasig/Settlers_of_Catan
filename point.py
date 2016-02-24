class Point:
    def __init__(self, hex1, hex2, hex3):
        self.coordinate = sorted([hex1,hex2,hex3])
        self.x = self.coordinate[0]
        self.y = self.coordinate[1]
        self.z = self.coordinate[2]

        self.settlement_owner = 0  # Owner of settlement on point
        self.city_owner = 0  # Owner of city on point

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
