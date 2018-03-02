from random import randint
from BaseAI_3 import BaseAI
import time

NEG_INF = float("-inf")
POS_INF = float("inf")
SPAWNED_TILES_VALUES = [2,4]
TIME_BUFFER = 0.05 # number of seconds remaining at which we end the depth-first traversal

class PlayerAI(BaseAI):

	# is this grid a terminal state?
	def isTerminalState(self, grid):
		return len(grid.getAvailableMoves()) == 0 

	# are we in the buffer time?
	def inBufferTime(self, start_time):
		time_elapsed = time.clock() - start_time
		time_remaining = 0.25 - time_elapsed
		return time_remaining < TIME_BUFFER

	def generateHeuristic(self, grid):
		return (None, len(grid.getAvailableCells()))

	# maximize - try and get to 2048 by moving up, left, down, right
	# returns: (move, utility)
	def maximize(self, grid, alpha, beta, depth, time_start):

		if self.isTerminalState(grid) or depth == 4:
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

		if self.isTerminalState(grid) or depth == 4:
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
		time_elapsed = time.clock() - time_start
		return move

		# moves = grid.getAvailableMoves()
		# return moves[randint(0, len(moves) - 1)] if moves else None