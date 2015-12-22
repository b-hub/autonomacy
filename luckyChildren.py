import sys
import random

def randomGenome(nOptions):
	genome = [random.randint(0, 100) for n in range(0, nOptions)]
	# and now normalise
	s = float(sum(genome))
	ret = map(lambda x: x/s, genome)
	return ret
	
	
# assume len(mGenome) = len(fGenome)
def child(parents, mutationProb):
	size = len(parents[0])
	lesserParent = random.randint(0,1)
	greaterParent = abs(lesserParent-1)
	fstHalf = [parents[lesserParent][random.randint(0, size-1)] for n in range(0, size/2)]
	sndHalf = [parents[greaterParent][random.randint(0, size-1)] for n in range(0, (size+1)/2)]
	return fstHalf + sndHalf

def avgChild(mother, father, mutationProb):
	child = [(mother[i] + father[i]) / 2.0 for i in range(0, len(mother))]
	return child
	
def outcome(outcomes):
	r = random.randint(0, 99) / 100.0
	i = 0
	tot = 0
	while i < len(outcomes):
		if tot + outcomes[i] >= r:
			return i
		tot += outcomes[i]
		i += 1
	#print ("WHAT!?" + str(tot) + ", " + str(r))
	return i-1

def partners(ps, n):
	size = len(ps)
	pairs = []
	while len(pairs) < n:
		pairs.append((ps[random.randint(0,size-1)], ps[random.randint(0,size-1)]))
	return pairs
	
def nextGeneration(population, world):
	bankAccounts = []
	winningOption = outcome(world)
	for p in population:
		chosenOption = outcome(p)
		investment = p[chosenOption]
		if chosenOption == winningOption:
			bankAccounts.append(investment)
		else:
			bankAccounts.append(-investment)
	
	results = sorted(zip(bankAccounts, population), reverse=True)
	bestHalf = [p for (b, p) in results[:len(population)]]
	
	newPop = bestHalf + [randomGenome(genomeSize) for n in range(1, len(population) - len(bestHalf))]
	nextGen = [child(pair, 0) for pair in partners(newPop, len(population))]
	
	return nextGen
	
def averageGenome(ps):
	avgGenome = []
	i = 0
	while i < len(ps[0]):
		avgGenome.append(reduce((lambda x, y: x + y), [p[i] for p in ps]) / float(len(ps)))
		i += 1
	
	return avgGenome
	
	
	
genomeSize = int(sys.argv[1])
poolSize = int(sys.argv[2])
world = [0.7, 0.25, 0.5]

population = [randomGenome(genomeSize) for n in range(1, poolSize)]

i = 0
while i < 1:
	print averageGenome(population)
	population = nextGeneration(population, world)
	i += 1
