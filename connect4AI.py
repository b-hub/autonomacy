import sys
import math
import copy

POTENTIAL = [[ 3,  4,  5,  5,  4,  3],
             [ 4,  6,  8,  8,  6,  4],
             [ 5,  8, 11, 11,  8,  5],
             [ 7, 10, 13, 13, 10,  7],
             [ 5,  8, 11, 11,  8,  5],
             [ 4,  6,  8,  8,  6,  4],
             [ 3,  4,  5,  5,  4,  3]]
             
def connections((x, y), r):
	rs = range(-r,r+1)
	return [(x+i, y+j) for i in rs for j in rs if i>=0 and j>=0 and (i==0 or j==0 or abs(i)==abs(j))]

def distance((x1,y1), (x2,y2)):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)
	
def negativeToZero(x):
	if x < 0:
		return 0
	else:
		return x
	
def potentialHelper(state, (disx, disy), (x,y), r):
	playerColor = state[x][y].color
	i = 0
	while i < r:
		try:
			col = x+i*disx
			row = y+i*disy
			if col < 0 or row < 0 or (len(state[col]) > row and state[col][row].color != playerColor):
				break
		except:
			break
		i += 1
	return i
	
def helperCheck(state, (disx, disy), (x,y), r):
	winningColor = state[x][y].color
	i = 1
	while i < r:
		try:
			col = x+i*disx
			row = y+i*disy
			if col < 0 or row < 0 or state[col][row].color != winningColor:
				break
		except:
			break
		i += 1
	return i-1

class GameState:
	def __init__(self, state, maxRows):
		self.state = state
		self.maxRows = maxRows
		
	def insert(self, col, piece):
		#try raising an error if col is full?
		pos = None
		if len(self.state[col]) < self.maxRows:
			self.state[col].append(piece)
			pos = (col, len(self.state[col])-1)
		return pos
		
	def moves(self):
		return [i for i in range(0, len(self.state)) if len(self.state[i]) < self.maxRows]
		
	def valid(self,(x,y)):
		return x >= 0 and x < len(self.state) and y >= 0 and y < maxRows
		
	def winningPos(self, pos):
		s = self.state
		r = 4

		colWin = helperCheck(s, (0,1), pos, r) + helperCheck(s, (0,-1), pos, r)
		rowWin = helperCheck(s, (1,0), pos, r) + helperCheck(s, (-1,0), pos, r)
		diaWin1 = helperCheck(s, (1,1), pos, r) + helperCheck(s, (-1,-1), pos, r)
		diaWin2 = helperCheck(s, (-1,1), pos, r) + helperCheck(s, (1,-1), pos, r)
		
		return colWin >= r-1 or rowWin >=r-1 or diaWin1 >=r-1 or diaWin2 >=r-1
		
	def potential(self, pos):
		s = self.state
		r = 4
		
		col = potentialHelper(s, (0,1), pos, r) + potentialHelper(s, (0,-1), pos, r)
		row = potentialHelper(s, (1,0), pos, r) + potentialHelper(s, (-1,0), pos, r)
		dia1 = potentialHelper(s, (1,1), pos, r) + potentialHelper(s, (-1,-1), pos, r)
		dia2 = potentialHelper(s, (-1,1), pos, r) + potentialHelper(s, (1,-1), pos, r)
		
		pot = map(negativeToZero, [col-4, row-4, dia1-4, dia2-4])
		return (sum(pot), pot)
	
	def potentialOf(self, piece):
		potentialTotal = 0
		for x in range(0, len(self.state)):
			for y in range(0, len(self.state[x])):
				if self.state[x][y].color == piece.color:
					pot = self.potential((x,y))
					potentialTotal += pot[0]
		return potentialTotal
		
	def clone(self):
		return GameState(copy.deepcopy(self.state), self.maxRows)
	
	def __str__(self):
		ret = "|" + "|".join([str(i) for i in range(1, len(self.state)+1)]) + "|\n"
		j = self.maxRows-1
		while j >= 0:
			line = "|"
			for col in self.state:
				try:
					line += col[j].color + "|"
				except IndexError:
					line += " |"
			j -= 1
			ret += line + '\n'
		return ret

class Piece:
	def __init__(self, color, isComputer):
		self.color = color	
		self.computer = isComputer

def minMax(gameState, players, p, depth):
	player = players[0]
	possibleStates = []
	for m in gameState.moves():
		state = gameState.clone()
		pos = state.insert(m, player)
		possibleStates.append((m, state, pos))
	players = players[1:] + [player]
	
	bestMove = (-float("inf"), None)
	for (m, state, pos) in possibleStates:
		rating = minMaxHelper(state, players, p, pos, depth-1)
		if rating >= bestMove[0]:
			bestMove = (rating, m)
	
	print bestMove[0]
	return bestMove[1]
	

def minMaxHelper(gameState, players, p, (x,y), depth):
	
	player = players[0]
	possibleStates = []
	for m in gameState.moves():
		state = gameState.clone()
		pos = state.insert(m, player)
		possibleStates.append((state, pos))
	players = players[1:] + [player]
	
	if not possibleStates or depth <= 0 or gameState.winningPos((x,y)):
		if gameState.winningPos((x,y)):
			if p.color == gameState.state[x][y].color:
				return float("inf")
			else:
				return -float("inf")
		else:
			enemyPotential = sum([gameState.potentialOf(ep) for ep in players if ep.color != p.color])
			return gameState.potentialOf(p) / float(enemyPotential)
	
	if player.color == p.color:
		return max([minMaxHelper(state, players, p, pos, depth - 1) for (state, pos) in possibleStates])
	else:
		return min([minMaxHelper(state, players, p, pos, depth - 1) for (state, pos) in possibleStates])

# ---------------------------------------------

foresight = int(raw_input("Enter number of moves the computer will look ahead (4 if slow): "))

s = GameState([[] for i in range(0, 7)], 6)
players = [Piece("X", True), Piece("O", True)]

pos = None
while not pos or not s.winningPos(pos):
	print s
	piece = players[0]
	if piece.computer:
		col = minMax(s, players, piece, foresight)
	else:
		col = int(raw_input("Player " + piece.color + "'s turn: ")) - 1
	pos = s.insert(col, piece)
	potentialTotal = 0
	for x in range(0, len(s.state)):
		for y in range(0, len(s.state[x])):
			if s.state[x][y].color == piece.color:
				pot = s.potential((x,y))
				potentialTotal += pot[0]
	print potentialTotal
	players = players[1:] + [piece]

print (str(s.state[pos[0]][pos[1]].color) + " wins!")

