from random import randint
from BaseAI_3 import BaseAI
import time, math

NEG_INF = float("-inf")
POS_INF = float("inf")
SPAWNED_TILES_VALUES = [2,4]
TIME_BUFFER = 0.08 # number of seconds remaining at which we end the depth-first traversal

class PlayerAI(BaseAI):
	nodes_expanded = 0 
	MAX_DEPTH = 4

	# is this grid a terminal state?
	def isTerminalState(self, grid):
		return len(grid.getAvailableMoves()) == 0 

	# are we in the buffer time?
	def inBufferTime(self, start_time):
		time_elapsed = time.clock() - start_time
		time_remaining = 0.25 - time_elapsed
		return time_remaining < TIME_BUFFER

	def calculateMono(self, currNumber, nextNumber):
		dMono = 0
		if currNumber < nextNumber: dMono = 1 
		if currNumber > nextNumber: dMono = -1
		return dMono

	def calculateBumpiness(self, currNumber, nextNumber):
		currNumberVal = math.log(currNumber, 2) if currNumber != 0 else 0 
		nextNumberVal = math.log(nextNumber, 2) if nextNumber != 0 else 0 
		return abs(currNumberVal - nextNumberVal)

	def generateHeuristic(self, grid):
		availableCells = len(grid.getAvailableCells())
		availableCellsWeight = 1
		monoWeight = 1
		smoothWeight = 1

		# coordinate system: x is the row-wise index, 0 is the left-most column
		# monotonicity: increases in row and column-wise directions
		# smoothness: keeps neighboring cells low

		# iterate over the columns
		colWiseMono = 0 
		colWiseBumpiness = 0		
		(y_idx, x_idx) = (0,0)
		while y_idx < 4:
			while x_idx < 3:
				currNumber = grid.map[x_idx][y_idx] 
				nextNumber = grid.map[x_idx + 1][y_idx]
				colWiseMono += self.calculateMono(currNumber, nextNumber) 
				colWiseBumpiness += self.calculateBumpiness(currNumber, nextNumber)			
				x_idx += 1
			x_idx = 0 
			y_idx += 1
		
		# iterate over the rows
		rowWiseMono = 0
		rowWiseBumpiness = 0
		(y_idx, x_idx) = (0,0)
		while x_idx < 4:
			while y_idx < 3:
				currNumber = grid.map[x_idx][y_idx] 
				nextNumber = grid.map[x_idx][y_idx+1]
				rowWiseMono += self.calculateMono(currNumber, nextNumber) 
				rowWiseBumpiness += self.calculateBumpiness(currNumber, nextNumber)		
				y_idx += 1
			y_idx = 0
			x_idx += 1

		mono = abs(colWiseMono) + abs(rowWiseMono)
		smoothness = 0 - rowWiseBumpiness - colWiseBumpiness # calculate smoothness by inverting bumpiness

		heuristic_value = (availableCells * availableCellsWeight) + (mono * monoWeight) + (smoothness * smoothWeight)

		return (None, heuristic_value)

	# maximize - try and get to 2048 by moving up, left, down, right
	# returns: (move, utility)
	def maximize(self, grid, alpha, beta, depth, time_start):
		self.nodes_expanded += 1

		if self.isTerminalState(grid) or depth == self.MAX_DEPTH:
			return self.generateHeuristic(grid)

		(maxMove, maxUtility) = (None, NEG_INF)

		for move in grid.getAvailableMoves():
			newGrid = grid.clone()
			newGrid.move(move)
			(_, currentUtility) = self.minimize(newGrid, alpha, beta, depth+1, time_start)

			if (currentUtility > maxUtility):
				(maxMove, maxUtility) = (move, currentUtility)

			if (maxUtility >= beta or self.inBufferTime(time_start)):
				break

			if (maxUtility > alpha):
				alpha = maxUtility

		return (maxMove, maxUtility)

	# minimize - try to minimize board score by placing new tiles
	# returns: (move, utility)
	def minimize(self, grid, alpha, beta, depth, time_start):
		self.nodes_expanded += 1

		if self.isTerminalState(grid) or depth == self.MAX_DEPTH:
			return self.generateHeuristic(grid)

		(minMove, minUtility) = (None, POS_INF)

		for cell in grid.getAvailableCells():
			for value in SPAWNED_TILES_VALUES:
				newGrid = grid.clone()
				newGrid.insertTile(cell, value)
				(_, currentUtility) = self.maximize(newGrid, alpha, beta, depth+1, time_start)

				if (currentUtility < minUtility):
					minUtility = currentUtility

				if (minUtility <= alpha or self.inBufferTime(time_start)):
					break

				if (minUtility < beta):
					beta = minUtility

		return (None, minUtility)
	
	def getMove(self, grid):
		time_start = time.clock()
		(move, utility) = self.maximize(grid, NEG_INF, POS_INF, 0, time_start)
		# print("Nodes expanded: " + str(self.nodes_expanded))
		#self.nodes_expanded = 0 
		return move

		# moves = grid.getAvailableMoves()
		# return moves[randint(0, len(moves) - 1)] if moves else None