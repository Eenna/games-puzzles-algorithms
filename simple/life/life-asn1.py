#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid
cole stevenson               crsteven
Duncan Krammer               krammer
Shridhar Patel               spatel1
Colman Koivisto              koivisto
Khrystina Vrublevska         vrublevs

#############################################
# Your answer to question 1-a:

a glider needs a grid that's unbounded for the whole simulation

.*.
..*
***

this is because the glider doens't die out and constantly moves
across the grid

#############################################
# Your answer to question 1-b:

a gosper glider gun is a pattern whose number of cells alive at any one 
time is unbounded

.......................**.........**..
......................*.*.........**..
**.......**...........**..............
**......*.*...........................
........**......**....................
................*.*...................
................*.....................
...................................**.
...................................*.*
...................................*..
......................................
......................................
........................***...........
........................*.............
.........................*............

that is because the gun shoots out gliders and those gliders keep upping
the live cell count indefinitely

#############################################
# Your answer to question 2:

For starters, life-np uses the numpy array instaad of the row array, which 
makes the indexing easier. The num-nbrs function from life.py isnt' needed
in life-np because it's functionality is merged with next state. 

Concerning the "infinity" of the grid in life.py: the grid isn't actually 
infinite. The file has a pad function that adds new rows and columns anytime
the pattern reaches the edge.

Having a guarded board simplifies num_nbrsbecause the function doesn't have 
to check for the edges of the board on each iteration. There is no need to
pass the board dimentions as arguments to it.

#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:

..........*...
...........*..
.........***..
..............
..............

iterations 260

#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
	B = []
	print(sys.argv[1])
	with open(sys.argv[1]) as f:
		for line in f:
			B.append(line.rstrip().replace(' ', ''))
		rows, cols = len(B), len(B[0])
		for j in range(1, rows):
			assert(len(B[j]) == cols)
		return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
	A = np.zeros((r, c), dtype=np.int8)
	for j in range(r):
		for k in range(c):
			if B[j][k] == ACH:
				A[j, k] = ALIVE
	return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
	N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
	for j in range(r):
		for k in range(c):
			if A[j][k] == ALIVE:
				N[j+t, k+t] = ALIVE
	return N, r+2*t, c+2*t


def print_array(A, r, c):
	print('')
	for j in range(r):
		out = ''
		for k in range(c):
			out += ACH if A[j, k] == ALIVE else DCH
		print(out)


def show_array(A, r, c):
	for j in range(r):
		line = ''
		for k in range(c):
			line += str(A[j, k])
		print(line)
	print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
	N = np.zeros((r, c), dtype=np.int8)
	changed = False
	for j in range(r):
		for k in range(c):
			num = 0
			if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
				num += 1
			if j > 0 and A[j-1, k] == ALIVE:
				num += 1
			if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
				num += 1
			if k > 0 and A[j, k-1] == ALIVE:
				num += 1
			if k < c-1 and A[j, k+1] == ALIVE:
				num += 1
			if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
				num += 1
			if j < r-1 and A[j+1, k] == ALIVE:
				num += 1
			if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
				num += 1
			if A[j, k] == ALIVE:
				if num > 1 and num < 4:
					N[j, k] = ALIVE
				else:
					N[j, k] = DEAD
					changed = True
			else:
				if num == 3:
					N[j, k] = ALIVE
					changed = True
				else:
					N[j, k] = DEAD
	return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""


def next_state2(A, r, c):
	N = np.zeros((r, c), dtype=np.int8)
	changed = False
	for j in range(r):
		for k in range(c):
			num = num_nbrs2(A, r, j, c, k)
			if A[j, k] == ALIVE:
				if num > 1 and num < 4:
					N[j, k] = ALIVE
				else:
					N[j, k] = DEAD
					changed = True
			else:
				if num == 3:
					N[j, k] = ALIVE
					changed = True
				else:
					N[j, k] = DEAD
	return N, changed
#############################################


#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""


def num_nbrs2(A, r, j, c, k):
	num = 0
	if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
		num += 1
	if j > 0 and A[j-1, k] == ALIVE:
		num += 1
	if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
		num += 1
	if k > 0 and A[j, k-1] == ALIVE:
		num += 1
	if k < c-1 and A[j, k+1] == ALIVE:
		num += 1
	if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
		num += 1
	if j < r-1 and A[j+1, k] == ALIVE:
		num += 1
	if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
		num += 1
	return num
	
#############################################


#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""


