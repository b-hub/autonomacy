import sys
import random
import time

beings = {}
DAY = 0

class Human:
	def __init__(self, dob, village): 
		self.matureAge = 18 * 365
		self.maxAge = random.randint(50, 100) * 365
		self.age = (DAY - dob)
		self.sex = random.randint(0,1)
		self.pregnancyCountdown = None
		self.relationships = {}
		
		self.name = self.generateName()
		self.village = village
		
	def isMature(self):
		return self.age >= self.matureAge
		
	def die(self):
		self.village.removeVillager(self)
		#print (self.getName() + " died!")
	
	def giveBirth(self):
		child = Human(DAY, self.village)
		#print(self.getName() + " gave birth to " + child.getName())
		self.village.addVillager(child)
		self.pregnancyCountdown = None
		
	def update(self):
		self.age += 1
		if self.age >= self.maxAge:
			self.die()
		else:
			if self.pregnancyCountdown is not None:
				self.pregnancyCountdown -= 1
				if self.pregnancyCountdown <= 0:
					self.giveBirth()
	
	def getAge(self):
		return self.age / 365
		
	def getName(self):
		s =  self.name + "(" + str(self.getAge()) + ")"
		return s
	
	def interact(self, being, duration):
		r = random.random()
		try:
			#change relationship based on duration and maybe activity
			
			chanceOfSex = self.sexualAttraction(being) * being.sexualAttraction(self)
			if self.isMature() and being.isMature() and r <= chanceOfSex:
				#print (self.getName() + " and " + being.getName() + " had sex!")
				if self.sex == 0 and being.sex == 1:
					self.impregnate()
				elif being.sex == 0 and self.sex == 1:
					being.impregnate()
					
			
		except KeyError:
			if self.isMature() and being.isMature():
				attraction = random.random()
				self.relationships[being] = {"attraction": attraction, "like": random.random()}
				#print (self.getName() + " and " + being.getName() + " meet for the first time...") 
			
	def generateName(self):
		nameLength = random.randint(2, 6) - 1
		name = chr(random.randint(65, 90))
		name += "".join([chr(random.randint(97, 122)) for n in range(0, nameLength)])
		
		if self.sex == 0:
			name += "0"
		else:
			name += "1"
		
		return name
		
	def impregnate(self):
		if self.sex == 0 and self.pregnancyCountdown is None:
			self.pregnancyCountdown = 270
			#print (self.getName() + " is pregnant!")
			
	def sexualAttraction(self, being):
		return self.relationships[being]["attraction"]
		
n = int(raw_input("Enter number of humans: "))

class Village:
	def __init__(self):
		self.vs = []
	
	def addVillager(self, villager):
		self.vs.append(villager)
	
	def removeVillager(self, villager):
		self.vs.remove(villager)
		
	def getVillagers(self):
		return self.vs
		
v1 = Village()
v2 = Village()
for x in range(0, n):
	v1.addVillager(Human(-18 * 365, v1))
	v2.addVillager(Human(-18 * 365, v2))


while True:
	print ("Day: " + str(DAY) + "(" + str(DAY / 356) + "), PopulationV1: " + str(len(v1.vs)) + ", PopulationV2: " + str(len(v2.vs)))
	interactions = random.randint(0, 10)
	while interactions > 0:
		v1.getVillagers()[random.randint(0, len(v1.getVillagers())-1)].interact(v1.getVillagers()[random.randint(0, len(v1.getVillagers())-1)], 10)
		v2.getVillagers()[random.randint(0, len(v2.getVillagers())-1)].interact(v2.getVillagers()[random.randint(0, len(v2.getVillagers())-1)], 10)
		interactions -= 1
	
	DAY += 1
	
	for h in v1.getVillagers():
		h.update()
	
	for h in v2.getVillagers():
		h.update()

		
	
