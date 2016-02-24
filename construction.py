import sys

edge_tiles =    [0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7]
hidden_tiles =  [0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7,8,12,13,29,36,40]

#checks if two given tiles are neighbors, doesn't matter if a road cannot be constructed between them (like 40 and 41)
def neighbor_tile(hex1,hex2): #hex1 must be smaller than hex2
	
	if(hex1>hex2): #ensuring that hex1 is always smaller so we can search for hex2 downwards
		print("change the order of hex tiles in neighbor_tile function")
		sys.exit()

	hex1_on_edge = hex1 in  edge_tiles
	hex2_on_edge = hex2 in edge_tiles

	if(abs(hex1-hex2)>8): #tiles are too far apart to be neighbors
		# print("Too far apart")
		return False
	
	elif(abs(hex1-hex2)==1):
		# print("Could be in the same row")
		if(hex1_on_edge and hex2_on_edge): 
			if(hex1%7==6):
				return False #eg: tile 13 and 14 are not neighbors
			else:
				return True	#tiles 3 and 4 are both edge tiles but are neighbors
		else:
			return True

	elif((hex1//7)%2 == 0): #odd numbered row
		# print("Odd numbered row")
		if(abs(hex1-hex2)==6 or abs(hex1-hex2)==7):
			return True
		else:
			return False

	elif((hex1//7)%2 == 1): #even numbered row
		# print("Odd numbered row")
		if(abs(hex1-hex2)==7 or abs(hex1-hex2)==8):
			return True
		else:
			return False

	else:
		print("What the hell")
		sys.exit()


	
class point:
	
	def __init__(self,hex1,hex2,hex3):
		if((hex1==hex2) or (hex2==hex3) or (hex3==hex1)):
			print("Enter three unique tiles.")
			sys.exit()

		# sort x,y,z in increasing order.
		x = min(hex1,hex2,hex3)
		z = max(hex1,hex2,hex3)
		y = hex1+hex2+hex3-x-z
		
		#check if such a point exists
		# print(neighbor_tile(x,y), neighbor_tile(y,z), neighbor_tile(x,z))
		if(neighbor_tile(x,y) and neighbor_tile(y,z) and neighbor_tile(x,z)):
			if((x in hidden_tiles) and (y in hidden_tiles) and (z in hidden_tiles)): #like 40,47,48
				print("Point lies in the sea!")
				sys.exit()
			else:
				pass
		else:
			print("Invalid point.")
			sys.exit()
		

while(True):
	x = int(input("hex1: "))
	y = int(input("hex2: "))
	z = int(input("hex3: "))
	a = point(x,y,z)
	# if(neighbor_tile(x,y)):
	# 	print("They are neighbors.\n")
	# else:
	# 	print("Not neighbors.\n")