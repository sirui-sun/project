from random import randint
from BaseAI_3 import BaseAI

NEG_INF = float("-inf")
POS_INF = float("inf")
SPAWNED_TILES_VALUES = [2,4]

class PlayerAI(BaseAI):

	# is this grid a terminal state?
	def isTerminalState(self, grid):
		return len(grid.getAvailableMoves()) == 0 

	def generateHeuristic(self, grid):
		return (None, len(grid.getAvailableCells()))

	# maximize - try and get to 2048 by moving up, left, down, right
	# returns: (move, utility)
	def maximize(self, grid, alpha, beta, depth):
		if self.isTerminalState(grid) or depth == 4:
			return self.generateHeuristic(grid)

		(maxMove, maxUtility) = (None, NEG_INF)

		for move in grid.getAvailableMoves():
			newGrid = grid.clone()
			newGrid.move(move)
			(_, currentUtility) = self.minimize(newGrid, alpha, beta, depth+1)

			if (currentUtility > maxUtility):
				(maxMove, maxUtility) = (move, currentUtility)

			if (maxUtility >= beta):
				break

			if (maxUtility > alpha):
				alpha = maxUtility

		return (maxMove, maxUtility)

	# minimize - try to minimize board score by placing new tiles
	# returns: (move, utility)
	def minimize(self, grid, alpha, beta, depth):

		if self.isTerminalState(grid) or depth == 4:
			return self.generateHeuristic(grid)

		(minMove, minUtility) = (None, POS_INF)

		for cell in grid.getAvailableCells():
			for value in SPAWNED_TILES_VALUES:
				newGrid = grid.clone()
				newGrid.insertTile(cell, value)
				(_, currentUtility) = self.maximize(newGrid, alpha, beta, depth+1)

				if (currentUtility < minUtility):
					minUtility = currentUtility

				if (minUtility <= alpha):
					break

				if (minUtility < beta):
					beta = minUtility

		return (None, minUtility)
	
	def getMove(self, grid):
		(move, utility) = self.maximize(grid, NEG_INF, POS_INF, 0)
		return move

		# moves = grid.getAvailableMoves()
		# return moves[randint(0, len(moves) - 1)] if moves else None