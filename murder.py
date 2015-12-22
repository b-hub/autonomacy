class Map:
	def __init__(self, layout):
		self.layout = layout
	
	def __str__(self):
		return str(self.layout)
	
	def shortest_path(self):
		pass
		
		
class Room:
	def __init__(self, name, owner):
		self.name = name
		self.occupants = []
		self.owner = owner
		self.locked = False
		
	def __str__(self):
		if owner:
			return owner + "'s " + self.name
		else:
			return self.name
	
	def enters(self, resident):
		self.occupants.append(resident)
	
	def leaves(self, resident):
		self.occupants.remove(resident)

aRoom = Room("Bedroom", "Alice")
bRoom = Room("Bedroom", "Ben")
cRoom = Room("Bedroom", "Charlie")

k = Room("Kitchen", None)
d = Room("Dining Room", None)
g = Room("Games Room", None)
l = Room("Library", None)
s = Room("Study", None)
c = Room("Conservatory", None)

c1 = Room("Corridor1", None)
c2 = Room("Corridor2", None)
c3 = Room("Corridor3", None)
c4 = Room("Corridor1", None)
c5 = Room("Corridor2", None)
c6 = Room("Corridor3", None)


layout = {: set([('B', 10), ('C', 5)]),
          'RoomB': set(['D', 'E']),
          'RoomC': set(['F']),
          'Corridor': set([]),
          'E': set(['F']),
          'F': set([])}
