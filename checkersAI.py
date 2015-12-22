import sys
import copy

class Piece:
	def __init__(self, white):
		self.type = "single"
		if white:
			self.direction = 1
		else:
			self.direction = -1
	
	def getDirections(self):
		direction = self.direction
		baseDirections = [(-1, direction), (1, direction)]
		
		if self.type is "single":
			return baseDirections
		else:
			return baseDirections + [(-1, 0 - direction), (1, 0 - direction)]
	
	def king(self):
		self.type = "double"

class GameState:
	def __init__(self, allies, enemies):
		self.allies = allies
		self.enemies = enemies
		
	def clone(self):
		return GameState(copy.deepcopy(self.allies), copy.deepcopy(self.enemies))

# -------------------------------------------

def validPos(pos):
	return pos in [(x,y) for y in range(0,8) for x in range(0+(y%2),8,2)]

def isFree(state, pos):
	return pos not in state.allies.keys() and pos not in state.enemies.keys()
		
def enemyAt(state, pos, turn):
	if turn:
		return pos in state.enemies.keys()
	else:
		return pos in state.allies.keys()

def move(state, oldPos, newPos, turn):
	newState = state.clone()
	if turn:
		movedPiece = newState.allies.pop(oldPos, None)
		newState.allies[newPos] = movedPiece
		newRow = newPos[1]
		if newRow in [0,7]:
			movedPiece.king()
	else:
		movedPiece = newState.enemies.pop(oldPos, None)
		newState.enemies[newPos] = movedPiece
		newRow = newPos[1]
		if newRow in [0,7]:
			movedPiece.king()
		
	return newState
	
def getPieceAt(state, pos):
	if pos in state.allies.keys():
		return state.allies[pos]
	elif pos in state.enemies.keys():
		return state.enemies[pos]
	else:
		return None
		

def rate(gameState):
	rating = 0
	try:
		rating = float(len(gameState.allies)) / float(len(gameState.enemies))
	except ZeroDivisionError:
		rating = float("inf")
	return rating
	
def tryJumping(state, turn, pos, eatenPs):
	pieces = state.allies
	if not turn:
		pieces = state.enemies
		
	jumps = []
	
	p = pieces[pos]
	for direction in p.getDirections():
		adjacentPos = (pos[0] + direction[0], pos[1] + direction[1])
		if enemyAt(state, adjacentPos, turn):
			jumpPos = (pos[0] + 2*direction[0], pos[1] + 2*direction[1])
			if isFree(state, jumpPos) and validPos(jumpPos):
				newState = move(state, pos, jumpPos, turn)
				if turn:
					newState.enemies.pop(adjacentPos, None) # remove eaten enemy
				else:
					newState.allies.pop(adjacentPos, None) # remove eaten enemy
				jumps += tryJumping(newState, turn, jumpPos, eatenPs + [adjacentPos])
				
	if jumps:
		return jumps
	elif eatenPs:
		return [(pos, eatenPs, state)]
	else:
		return []

def getPossibleMoves(state, turn):
	pieces = state.allies
	if not turn:
		pieces = state.enemies
	
	normalMoves = []
	jumpMoves = []
	
	for pos in pieces.keys():
		p = pieces[pos]
		for direction in p.getDirections():
			adjacentPos = (pos[0] + direction[0], pos[1] + direction[1])
			if isFree(state, adjacentPos) and validPos(adjacentPos):
				normalMoves.append(((pos, adjacentPos), []))
			
			# need recursive function for multiple jumps
			else:
				jMs = tryJumping(state, turn, pos, [])
				for j in jMs:
					jumpMoves.append(((pos, j[0]), j[1]))
	
	if jumpMoves:
		return jumpMoves
	else:
		return normalMoves
					
# (fromPos, toPos, eatenPieces)
def getPossibleStates(state, turn):
	pieces = state.allies
	if not turn:
		pieces = state.enemies
	
	neutralStates = []
	jumpStates = []
	
	for pos in pieces.keys():
		p = pieces[pos]
		for direction in p.getDirections():
			adjacentPos = (pos[0] + direction[0], pos[1] + direction[1])
			if isFree(state, adjacentPos) and validPos(adjacentPos):
				neutralStates.append(move(state, pos, adjacentPos, turn))
			
			# need recursive function for multiple jumps
			else:
				jMs = tryJumping(state, turn, pos, [])
				for j in jMs:
					jumpStates.append(j[2])
	
	if jumpStates:
		return jumpStates
	else:
		return neutralStates
		
def finished(state):
	return len(state.allies.keys()) == 0 or len(state.enemies.keys()) == 0

def minMax(gameState, turn, depth):
	possibleStates = getPossibleStates(gameState, turn)
	
	bestMove = (-float("inf"), None)
	for state in possibleStates:
		rating = minMaxHelper(state, not turn, depth-1)
		if rating >= bestMove[0]:
			bestMove = (rating, state)
	
	print bestMove[0]
	return bestMove[1]



def minMaxHelper(gameState, turn, depth):
	if depth <= 0:
		return rate(gameState)
	
	possibleStates = getPossibleStates(gameState, turn)
	
	if not possibleStates:
		return rate(gameState)
	
	if turn:
		return max([minMaxHelper(state, not turn, depth - 1) for state in possibleStates])
	else:
		return min([minMaxHelper(state, not turn, depth - 1) for state in possibleStates])


		
def printState(state):
	blackSqrs = [(x,y) for y in range(0,8) for x in range(0+(y%2),8,2)]
	print " | A | B | C | D | E | F | G | H |"
	for row in range(0,8):
		line = str(row+1) + "|"
		for col in range(0,8):
			pos = (col, row)
			if pos in state.allies.keys():
				line += " W |"
			elif pos in state.enemies.keys():
				line += " B |"
			else:
				if (col, row) in blackSqrs:
					line += "   |"
				else:
					line += " - |"
		
		print line + " " + str(row+1)
	print " | A | B | C | D | E | F | G | H |"
		

def strToCoords(s):
	try:
		return (ord(s[0]) - ord('A'), int(s[1])-1)
	except:
		return None

def coordsToStr(pos):
	return chr(ord('A') + pos[0]) + str(pos[1]+1)
		

startWhitePos = [(x,y) for y in range(0,3) for x in range(0+(y%2),8,2)]
startBlackPos = [(x,y) for y in range(5,8) for x in range(0+(y%2),8,2)]
white = dict([(pos,Piece(True)) for pos in startWhitePos])
black = dict([(pos,Piece(False)) for pos in startBlackPos])

gameState = GameState(white, black)

while not finished(gameState):
	printState(gameState)
	print ("----------------------------------")
	gameState = minMax(gameState, True, 6)
	moves = dict(getPossibleMoves(gameState, False))
	printState(gameState)
	
	validMove = False
	while not validMove:
		fromPos = strToCoords(raw_input("Enter position of piece to move: ").upper())
		toPos = strToCoords(raw_input("Enter position to move to: ").upper())
		if fromPos and toPos:
			m = (fromPos, toPos) 
			if m in moves.keys():
				validMove = True
				for p in moves[m]:
					gameState.allies.pop(p, None) # remove jumped pieces
				gameState = move(gameState, fromPos, toPos, False)
			else:
				print("Not a valid move, the possible moves are:")
				print [(coordsToStr(m[0]), coordsToStr(m[1])) for m in moves.keys()] 
		else:
			print("Invalid positions")
			
	
	
	

