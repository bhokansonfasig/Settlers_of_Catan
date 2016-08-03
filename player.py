from point import Point
from road import Road
import pickle

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
			# self.color = "#FFFFFF"  # White

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

		# Strings of resources for ports owned
		self.ports = []

		#Access to points: useful for implementing building of new roads
		self.points = []

		# Acquired resources
		self.wood = 0
		self.brick = 0
		self.wheat = 0
		self.sheep = 0
		self.stone = 0

		# For testing, add resources to human players and fewer to computers
		# if self.AI_code<0:
		# 	self.wood += 20
		# 	self.brick += 20
		# 	self.wheat += 20
		# 	self.sheep += 20
		# 	self.stone += 20
		# else:
		# 	self.wood += 20
		# 	self.brick += 20

		#Development cards: lets leave these for now

		# Score keeping
		self.score = 0
		self.road_length = 0
		self.has_longest_road = False
		self.has_largest_army = False # For once we do development cards
		
		self.file_name = self.name + ".soc"
		print (self.file_name, type(self.file_name))
		player_file_exists = False
		from os import remove
		try:
			player_file_exists = os.path.isfile(self.file_name)
			# print ("STEP1")
		except:
			pass
			# print ("STEP2")
		if player_file_exists:
			# print ("STEP3")
			
			remove(self.file_name)
			print("Deleted old player file", self.file_name)


	def __eq__(self,other):
		return((self.index == other.index) and (self.name == other.name))

	def deflate(self):
		points = [p.coordinate for p in self.points]
		roads  = [r.coordinates for r in self.roads]
		print ('stored:',self.name,roads)
		settlements = [s.coordinate for s in self.settlements]
		cities = [c.coordinate for c in self.cities]
		resources = [self.wood,self.brick,self.wheat,self.sheep,self.stone]
		data = [points,roads,settlements,cities,resources,self.score]
		with open(self.file_name,'wb') as f:
			pickle.dump(data,f)
		f.close()
	
	def inflate(self):
		with open(self.file_name,'rb') as f:
			data = pickle.load(f)
		f.close()

		# print (self.name)
		for x in data[0]: 
			if x not in [p.coordinate for p in self.points]:
				print (self.name,'read point:',x)
				self.points.append(Point(x[0],x[1],x[2]))

		for x in data[1]: 
			if x not in [r.coordinates for r in self.roads]:
				print (self.name,' read road:',x)
				p1 = Point(x[0][0],x[0][1],x[0][2])
				p2 = Point(x[1][0],x[1][1],x[1][2])
				self.roads.append(Road(p1,p2))

		for x in data[2]:
			# print (self.name,'new settlement: ',x) 
			if x not in [s.coordinate for s in self.settlements]:
				self.settlements.append(Point(x[0],x[1],x[2]))	

		for x in data[3]: 
			# print (self.name,'new city: ',x)
			if x not in [s.coordinate for s in self.cities]:
				self.cities.append(Point(x[0],x[1],x[2]))

		# print (data[4],'\n')
		# for x in data[4]:
		# 	self.wood = x[0]
		# 	self.brick = x[1]
		# 	self.wheat = x[2]
		# 	self.sheep = x[3]
		# 	self.stone = x[4]

		self.score = data[5]

	def resource_count(self):
		self.deflate()
		self.inflate()
		return self.wood + self.brick + self.wheat + self.sheep + self.stone

	def single_resource_count(self,check_resource):
		if check_resource.lower()=="wood":
			return self.wood
		elif check_resource.lower()=="brick":
			return self.brick
		elif check_resource.lower()=="sheep":
			return self.sheep
		elif check_resource.lower()=="wheat":
			return self.wheat
		elif check_resource.lower()=="stone":
			return self.stone

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


	def adjacent_point(self,p1,p2):
		common_hex = len(p1+p2) - len(set(p1+p2))
		if(common_hex == 2):
			return True
		else:
			return False
