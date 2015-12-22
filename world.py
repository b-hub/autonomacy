import random

FOOD_CONSUMPTION_RATE = 1

class Village:
	startingPopulation = 10
	def __init__(self):
		self.population = [person() for n in range(0, startingPopulation)]
		self.food = len(self.population) * FOOD_CONSUMPTION_RATE * 100
		
# -----------------------------------------

MAX_WOLF_ENCOUNTER_CHANCE = 0.1
SAFE_WOLF_HUMAN_RATIO = 2.0 / 1.0

class forest:
	def __init__(self):
		self.worldEncounterChance = random.random() * MAX_WOLF_ENCOUNTER_CHANCE
		self.resource = "wood"
	
	def extractResources(self, people):
		r = random.random()
		wolfs = random.randint(1, 6)
		# humans encounter wolf(s)
		if r <= self.worldEncounterChance:
			# if wolfs outnumber humans enough then humans are wiped out
			if wolfs / float(len(people)) > SAFE_WOLF_HUMAN_RATIO:
				for p in people:
					p.die()
		
		for p in people:
			if p.alive():
				p.gather(self.resource)
