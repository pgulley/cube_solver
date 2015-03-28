##pgulley 2015
import random
import copy

#How frequently we print output	
OUTPUT_RATE = 1000000 

##tools
def move(_pos, _vec):
	for i in range(0,3):
		_pos[i] = _pos[i] + _vec[i]
	return _pos

def getTurns(direction_vector):
	turns = []
	change = range(0,3)
	if (direction_vector.count(1)==0):
		change.pop(direction_vector.index(-1))
	else:
		change.pop(direction_vector.index(1))
	for i in change:
		A = [0,0,0]
		A[i] = 1
		turns.append(A)
		B = [0,0,0]
		B[i] = -1
		turns.append(B)
	return turns;

def valid_pos(pos):
	for i in pos:
		if (i < 0 or i > 3):
			return False
	return True

#The actual constraints of the problem, recorded from the physical puzzle
#Where the bends are.
# 0 = FORWARD
# 1 = TURN
turn_seq = [1,0,0,1,1,0,1,1,
			1,0,0,1,1,0,1,1,
			0,1,1,0,1,1,1,1,
			1,1,1,1,1,0,1,0,
			1,1,1,1,1,1,0,1,
			0,0,1,1,1,0,0,0,
			1,1,0,1,1,1,1,1,
			1,1,1,1,1,0,0,1]

def starting_pos():
	return [[0,0,0],[1,0,0],[1,1,0],[1,1,1]]

def all_dirs():
	return [[0,0,1],[0,1,0],[1,0,0],[-1,0,0],[0,-1,0],[0,0,-1]]



def print_util(i):
	if(len(i))==1 and i[0] == 'fill':
		return 0
	else:
		return len(i)

def printStats(loops, steps, starting_left, turns):

	turns_stack = [print_util(i) for i in turns.values()]
	print_msg = """
==================
processing step  : {0} 
at puzzle step   : {1} 
starts left      : {2}
turn stack       : {3} """
	print(print_msg.format(loops, steps, starting_left, turns_stack))

## A demo of the path construction tools. 
import random
def random_path():
	pos = [0,0,0]
	direction = [0,0,1]
	turns = []
	path = []
	for i in turn_seq:
		if i == 0:
			pos = move(pos,direction)
		else:
			turns = getTurns(direction)
			direction = random.choice(turns)
			pos = move(pos,direction)
		path.append(copy.deepcopy(pos)) 
	return path


##The actual search
def depth_first_search_path():
	all_starting_pos = starting_pos()
	pos = all_starting_pos.pop()
	turns = {0:all_dirs()}
	direction = turns[0].pop()
	path = [copy.deepcopy(pos)]
	steps = 0
	loops = 0
	max_steps = 0
	max_path = 0
	while steps < 64:# and loops < 100000: ##(Incase we want to limit for testing)
		loops += 1

		if(loops%OUTPUT_RATE==0):
			printStats(loops, steps, len(all_starting_pos), turns)

		if turn_seq[steps] == 1 and steps != 0: 
			if((steps not in turns) or len(turns[steps]) == 0): 
				turns[steps] = getTurns(direction)
				direction = turns[steps].pop()
		new_pos = move(pos, direction)
		##If pos doesn't overlap and is in cube
		if path.count(new_pos) == 0 and valid_pos(new_pos): 
			pos = new_pos
			path.append(copy.deepcopy(pos))
			steps += 1
			if(steps> max_steps):
				max_steps += 1
				max_path = path
		else:  
			while (steps >=0 ) and (turn_seq[steps]==0 or turns[steps][0]== 'fill'):
				#go backwards until we see a fork with untried turns
				if((steps in turns) and (turns[steps][0]=='fill')):
					turns[steps].pop()
				path.pop(steps)
				steps -= 1
			if steps >= 0:
				#try another direction
				direction = turns[steps].pop()
				#if no directions are left, mark as empty
				if(len(turns[steps]) == 0):
					turns[steps] = ['fill']
				pos = copy.deepcopy(path[-1])
			else:
				if(len(all_starting_pos)>0):
					pos = all_starting_pos.pop()
					path = [copy.deepcopy(pos)]
					turns = {0:all_dirs()}
					direction = turns[0].pop()
					steps = 0
				else:
					print("we've come to an early end again, my friends")
					output = open("cube_puzzle_farthest.txt", "w")
					output.write(str(max_path))
					output.write("\n")
					output.write(str(max_steps))
					output.close()

	print("The final path: ")
	print path
	print("writing to file")
	output = open("cube_puzzle_solution.txt", "w");
	output.write(str(path))
	output.close()


def main():
	print("Searching...")
	depth_first_search_path()

if __name__ == "__main__":
    main()




