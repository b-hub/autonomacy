import sys
import random

def normalise(arr):
	s = float(sum(arr))
	return map(lambda x: x/s, arr)

# can improve with matrix multiplication
def decisionMatrix(n):
	maxPoint = 10
	matrix = []
	i = 0
	while i < n:
		row = []
		selfVote = random.randint(n * (maxPoint/2), n * (maxPoint/2) * 9)
		j = 0
		while j < n:
			if i == j:
				row.append(selfVote)
			else:
				row.append(random.randint(0, maxPoint))
			j += 1
		matrix.append(normalise(row))
		i += 1
		
	return matrix

def vote(decisions):
	r = random.random()
	acc = 0
	i = 0
	while i < len(decisions):
		acc += decisions[i]
		if r <= acc:
			return i
		i += 1
	
	# shouldn't happen - but may with floating point error
	print(str(r) + ": " + str(decisions) + " = " + str(sum(decisions)))
	exit(-1)
	

def applyPanic(matrix, panicLevel, popularity):
	panicMap = []
	i = 0
	while i < len(matrix):
		voteSelf = matrix[i][i]
		voteOther = 1 - voteSelf
		influence = voteSelf * panicLevel
		
		j = 0
		while j < len(matrix):
			pop = 0.0
			try:
				pop = popularity[j]
			except KeyError:
				pass
			
			if pop < 0.5:
				if i == j:
					matrix[i][j] -= influence
				else:
					matrix[i][j] += influence * matrix[i][j] / voteOther
				
			#majority rule...
			#decision becomes closer to previous vote popularity by a factor of panicLevel
			matrix[i][j] += (pop - matrix[i][j]) * panicLevel
			
			j += 1
		
		# incase maths mess up re-normalise it
		if sum(matrix[i]) != 1:
			matrix[i] = normalise(matrix[i])
		
		i += 1

def popularity(votes):
	tally = {}
	n = float(len(votes))
	for v in votes:
		try:
			tally[v] += 1
		except KeyError:
			tally[v] = 1
	for key in tally.keys():
		tally[key] /= n
	return tally
				

n = int(raw_input("Enter the number of players: "))
pMax = float(int(raw_input("Enter the number of Votes before max panic sets in: ")))
dM = decisionMatrix(n)

p = 0
i = 0
while True:
	#print dM
	pop = popularity([vote(voter) for voter in dM])
	print ("POLL: " + str(i))
	for poll in sorted([(pop[voter], voter) for voter in pop.keys()], reverse=True)[:5]:
		print (poll)
	if len(pop) == 1:
		print i
		break
	applyPanic(dM, p / pMax, pop)
	if p < pMax:
		p += 1
	i += 1




