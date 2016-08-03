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
		if self.AI_code<0:
			self.wood += 20
			self.brick += 20
			self.wheat += 20
			self.sheep += 20
			self.stone += 20
		# else:
		# 	self.wood += 20
		# 	self.brick += 20

		#Development cards: lets leave these for now

		# Score keeping
		self.score = 0
		self.road_length = 0 
		self.has_longest_road = False
		self.has_largest_army = False # For once we do development cards

	def __eq__(self,other):
		return((self.index == other.index) and (self.name == other.name))

	def resource_count(self):
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