def next_state_torus(A, r, c):
	N = np.zeros((r, c), dtype=np.int8)
	changed = False
	for j in range(r):
		for k in range(c):
			num = num_nbrs_torus(A, r, j, c, k)
			if A[j, k] == ALIVE:
				if num > 1 and num < 4:
					N[j, k] = ALIVE
				else:
					N[j, k] = DEAD
					changed = True
			else:
				if num == 3:
					N[j, k] = ALIVE
					changed = True
				else:
					N[j, k] = DEAD
	return N, changed
#############################################

#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""
def num_nbrs_torus(A, r, j, c, k): 
	""" Counts number of neighbours for a torus.

	Args:
		A: the numpy board
		r: number of rows in the board
		j: current row of the cell in the iteration
		c: number of columns in the board
		k: current column of the cell in the iteration
	
	Returns:
		num: the number of neighbours
	"""
	num = 0
	r = r - 1 # to account for off by one errors
	c = c - 1
	if j == 0:
		if k == 0:
			# top left corner edge case
			if A[r, c] == ALIVE:
				num += 1
			if A[j, c] == ALIVE:
				num += 1
			if A[j+1, c] == ALIVE:
				num += 1

			if A[r, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j+1, k+1] == ALIVE:
				num += 1

		if k > 0 and k < c:
			# top row minus corners edge cases
			if A[r, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j+1, k-1] == ALIVE:
				num += 1

			if A[r, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j+1, k+1] == ALIVE:
				num += 1
		
		if k == c:
			# top right corner edge case
			if A[r, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j+1, k-1] == ALIVE:
				num += 1

			if A[r, 0] == ALIVE:
				num += 1
			if A[j, 0] == ALIVE:
				num += 1
			if A[j+1, 0] == ALIVE:
				num += 1
		
		if A[j+1,k] == ALIVE:
			num += 1
		if A[r, k] == ALIVE:
			num += 1

	if j > 0 and j < r:
		if k == 0:
			# left side minus corners edge cases
			if A[j-1, c] == ALIVE:
				num += 1
			if A[j, c] == ALIVE:
				num += 1
			if A[j+1, c] == ALIVE:
				num += 1

			if A[j-1, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j+1, k+1] == ALIVE:
				num += 1

		if k > 0 and k < c:
			# center
			if A[j-1, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j+1, k-1] == ALIVE:
				num += 1

			if A[j-1, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j+1, k+1] == ALIVE:
				num += 1
		
		if k == c:
			# right side minus corners edge cases
			if A[j-1, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j+1, k-1] == ALIVE:
				num += 1

			if A[j-1, 0] == ALIVE:
				num += 1
			if A[j, 0] == ALIVE:
				num += 1
			if A[j+1, 0] == ALIVE:
				num += 1
		
		if A[j+1,k] == ALIVE:
			num += 1
		if A[j-1, k] == ALIVE:
			num += 1


	if j == r:
		if k == 0:
			# bottom left corner edge cases
			if A[j-1, c] == ALIVE:
				num += 1
			if A[j, c] == ALIVE:
				num += 1
			if A[0, c] == ALIVE:
				num += 1

			if A[0, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j-1, k+1] == ALIVE:
				num += 1

		if k > 0 and k < c:
			# bottom row minus corners edge cases
			if A[0, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j-1, k-1] == ALIVE:
				num += 1

			if A[0, k+1] == ALIVE:
				num += 1
			if A[j, k+1] == ALIVE:
				num += 1
			if A[j-1, k+1] == ALIVE:
				num += 1
		
		if k == c:
			# bottom right corner edge cases
			if A[0, k-1] == ALIVE:
				num += 1
			if A[j, k-1] == ALIVE:
				num += 1
			if A[j-1, k-1] == ALIVE:
				num += 1

			if A[0, 0] == ALIVE:
				num += 1
			if A[j, 0] == ALIVE:
				num += 1
			if A[j-1, 0] == ALIVE:
				num += 1
		
		if A[j-1,k] == ALIVE:
			num += 1
		if A[0, k] == ALIVE:
			num += 1
	
	return num
#############################################


"""
input, output
"""

pause = 0.0

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
	itn = 0
	B, r, c = get_board()
	print(B)
	X = convert_board(B, r, c)
	A, r, c = expand_grid(X, r, c, 0)
	print_array(A, r, c)
	while itn <= max_itn:
		sleep(pause)
		newA, delta = next_state2(A, r, c)
		if not delta:
			break
		itn += 1
		A = newA
		print_array(A, r, c)
	print('\niterations', itn)


def main():
	interact(259)


if __name__ == '__main__':
	main()
