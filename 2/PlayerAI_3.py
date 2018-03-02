from random import randint
from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):

	# returns: (state, utility)
	def maximize(grid):
		if TERMINAL_TEST(grid):
			return <None, EVAL(state)>

		<maxChild, maxUtility = <NULL, -infinity>

		for child in state.children():
			<_, utility> = MINIMIZE(child)

			if (utility > maxUtility):
				<maxChild, maxUtility> = <child, utility>

		return <maxChild, maxUtility>

	def minimize(grid):
		if TERMINAL_TEST(grid):
			return (None, EVAL(state))

		<minChild, minUtility = <NULL, infinity>

		for child in state.children():
			<_, utility> = MAXIMIZE(child)

			if (utility < minUtility):
				<minChild, minUtility> = <child, utility>

		return <minChild, minUtility>


	def getMove(self, grid):
		moves = grid.getAvailableMoves()

		# Moves: UP, DOWN, LEFT, RIGHT
		return moves[randint(0, len(moves) - 1)] if moves else None