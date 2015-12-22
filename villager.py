import sys
import random

class MentalAttr:
	def __init__(self):
		self.attr["stubborness"] = random.random()
		self.attr["intelligence"] = random.random()
		
class PhysicalAttr:
	def __init__(self):
		# 0=Female, 1=Male
		self.sex = random.randint(0,1)
		self.speed = random.random()

class Person:
	def __init__(self):
		self.physical = PhysicalAttr()
		self.mental = MentalAttr()
		
class King:
	def __init__(self, person):
	self.person = person
		
	def imaginOptions(self, allOptions):
		pass
		
		

