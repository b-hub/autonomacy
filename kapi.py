QUARRY_DATA_LOC = "quarryData.txt"
SAWMILL_DATA_LOC = "sawmillData.txt"
OREMINE_DATA_LOC = "oremineData.txt"

import bisect


def read_file(filename):
	eFile = open(filename, 'r')
	content = eFile.read()
	eFile.close()
	return content
	
def parseResData(filename):
	content = read_file(filename)
	data = []
	
	for line in content.split('\n'):
		lineData = [d.strip() for d in line.split('\t')]
		if len(lineData) == 6:
			level = int(lineData[0])
			costStone = int(lineData[1])
			costWood = int(lineData[2])
			costIron = int(lineData[3])
			costSettler = int(lineData[4].split('/')[0])
			production = float(lineData[5])
			
			data.append((level, costStone, costWood, costIron, costSettler, production))
			
	return data
	
class resBuilding:
	def __init__(self, data):
		self.data = data
		
	def cost(self, level):
		lvlData = self.data[level]
		return (lvlData[1], lvlData[2], lvlData[3]) #lvl[4] (settlers required)
		
	def production(self, level):
		return self.data[level][5]
		
		
graph = {'A': set(['B', 'C']),
         'B': set(['D', 'E']),
         'C': set(['F']),
         'D': set([]),
         'E': set(['F']),
         'F': set([])}
         
def bfs(graph, root):
    visited, queue = set(), [root]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)
    return visited

print bfs(graph, 'A') # {'B', 'C', 'A', 'F', 'D', 'E'}

def bfs_path(graph, root, goal):
    queue = [(root, [root])]
    while queue:
        (node, path) = queue.pop(0)
        for next in graph[node]:
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

#print list(bfs_path(graph, 'A', 'F')) # [['A', 'C', 'F'], ['A', 'B', 'E', 'F']]
                
def waitAndSpace(curRes, reqRes, productionRates):
	x = zip(curRes, reqRes, productionRates)
	times = [(req - cur) / rate for (cur, req, rate) in x]
	maxT = max(times)
	if maxT < 0:
		maxT = 0
	leftovers = [int(cur + rate*maxT - req) for (cur, req, rate) in x]
	for l in leftovers:
		if l < 0:
			print ((x, times, maxT, leftovers))
			exit(-1)
	return (maxT, leftovers)

#building, (qLvl, sLvl, mLvl), storage, time, buildOrder   
def bfs_builder(root, goal, maxDepth, (q,s,m)):
	queue = [(root, root[0])]
	while queue:
		(node, path) = queue.pop(0)
		print ("Depth: " + str(len(path)) + "		Queue: " + str(len(queue)))
		(Building, (qL, sL, mL), currRes, time) = node
		currProduction = (q.production(qL), 
                      s.production(sL), 
                      m.production(mL))
        
		options = []
        
		if qL < goal[0]:
			newLvl = qL+1
			was = waitAndSpace(currRes, q.cost(newLvl), currProduction)
			options.append(('Q', (newLvl, sL, mL), was[1], time + was[0])) 
        
		if sL < goal[1]:
			newLvl = sL+1
			was = waitAndSpace(currRes, s.cost(newLvl), currProduction)
			options.append(('S', (qL, newLvl, mL), was[1], time + was[0])) 
        
		if mL < goal[2]:
			newLvl = mL+1
			was = waitAndSpace(currRes, m.cost(newLvl), currProduction)
			options.append(('M', (qL, sL, newLvl), was[1], time + was[0])) 
        
		for next in options:
			if next[1] == goal or (maxDepth is not None and len(path) == maxDepth):
				return ((next[3], sum(next[2]), next[1]), path + next[0])
			else:
				queue.append((next, path + next[0]))
				#keys = [k[0][3] for k in queue]
				#time = next[3]
				#queue.insert(bisect.bisect(keys, time), (next, path + next[0]))
		
		#queue.sort(key = lambda r: r[0][1], reverse=True) # messes up the result for some reason
		queue.sort(key = lambda r: r[0][3])
		#queue = queue[:]
        

q = resBuilding(parseResData(QUARRY_DATA_LOC))
s = resBuilding(parseResData(SAWMILL_DATA_LOC))
m = resBuilding(parseResData(OREMINE_DATA_LOC))

result = bfs_builder(('R', (0,0,0),(100,100,100),0),(5,5,5),None, (q, s, m))
print result




