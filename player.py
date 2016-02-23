class player:
	
	def __init__(self,index):
		#Index determines the turn order
		self.index = index
	
		# Building resources limit
		self.road_max = 15
		self.settlement_max = 5
		self.city_max = 4
	
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

	def resource_cards_count(self):
		return self.wood + self.brick + self.wheat + self.sheep + self.stone	

	#counting resource cards when the robber comes
	def rob(self):
		if(self.resource_cards_count() > 7): 
			return True
		else: 
			return False

