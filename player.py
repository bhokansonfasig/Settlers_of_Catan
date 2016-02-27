from point import Point
from road import Road

class Player:

	def __init__(self,index,name,AI_code):
		# Index of player. Set despite turn order
		#  (i.e. player with index 1 may play third)
		self.index = index

		# Color of player's pieces
		if self.index==1:
			self.color = "red"
		elif self.index==2:
			self.color = "blue"
		elif self.index==3:
			self.color = "green"
		elif self.index==4:
			self.color = "white"

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

		#Development cards: lets leave these for now

		# Score keeping
		self.road_length = 0 #we better deal with this from early on
		self.score = 0

	def resource_count(self):
		return self.wood + self.brick + self.wheat + self.sheep + self.stone

	# Counting resource cards when the robber comes
	def robbable(self):
		if(self.resource_count() > 7):
			return True
		else:
			return False

	def __eq__(self,other):
		return((self.index == other.index) and (self.name == other.name))
