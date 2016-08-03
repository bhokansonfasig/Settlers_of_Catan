class Road:
    def __init__(self, point1, point2):
        self.coordinates = sorted([point1.coordinate,point2.coordinate])

        if point1.coordinate==self.coordinates[0]:
            self.point1 = point1
            self.point2 = point2
        else:
            self.point1 = point2
            self.point2 = point1

        self.tiles = list(set(point1.coordinate).intersection(point2.coordinate))

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

    def return_connected_road(self,road_list):
        for road in road_list:
            if(self.connected(road)):
                return road

    def common_tile(self,other):
        return(list(set(self.tiles).intersection(other.tiles)))



def check_road_length(roads):
    max_length = 0
    for road in roads:
        removable_roads = roads[:]
        length1 = recursive_road_count(removable_roads,road,road.point1)
        removable_roads = roads[:]
        length2 = recursive_road_count(removable_roads,road,road.point2)
        if length1>max_length:
            max_length = length1
        elif length2>max_length:
            max_length = length2

    return max_length

def recursive_road_count(roads,starting_road,starting_point):
    roads.remove(starting_road)
    connections = []
    for road in roads:
        if starting_point.coordinate==road.point1.coordinate:
            connections.append([road,road.point2])
        elif starting_point.coordinate==road.point2.coordinate:
            connections.append([road,road.point1])

    if len(connections)==0:
        return 1
    if len(connections)==1:
        return 1+recursive_road_count(roads[:],connections[0][0],connections[0][1])
    if len(connections)==2:
        branch1 = connections[0]
        branch1_roads = roads[:]
        branch2 = connections[1]
        branch2_roads = roads[:]
        branch1_count = recursive_road_count(branch1_roads,branch1[0],branch1[1])
        branch2_count = recursive_road_count(branch2_roads,branch2[0],branch2[1])
        if branch1_count>branch2_count:
            return 1+branch1_count
        else:
            return 1+branch2_count
