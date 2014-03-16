import random
import pygame, sys
from pygame.locals import *
from optparse import OptionParser

#options
parser = OptionParser()
parser.add_option('-w', '--width',
					dest='width', default=1000,
					help='The width of the panel.')
parser.add_option('-f', '--fps',
					dest='fps', default=10,
					help='The frames per second.')
parser.add_option('-l', '--length',
					dest='height', default=1000,
					help='The length (height) of the panel.')
parser.add_option('-s', '--cell_size',
					dest='cell_size', default=10,
					help='The size of each individual cell.')
parser.add_option('-r', '--rule_number', 
					dest='rule_number', default=224,
					help='The Wolfram rule number.')
(options, args) = parser.parse_args()

#setting variables from options
fps = int(options.fps)
width = int(options.width)
height = int(options.height)
cell_size = int(options.cell_size)
rule_number = int(options.rule_number)

#other fixed variables
cwidth = width/cell_size
cheight = height/cell_size
black = (0, 0, 0)
white = (255,255,255)
gray = (40, 40, 40)
panel = pygame.display.set_mode((width, height))

#draws the grid on the panel
def drawGrid():
	for x in range(0, width, cell_size):
		pygame.draw.line(panel, gray, (x, 0), (x, height))
	for y in range(0, height, cell_size):
		pygame.draw.line(panel, gray, (0, y), (width, y))

#creates a grid of all dead (0) cells		
def blankGrid():
	grid = {}
	for y in range (cheight):
		for x in range (cwidth):
			grid[x,y] = 0
	return grid

#sets each cell to alive (1) or dead (0)
def randomStates(cell_states):
	#randomly sets states
	"""for i in cell_states:
		cell_states[i] = random.randint(0,1)"""
		
	#manually sets states
	#pg229a
	"""cell_states[28,28] = 1
	cell_states[28,29] = 1
	cell_states[28,30] = 1
	cell_states[28,32] = 1
	cell_states[29,28] = 1
	cell_states[29,29] = 1
	cell_states[29,30] = 1
	cell_states[29,31] = 1
	cell_states[29,32] = 1
	cell_states[30,28] = 1
	cell_states[30,29] = 1
	cell_states[30,32] = 1
	cell_states[31,32] = 1
	cell_states[32,28] = 1
	cell_states[32,29] = 1
	cell_states[32,30] = 1"""
	
	#pg229b
	"""cell_states[30,30] = 0
	cell_states[30,28] = 1
	cell_states[30,31] = 1
	cell_states[31,29] = 1
	cell_states[32,29] = 1
	cell_states[32,31] = 1
	cell_states[32,32] = 1
	cell_states[29,29] = 1
	cell_states[29,31] = 1
	cell_states[29,32] = 1
	cell_states[28,31] = 1
	cell_states[28,32] = 1"""
	
	#pg230c
	cell_states[28,28] = 1
	cell_states[28,30] = 1
	cell_states[28,31] = 1
	cell_states[28,32] = 1
	cell_states[29,28] = 1
	cell_states[29,29] = 1
	cell_states[29,30] = 1
	cell_states[29,31] = 1
	cell_states[29,32] = 1
	cell_states[30,29] = 1
	cell_states[30,31] = 1
	cell_states[30,32] = 1
	cell_states[31,29] = 1
	cell_states[31,30] = 1
	cell_states[31,31] = 1
	cell_states[31,32] = 1
	cell_states[32,28] = 1
	cell_states[32,31] = 1
	cell_states[32,32] = 1
	return cell_states

#colors the living cells black and the dead cells white	
def colorLiving(i, cell_states):
	x = i[0]
	y = i[1]
	y = y * cell_size
	x = x * cell_size
	if cell_states[i] == 0:
		pygame.draw.rect(panel, white, (x, y, cell_size, cell_size))
	if cell_states[i] == 1:
		pygame.draw.rect(panel, black, (x, y, cell_size, cell_size))
	return None

#counts how many living neighbors a cell has
def neighborCount (i, cell_states):
	neighbors = 0
	for x in range (-1,2):
		for y in range (-1,2):
			checkCell = (i[0] + x, i[1] + y)
			if checkCell[0] < cwidth and checkCell[0] >= 0:
				if checkCell[1] < cheight and checkCell[1] >= 0:
					if cell_states[checkCell] == 1:
						if x == 0 and y == 0:
							neighbors += 0
						else:
							neighbors += 1
	return neighbors

#takes the rule number and makes it binary
def toBinary(int):
	binary = []
	for i in xrange(17,-1,-1):
		binary.append((int & 2**i) >> i)
	return binary
	
#creates the next generation of cells
def gen (cell_states):
	rule = toBinary(rule_number)
	#print rule
	newGen = {}
	for i in cell_states:
		neighbors = neighborCount(i, cell_states)
		if cell_states[i] == 1:
			newGen[i] = rule[17 - (2*neighbors +1)]
		elif cell_states[i] == 0:
			newGen[i] = rule[17 - (2*neighbors)]
	return newGen
	
def main():
	
	#initializes pygame
	pygame.init()
	
	#creates a clock for how often to update the display
	fpsclock = pygame.time.Clock()
	
	#sets the pygame caption
	pygame.display.set_caption('CA')

	panel.fill(white)
	
	cell_states = blankGrid()
	cell_states = randomStates(cell_states)
	
	
	for i in cell_states:
		colorLiving(i, cell_states)
	
	drawGrid()
	pygame.display.update()
	
	
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		cell_states = gen(cell_states)
		
		for i in cell_states:
			colorLiving(i, cell_states)
		
		drawGrid()
		pygame.display.update()
		fpsclock.tick(fps)
	
if __name__ == '__main__':
	main()
