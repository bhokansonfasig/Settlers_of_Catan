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


#allots a number to each road which corresponds to how many other roads its connected to
def classify_road(player):
    # from player import Player
    # output = [] 
    player.road_types = [[],[],[],[],[]]
    for road in player.roads:
        connections = 0
        for other_road in player.roads:
            # if(road == other_road):
            #     continue
            # else:
            if(road.connected(other_road)):
                connections += 1
        player.road_types[connections].append(road)

    s = ''
    for t in range(0,5):
        s += str(len(player.road_types[t])) + " "
    # return output
    print(s,player.name)

# #isolates disconnected single piece roads and simple straight roads
# def isolate_simple_structures(player,road_types):
#     edges = []
#     for t in road_types:
#         if(t == 0): #lone roads, nothing to be done
#             road_types[t] = -1 
#         elif(t == 1):
#             edges.append(player.roads[t])
#             # road_types[t] = -1
#         else:
#             continue
#     #start from edges and see if we end up on another edge => straight chain
#     for edge in edges:
#         # if(road_types)
#         # for road in player.roads:
#         #     if(road.connected(intermediate_road)):
#         intermediate_road = edge.find_connected(player.roads)
#         while(intermediate_road.connections == 2):
#             intermediate_road.connections = -1
#             intermediate_road = intermediate_road.find_connected(player.roads)

            

