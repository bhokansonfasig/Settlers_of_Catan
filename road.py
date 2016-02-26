class Road:
    def __init__(self, point1, point2):
        from point import Point
        self.coordinates = sorted([point1.coordinate,point2.coordinate])
        # print(self.coordinates)
        print("this ran")

        self.point1 = Point(self.coordinates[0][0],self.coordinates[0][1],
                            self.coordinates[0][2])
        self.point2 = Point(self.coordinates[1][0],self.coordinates[1][1],
                            self.coordinates[1][2])

        self.tk_index = None  # Tkinter index of road

        #self.owner = 0  # Owner of road

        # Check whether road is valid on board
        if self.point1.valid and self.point2.valid:
            # If both points are valid, the road is valid, unless the points do
            #  not share exactly two of three coordinate elements
            shared = 0
            for i in self.point1.coordinate:
                if i in self.point2.coordinate:
                    shared += 1

            if shared==2:
                self.valid = True
            else:
                self.valid = False

        else:
            self.valid = False

    def __eq__(self,other):
        # print(self.coordinates,other.coordinates)
        return(self.coordinates == other.coordinates)

if __name__ == '__main__':
    from point import Point
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
        p2 = Point(x2,y2,z2)

        
        r1 = Road(p1,p2)
        print("r1 initialized.\n")

        x2 = int(input("hex1: "))
        y2 = int(input("hex2: "))
        z2 = int(input("hex3: "))

        x1 = int(input("hex1: "))
        y1 = int(input("hex2: "))
        z1 = int(input("hex3: "))
        
        p3 = Point(x1,y1,z1)
        p4 = Point(x2,y2,z2)

        r2 = Road(p3,p4)

        if(r1==r2):
            print("same road")
        else:
            print("distinct roads")