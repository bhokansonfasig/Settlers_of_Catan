from point import Point
from road import Road

class Player:

	def __init__(self,index,name,AI_code):
		# Index of player. Set despite turn order
		#  (i.e. player with index 1 may play third)
		self.index = index

		# Color of player's pieces
		if self.index==1:
			self.color = "#EE0000"  # Red
		elif self.index==2:
			self.color = "#0000CC"  # Blue
		elif self.index==3:
			self.color = "#00CC00"  # Green
		elif self.index==4:
			self.color = "#FF8000"  # Orange

		self.name = name

		# What AI level is the player (-1 for human)
		self.AI_code = AI_code

		# Building resources limit
		self.road_max = 15
		self.settlement_max = 5
		self.city_max = 4

		# Structures built
		self.roads = []
		self.settlements = []
		self.cities = []

		#Access to points: useful for implementing building of new roads
		self.points = []

		# Acquired resources
		self.wood = 0
		self.brick = 0
		self.wheat = 0
		self.sheep = 0
		self.stone = 0

		# For testing, add resources to human players and fewer to computers
		if self.AI_code<0:
			self.wood += 20
			self.brick += 20
			self.wheat += 20
			self.sheep += 20
			self.stone += 20
		else:
			self.wood += 20
			self.brick += 20

		#longest road stuff
		self.road_types = [[],[],[],[],[]] #the index corresponds to the number of connections
		self.calculation_complete = False
		self.longest_simple_chain = 0

		#Development cards: lets leave these for now

		# Score keeping
		self.score = 0
		self.road_length = 0 #we better deal with this from early on
		self.has_longest_road = False
		self.has_largest_army = False # For once we do development cards

	def __eq__(self,other):
		return((self.index == other.index) and (self.name == other.name))

	def resource_count(self):
		return self.wood + self.brick + self.wheat + self.sheep + self.stone

	# Counting resource cards when the robber comes
	def robbable(self):
		if(self.resource_count() > 7):
			return True
		else:
			return False

	def calculate_score(self):
		self.score = 0
		# One point for each settlement
		self.score += len(self.settlements)
		# Two points for each city
		self.score += 2*len(self.cities)
		# Two points for longest road
		if self.has_longest_road:
			self.score += 2
		# Two points for largest army
		if self.has_largest_army:
			self.score += 2

	def give_resource(self,resource):
		if resource=="wood":
			self.wood += 1
		elif resource=="brick":
			self.brick += 1
		elif resource=="wheat":
			self.wheat += 1
		elif resource=="sheep":
			self.sheep += 1
		elif resource=="stone":
			self.stone += 1

	#alots a number to each road which corresponds to how many other roads its connected to
	def classify_road(self):
	    self.road_types = [[],[],[],[],[]]
	    for road in self.roads:
	        connections = 0
	        for other_road in self.roads:
	            # if(road == other_road):
	            #     continue
	            # else:
	            if(road.connected(other_road)):
	                connections += 1
	        self.road_types[connections].append(road)


	def isolate_simple_straight_chains(self):
	    chain_lengths = []
	    self.calculation_complete = False
	    self.classify_road()
	    for edge in self.road_types[1]:
	        length = 0
	        intermediate_road = edge
	        self.road_types[1].remove(edge)
	        while (len(intermediate_road.find_connected(self.road_types[2])) != 0):
	            intermediate_road = intermediate_road.find_connected(self.road_types[2])[0]
	            self.road_types[2].remove(intermediate_road)
	            length += 1
	        if(len(intermediate_road.find_connected(self.road_types[1]))==1):
	            other_edge = intermediate_road.find_connected(self.road_types[1])[0]
	            self.road_types[1].remove(other_edge)
	            chain_lengths.append(length+2)
	        # print(chain_lengths,self.name)

	    if(len(chain_lengths) == 2): #there were two chains, and they were identified
	        self.calculation_complete = True
	    if(len(chain_lengths) == 1): #checking if whats left is too small to give the longest road
	        leftover = len(self.roads)-chain_lengths[0]
	        if (leftover < (chain_lengths[0]+1)): #the leftover _must_ have a longer chain, else no need to evaluate it
	            self.calculation_complete = True

	    if(self.calculation_complete):
	        print("longest:",max(chain_lengths),self.name)

	    #the length of the chain that we do have is useful for comparision while looking at the complex structure
	    if(len(chain_lengths)!=0):
	        longest_simple_chain = max(chain_lengths)
	    else:
	    	longest_simple_chain = 0

	def isolate_loops(self):
		self.isolate_simple_straight_chains()
		occupied_edges = [0]*49
		tiles_with_loops = []

		for road in self.road_types[2]+self.road_types[3]+self.road_types[4]:
			occupied_edges[road.tiles[0]] += 1
			occupied_edges[road.tiles[1]] += 1

		for tile in range(0,len(occupied_edges)):
			if(occupied_edges[tile]==6):
				tiles_with_loops.append(tile)

		return tiles_with_loops

		# for index in tiles_with_loops:
		# 	print(self.name,index)

	#a single road connected to a loop is an edge, but it has _two_ connections
	def find_complex_edges(self):
		self.isolate_simple_straight_chains()
		complex_edges = []
		for possible_edge in self.road_types[2]:
			neighbors = possible_edge.find_connected(self.roads)

			a = possible_edge.common_tile(neighbors[0])
			b = possible_edge.common_tile(neighbors[1])
			c = neighbors[0].common_tile(neighbors[1])

			if(len(set(a+b+c))==3):
				complex_edges.append(possible_edge)

		print(self.name,"has",len(complex_edges),"complex edges")

		return complex_edges





	# def only_branches_and_no_loops(self):
	# 	self.isolate_simple_straight_chains()
	# 	if(len(self.isolate_loops)==0):
	# 		complex_edges = find_complex_edges()
	# 		all_edges = self.road_types[1]+complex_edges
	# 		output = [[0 for x in range(len(all_edges)))] for x in range(len(all_edges))] 
		
	# 		for edge in all_edges:
	# 			all_edges = self.road_types[1]+complex_edges
	# 			paths = []
	# 			intermediate_road = edge
	# 			while (len(all_edges) != 0):
	# 				middle_roads = road_types[2]+road_types[3]+road_types[4]
	# 	            intermediate_road = intermediate_road.find_connected(middle_roads)
	# 	            paths.append[intermediate_road]


	# def only_branches_and_no_loops(self):
	# 	import copy
	# 	self.isolate_loops()
	# 	road_types = copy.deepcopy(self.road_types)
	# 	output = []
	# 	if(len(loops)==0):
	# 		for edge in road_types[1]:
	# 			paths = []
	# 			intermediate_road = edge
	# 			while (len(road_types[1]) != 0):
	# 				middle_roads = road_types[2]+road_types[3]+road_types[4]
	# 	            intermediate_road = intermediate_road.find_connected(middle_roads)
	# 	            self.road_types[2].remove(intermediate_road)

