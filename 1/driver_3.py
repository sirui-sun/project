# arguments: <method> <board>

import sys, queue, time, heapq, math

method = sys.argv[1]
board_start = sys.argv[2]
ordered_actions = ["Up", "Down", "Left", "Right"]
start_time = time.time()

# is the current board solved?
def is_solved(board):
	return board == "0,1,2,3,4,5,6,7,8"

# can the current board be moved with the specified action?
def can_move(action, board):
	space_position = board.index('0') 
	if (action == "Up"):
		return space_position > 4
	if (action == "Down"):
		return space_position < 12
	if (action == "Left"):
		return (space_position != 0 and space_position != 6 and  space_position != 12)
	if (action == "Right"):
		return (space_position != 4 and space_position != 10 and space_position != 16)

# move the board in the specified action
def move(action, board):
	space_position = board.index('0')
	target_character = "9"
	if (action == "Up"):
		target_position = space_position - 6
	if (action == "Down"):
		target_position = space_position + 6
	if (action == "Left"):
		target_position = space_position - 2
	if (action == "Right"):
		target_position = space_position + 2
	target_character = board[target_position]
	temp_string = board.replace("0", "9")
	temp2_string = temp_string.replace(target_character, "0")
	return temp2_string.replace("9", target_character)

# find the Manhattan distance for a given board
def manhattan_distance(board):
	total_distance = 0
	idx = 0
	current_x = 1
	current_y = 1
	while (idx <= 16):
		current_char = board[idx]
		# print("current char: " + str(current_char))
		# print("\tcurrent x: " + str(current_x))
		# print("\tcurrent y: " + str(current_y))
		if current_char != "0": 
			target_xy = get_home_xy(current_char)
			target_x = target_xy[0]
			target_y = target_xy[1]
			# print("\ttarget x: " + str(target_x))
			# print("\ttarget y: "+ str(target_y))

			current_distance = math.fabs(current_x - target_x) + math.fabs(current_y - target_y)
			# print("\tthis distance: "+ str(current_distance))
			total_distance += current_distance
		idx += 2
		current_x += 1
		if (current_x) == 4: current_x = 1
		if (idx == 6 or idx == 12): current_y += 1
		
	return total_distance

def get_home_xy(ch):
	num = int(ch)
	x = 1
	y = 1
	if (num == 1 or num == 4 or num == 7): x = 2 
	if (num == 2 or num == 5 or num == 8): x = 3
	if (num == 3 or num == 4 or num == 5): y = 2 
	if (num == 6 or num == 7 or num == 8): y = 3 
	return (x,y) 

# handle a solved node - print out the outputs correctly.
def handle_solved_node(node, nodes_expanded, max_search_depth):
	solution_list = []
	current_node = node
	while (current_node.get_action() != "parent"):
		solution_list = [current_node.get_action()] + solution_list
		current_node = current_node.get_parent_node()

	f = open("output.txt", "w")
	f.write("path_to_goal: " + str(solution_list) + "\n")
	f.write("cost_of_path: " + str(len(solution_list)) + "\n")
	f.write("nodes_expanded: " + str(nodes_expanded) + "\n")	
	f.write("search_depth: " + str(len(solution_list)) + "\n")	
	f.write("max_search_depth: " + str(max_search_depth) +"\n")
	f.write("running_time: %s" % (time.time() - start_time) + "\n")
	f.write("max_ram_usage: 1")

class Node:
	def __init__(self, parent_node, action, board_state, depth):
		self.parent_node = parent_node
		self.action = action
		self.board_state = board_state
		self.depth = depth

	def __eq__(self, other):
		return self.board_state == other.board_state

	def __lt__(self, other):
		return self.get_est_total_distance() < other.get_est_total_distance()

	def get_est_total_distance(self):
		return self.get_depth() + self.get_manhattan_distance()

	def get_manhattan_distance(self):
		return manhattan_distance(self.get_board_state())

	def get_board_state(self):
		return self.board_state

	def get_action(self):
		return self.action

	def get_parent_node(self):
		return self.parent_node

	def get_depth(self):
		return self.depth

def breadth_first_search(board_start):
	frontier = queue.Queue()
	frontier.put(Node(0, "parent", board_start, 0))
	max_search_depth = 0
	seen = {}
	seen[board_start] = 1
	nodes_expanded = -1 # off set for parent

	while (not frontier.empty()):
		current_node = frontier.get()
		current_depth = current_node.get_depth()
		current_board_state = current_node.get_board_state()
		nodes_expanded += 1

		if (is_solved(current_board_state)):
			handle_solved_node(current_node, nodes_expanded, max_search_depth)
			break

	 	# add Up, Down, Left, Right neighbors
		for action in ordered_actions:
			if (can_move(action, current_board_state)):
				next_board_state = move(action, current_board_state)
				if (next_board_state not in seen): 
					frontier.put(Node(current_node, action, next_board_state, current_depth + 1))
					max_search_depth = (current_depth + 1) if (current_depth + 1) > max_search_depth else max_search_depth
					seen[next_board_state] = 1

def depth_first_search(board_start):
	frontier = []
	seen = {}
	frontier.append(Node(0, "parent", board_start, 0))
	seen[board_start] = 1
	ordered_actions.reverse()
	nodes_expanded = -1 # off set for parent
	max_search_depth = 0

	while (frontier):
		current_node = frontier.pop()
		current_depth = current_node.get_depth()
		current_board_state = current_node.get_board_state()
		nodes_expanded += 1

		if (is_solved(current_board_state)):
			handle_solved_node(current_node, nodes_expanded, max_search_depth)
			break

		# add Up, Down, Left, Right neighbors
		for action in ordered_actions:
			if (can_move(action, current_board_state)):
				next_board_state = move(action, current_board_state) 
				# skip node if either 
				if (next_board_state not in seen): 
					frontier.append(Node(current_node, action, next_board_state, current_depth + 1))
					max_search_depth = (current_depth + 1) if (current_depth + 1) > max_search_depth else max_search_depth
					seen[next_board_state] = 1

def a_star_search(board_start):
	frontier = []
	heapq.heappush(frontier, Node(0, "parent", board_start, 0))
	seen  = {}
	seen[board_start] = 1
	nodes_expanded = -1 # off set for parent
	max_search_depth = 0
	ordered_actions.reverse()

	while (frontier):
		current_node = heapq.heappop(frontier)
		current_depth = current_node.get_depth()
		current_board_state = current_node.get_board_state()
		nodes_expanded += 1

		if(is_solved(current_board_state)):
			handle_solved_node(current_node, nodes_expanded, max_search_depth)
			break

		# add Up, Down, Left, Right neighbors
		for action in ordered_actions:
			if (can_move(action, current_board_state)):
				next_board_state = move(action, current_board_state) 
				next_node = Node(current_node, action, next_board_state, current_depth + 1)
 
				if (next_board_state not in seen): 
					heapq.heappush(frontier, next_node)
					max_search_depth = (current_depth + 1) if (current_depth + 1) > max_search_depth else max_search_depth
					seen[next_board_state] = 1

if (method == "dfs"):
	depth_first_search(board_start)

if (method == "bfs"):
	breadth_first_search(board_start)

if (method == "ast"):
	a_star_search(board_start)