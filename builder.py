
class Quarry:
	def __init__(self):
		self.level = 0
		self.maxLevel = 50
	
	def cost(self,level):
		return (level * 8, level * 5, level * 10)
	
	def production(self,level):
		return level / 2.0 + 1
		
class Sawmill:
	def __init__(self):
		self.level = 0
		self.maxLevel = 50
	
	def cost(self,level):
		return (level * 10, level * 5, level * 8)
	
	def production(self,level):
		return level / 2.0 + 1
		
class Mine:
	def __init__(self):
		self.level = 0
		self.maxLevel = 50
	
	def cost(self,level):
		return (level * 10, level * 8, level * 5)
	
	def production(self,level):
		return level / 2.0 + 1

q = Quarry()
s = Sawmill()
m = Mine()


def waitAndSpace(curRes, reqRes, productionRates):
	x = zip(curRes, reqRes, productionRates)
	times = [(req - cur) / rate for (cur, req, rate) in x]
	leftovers = [cur + rate*t - req for ((cur, req, rate),t) in zip(x, times)]
	return (max(times), leftovers)
	
	
	
def build((qLvl, sLvl, mLvl), storage, time, buildOrder, bR, depth, ds):
	ds.append(depth)
	maxLvl = 6
	currProduction = (q.production(qLvl), s.production(sLvl), m.production(mLvl))
	
	if qLvl == sLvl == mLvl == maxLvl:
		if len(bR) == 0:
			bR.append((time, buildOrder))
		elif time < bR[0][0]:
			bR[0] = (time, buildOrder)
			

	if qLvl < maxLvl:
		newLevel = qLvl+1
		o = buildOrder + "Q"
		was = waitAndSpace(storage, q.cost(newLevel), currProduction)
		newTime = time + was[0]
		if len(bR) == 0 or newTime < bR[0][0] or True:
			build((newLevel, sLvl, mLvl), was[1], newTime, o, bR, depth+1, ds)
	
	if sLvl < maxLvl:
		newLevel = sLvl+1
		o = buildOrder + "S"
		was = waitAndSpace(storage, s.cost(newLevel), currProduction)
		newTime = time + was[0]
		if len(bR) == 0 or newTime < bR[0][0] or True:
			build((qLvl, newLevel, mLvl), was[1], newTime, o, bR, depth+1, ds)
			
	if mLvl < maxLvl:
		newLevel = mLvl+1
		o = buildOrder + "M"
		was = waitAndSpace(storage, m.cost(newLevel), currProduction)
		newTime = time + was[0]
		if len(bR) == 0 or newTime < bR[0][0] or True:
			build((qLvl, sLvl, newLevel), was[1], newTime, o, bR, depth+1, ds)

ds = []
bR = []
build((0,0,0),(0,0,0),0,"", bR, 0, ds)
print len(bR)

count = {}
for d in ds:
	try:
		count[d] += 1
	except KeyError:
		count[d] = 1

print count











