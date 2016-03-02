class Road:
    def __init__(self, point1, point2):
        from point import Point
        self.coordinates = sorted([point1.coordinate,point2.coordinate])

        self.point1 = Point(self.coordinates[0][0],self.coordinates[0][1],
                            self.coordinates[0][2])
        self.point2 = Point(self.coordinates[1][0],self.coordinates[1][1],
                            self.coordinates[1][2])

        self.tk_index = None  # Tkinter index of road

        self.connections = 0 #for calculating longest road


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

    #returns false if the two roads are the same
    def connected(self,other):
        if(self == other):
            return False
        if((self.point1.coordinate in other.coordinates) or (self.point2.coordinate in other.coordinates)):
            return True
        else:
            return False

    def find_connected(self,road_list):
        connections = []
        for road in road_list:
            if(self.connected(road)):
                connections.append(road)

        return connections




            

