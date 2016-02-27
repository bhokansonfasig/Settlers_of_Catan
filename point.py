from tiles import Tile

class Point:
    def __init__(self, hex1, hex2, hex3):
        self.coordinate = sorted([hex1,hex2,hex3])
        self.x = self.coordinate[0]
        self.y = self.coordinate[1]
        self.z = self.coordinate[2]

        self.vertex = False

        self.tk_index = None  # Tkinter index of settlement or city

        #self.settlement_owner = 0  # Owner of settlement on point
        #self.city_owner = 0  # Owner of city on point

        # Check whether point is valid on board
        tile_1 = Tile(self.x)
        tile_2 = Tile(self.y)
        tile_3 = Tile(self.z)
        if tile_1.has_neighbor(tile_2) and tile_2.has_neighbor(tile_3) and \
            tile_3.has_neighbor(tile_1):
            if not(tile_1.visible) and not(tile_2.visible) and \
                not(tile_3.visible):
                self.valid = False
            else:
                self.valid = True
        else:
            self.valid = False


    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y and self.z == other.z)

    #checks if two points are adjacent
    def adjacent_point(self,other):
        if(not(self.valid and other.valid)):
            print ("non valid points were given to check for adjacency!")
            return False
        common = list(set(self.coordinate).intersection(other.coordinate))
        if(len(common) == 2):
            return True
        else:
            return False

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


if __name__ == '__main__':
    x = 17
    y = 23
    z = 24
    while(True):
        x2 = int(input("hex1: "))
        y2 = int(input("hex2: "))
        z2 = int(input("hex3: "))

        x1 = int(input("hex1: "))
        y1 = int(input("hex2: "))
        z1 = int(input("hex3: "))

        p1 = Point(x1,y1,z1)
        # p2 = Point(x2,y2,z2)

        print(p1.adjacent_point(Point(x2,y2,z2)))

        # if(adjacent_points(p1,p2)):
        #     print("adjacent")
        # else:
        #     print("non adjacent")
        # z = int(input("hex3: "))
        # if(neighbor_tile(x,y)):
        #   print("They are neighbors.\n")
        # else:
        #   print("Not neighbors.\n")
