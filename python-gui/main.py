from Slider import Slider
from Button import Button
from InputBox import InputBox
from CheckBox import CheckBox
import pygame, math, sys, os
from IPython import embed
import Colors as c
from Config import Config
from random import random
import src.bridge as bdg
import copy
import shutil
pygame.init()

X = 1200  # screen width
Y = 600  # screen height
data_path = '/data/demo/csvdata/'
weights_path = '/data/src/weights/'
tensor_path = '/data/src/tensorboard/'

def drawGrid():
	size=20

	height = maze_y.val*size
	width = maze_x.val*size

	grid = pygame.surface.Surface((width, height))
	for i in range(0,maze_x.val):
		for j in range(0, maze_y.val):

			if [i,j] in walls:
				pygame.draw.rect(grid, c.GREY, [i*size, j*size, size, size])
			elif [i,j] == finalstate:
				pygame.draw.rect(grid, c.COLOR_ACTIVE, [i*size, j*size, size, size])
			elif [i,j] == initstate:
				pygame.draw.rect(grid, c.CYAN, [i*size, j*size, size, size])
			else:
				pygame.draw.rect(grid, c.WHITE, [i*size, j*size, size, size], 1)

	screen.blit(grid, (450, 60))

def loadEnv(env):
	config.loadEnvironment(env)
	guiCopyValues()
	for box in input_boxes:
		box.txt_surface = box.font.render(box.text, True, box.color)

def drawEnvironment():
	env_x = 900
	env_y = 50
	font = pygame.font.SysFont("Segoe Print", 30)
	tenv = font.render("ENVIRONMENTS", True, (255, 255, 255))
	screen.blit(tenv, (env_x, env_y))

def showForm():
	string1 = ["Version", "Iterations", "Tensorboard", "Num. Walls", "Visible Radius", "Save weights", "Save freq.", "Normal reward",
	"Min wall", "Max wall"]
	string2 = ["Done reward", "Edge value", "Num. Agents", "Eps. max", "Eps. min", "Health", "Batch Size", "Variance",
	"% of Selection", "Partial Observability", "Seed"]

	text1=[]
	text2=[]

	step = 33
	for i,s in enumerate(string1):
		text1.append(font.render(s, True, (255, 255, 255)))
		screen.blit(text1[i], (25, step*i + 200))
	for i,s in enumerate(string2):
		text2.append(font.render(s, True, (255, 255, 255)))
		screen.blit(text2[i], (220, step*i + 200))



font = pygame.font.SysFont("Verdana", 18)
screen = pygame.display.set_mode((X, Y))


maze_x = Slider(screen, "Maze X", 11, 20, 3, 25)
maze_y = Slider(screen, "Maze Y", 11, 20, 3, 225)
slides = [maze_x,maze_y]

x_alg = 75
step = 80
y_alg = 175
algorithm = "DQN"

def clearGrid(args):
	global walls, initstate, finalstate
	walls.clear()
	initstate = []
	finalstate = []

def generalActions(args):
	global counter_files
	if args == 'SAVE':
		response = config.saveEnvironment()
		if response:
			exists = False
			for e in env_buttons:
				if e.txt == config.version:
					exists = True
			if not exists:
				env_buttons.append(Button(screen, config.version, (env_x_files + 64, step_files*(counter_files+1) + env_y_files), loadEnv, size=(200,32), font_size=25))
			counter_files += 1
	elif args == 'TRAIN':
        if config.saveweights and os.exists(os.path.join(weights_path, config.alg, config.version)):
            print("Weights already exist for this experiment.")
        elif config.tensorboard and os.exists(os.path.join(tensor_path, config.alg, config.version)):
            print("Tensorboard logs already exist for this experiment.")
        else:
    		conf = config.getJSONData()
    		new_dict = copy.deepcopy(conf)
    		bdg.train(new_dict)
	elif args == 'EVAL':
        if os.exists(os.path.join(data_path, config.alg, config.version)):
            print("CSV files already exist for this experiment.")
        else:
    		conf = config.getJSONData()
    		new_dict = copy.deepcopy(conf)
    		print(new_dict)
    		bdg.eval(new_dict)
	elif args == 'DEL':
		for e in env_buttons:
			if e.txt == config.version and e.hit:
				config.removeEnvironment()
				env_buttons.remove(e)

	elif args == '3D':
		if os.exists(os.path.join(data_path, self.alg, 'current')):
			shutil.rmtree(os.path.join(data_path, self.alg, 'current'))
		os.mkdir(os.path.join(data_path, self.alg, env))
		shutil.copytree(os.path.join(data_path, self.alg, self.version), os.path.join(data_path, self.alg, 'current'))


def updateAlg(alg):
	version.text = alg + '.' + version.text.split('.')[1] + '.' + version.text.split('.')[2]
	version.txt_surface = version.font.render(version.text, True, version.color)


initx = 490
inity = 35
step = 80
reset = Button(screen, "Reset", (initx, inity), clearGrid)
wallb = Button(screen, "Walls", (initx + step, inity), lambda a: None)
initb = Button(screen, "Init State", (initx + 2*step, inity), lambda a: None)
finalb = Button(screen, "Final State", (initx + 3*step, inity), lambda a: None)
cells = [wallb, initb, finalb]
drawing = "Walls"
wallb.hit = True

dqn = Button(screen, "DQN", (x_alg, y_alg), updateAlg)
ga = Button(screen, "GA", (x_alg+step, y_alg), updateAlg)
rwb = Button(screen, "PGM", (x_alg+2*step, y_alg), updateAlg)
a2c = Button(screen, "A2C", (x_alg+3*step, y_alg), updateAlg)
algorithms = [dqn,ga, rwb, a2c]
dqn.hit = True

env_buttons = []
files = os.listdir('../envs')
env_x_files = 930
env_y_files = 75
step_files = 32

# Initialize i just in case there are no envs
i=-1
for i,f in enumerate(files):
	env_buttons.append(Button(screen, f.split('.json')[0], (env_x_files + 64, step_files*(i+1) + env_y_files), loadEnv, size=(200,32), font_size=25))

counter_files = i + 1


input_boxes = []
step = 33

xcol1 = 120
version = InputBox(screen, xcol1, step*0 + 200, 50, step-10, "DQN.0.0")
iterations = InputBox(screen, xcol1, step*1 + 200, 50, step-10, "10000")
numwalls = InputBox(screen, xcol1, step*3 + 200, 50, step-10, "15")
visibleRad = InputBox(screen, xcol1, step*4 + 200, 50, step-10, "1")
savefreq = InputBox(screen, xcol1, step*6 + 200, 50, step-10, "1000")
normal_reward = InputBox(screen, xcol1, step*7 + 200, 50, step-10, "-0.04")
min_wall = InputBox(screen, xcol1, step*8 + 200, 50, step-10, "-1")
max_wall = InputBox(screen, xcol1, step*9 + 200, 50, step-10, "0")
tensorboard = CheckBox(screen, (xcol1+20, step*2+205))
saveweights = CheckBox(screen, (xcol1+20, step*5+205))

xcol2 = 320
done_reward = InputBox(screen, xcol2, step*0 + 200, 50, step-10, "10")
edge_value = InputBox(screen, xcol2, step*1 + 200, 50, step-10, "-1")
numAgents = InputBox(screen, xcol2, step*2 + 200, 50, step-10, "1")
epsmax = InputBox(screen, xcol2, step*3 + 200, 50, step-10, "0.7")
epsmin = InputBox(screen, xcol2, step*4 + 200, 50, step-10, "0.0001")
health = InputBox(screen, xcol2, step*5 + 200, 50, step-10, "20")
batch_size = InputBox(screen, xcol2, step*6 + 200, 50, step-10, "1000")
variance = InputBox(screen, xcol2, step*7 + 200, 50, step-10, "0.03")
posel = InputBox(screen, xcol2, step*8 + 200, 50, step-10, "0.05")
po = CheckBox(screen, (xcol2+30, step*9+205))
seed = InputBox(screen, xcol2, step*10 + 200, 50, step-10, "0")


input_boxes = [version, iterations, numwalls, visibleRad, savefreq, normal_reward, min_wall, max_wall,
	done_reward, edge_value, numAgents, epsmax, epsmin, health, batch_size, variance, posel, seed]

checkboxes = [tensorboard, saveweights, po]

walls = []
initstate = []
finalstate = []
walls_values = []


# SAVE TRAIN EVAL BUTTONS
initx = 400
inity = 520
step = 100
font_size = 25
save = Button(screen, "SAVE", (initx + step, inity), generalActions, size=(80,50), font_size=font_size)
train = Button(screen, "TRAIN", (initx + 2*step, inity), generalActions,size=(80,50), font_size=font_size)
eval = Button(screen, "EVAL", (initx + 3*step, inity), generalActions,size=(80,50), font_size=font_size)
delete = Button(screen, "DEL", (initx + 4*step, inity), generalActions,size=(80,50), font_size=font_size)
threed = Button(screen, "3D", (initx + 5*step, inity), generalActions,size=(80,50), font_size=font_size)
actions = [save, train, eval, delete, threed]

# Function to handle button clicks for groups of buttons where only one
# at the same time can be selected
def oneSelectedButtons(buttons, pos):
	for button in buttons:
		if button.rect.collidepoint(pos):
			button.call_back()
			button.hit = not button.hit
			for b in buttons:
				if not b==button:
					b.hit = False

# Function to handle type of cells in the grid
def updateCells(x,y):
	global walls, finalstate, initstate, cells

	x_ = int((x-450)/20)
	y_ = int((y-60)/20)

	if x_ < maze_x.val and y_ < maze_y.val and x_ >= 0 and y_ >= 0:
		if [x_,y_] in walls:
			index = walls.index([x_,y_])
			walls.remove([x_,y_])
			del walls_values[index]
		elif [x_,y_] == finalstate:
			finalstate = []
		elif [x_,y_] == initstate:
			initstate = []
		else:
			for button in cells:
				if button.hit and button.txt == "Walls":
					walls.append([x_,y_])
					walls_values.append(random()*(float(config.max_wall)-float(config.min_wall)) + float(config.min_wall))
				elif button.hit and button.txt == "Init State":
					initstate = [x_,y_]
				elif button.hit and button.txt == "Final State":
					finalstate = [x_,y_]

# When we want to copy values from the Config to the GUI we'll make use of this function
def guiCopyValues():
	global version, tensorboard, numwalls, saveweights, po, iterations, savefreq, batch_size, seed
	global health, done_reward, visibleRad, min_wall, max_wall, edge_value, normal_reward, walls_values
	global numAgents, maze_x, maze_y, epsmax, epsmin, variance, posel, walls, finalstate, initstate

	for a in algorithms:
		if a.txt == config.alg:
			a.hit = True
		else:
			a.hit = False

	version.text = config.version
	tensorboard.hit = config.tensorboard
	saveweights.hit = config.saveweights
	po.hit = config.po

	iterations.text = config.iterations
	numwalls.text = config.numwalls
	savefreq.text = config.savefreq
	batch_size.text = config.batch_size
	health.text = config.health
	done_reward.text = config.done_reward
	visibleRad.text = config.visibleRad
	min_wall.text = config.min_wall
	max_wall.text = config.max_wall
	edge_value.text = config.edge_value
	normal_reward.text = config.normal_reward
	numAgents.text = config.numAgents

	maze_y.val = config.height
	maze_x.val = config.width

	epsmax.text = config.epsmax
	epsmin.text = config.epsmin

	variance.text = config.variance
	posel.text = config.pos

	walls = config.walls
	finalstate = config.finalstate
	initstate = config.initstate
	walls_values = config.walls_values
	seed.text = config.seed

# When we want to update the values of Config with the custom values from the GUI
# we'll make use of this function
def copyValues():
	config.version = version.text
	for a in algorithms:
		if a.hit:
			config.alg = a.txt
			break
	config.tensorboard = tensorboard.hit
	config.saveweights = saveweights.hit
	config.po = po.hit

	config.iterations = iterations.text
	config.numwalls = numwalls.text
	config.savefreq = savefreq.text
	config.batch_size = batch_size.text
	config.health = health.text
	config.done_reward = done_reward.text
	config.visibleRad = visibleRad.text
	config.min_wall = min_wall.text
	config.max_wall = max_wall.text
	config.edge_value = edge_value.text
	config.normal_reward = normal_reward.text
	config.numAgents = numAgents.text
	config.height = maze_y.val
	config.width = maze_x.val

	config.epsmax = epsmax.text
	config.epsmin = epsmin.text

	config.variance = variance.text
	config.pos = posel.text

	config.walls = walls
	config.finalstate = finalstate
	config.initstate = initstate
	config.walls_values = walls_values
	config.seed = seed.text


config = Config()
guiCopyValues()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			x,y = pos
			updateCells(x,y)
			for s in slides:
				if s.button_rect.collidepoint(pos):
					s.hit = True
			if reset.rect.collidepoint(pos):
				reset.call_back()
			for a in actions:
				if a.rect.collidepoint(pos):
					a.call_back()
			for group in [cells, algorithms, env_buttons]:
				oneSelectedButtons(group, pos)
			for button in checkboxes:
				if button.rect.collidepoint(pos):
					button.hit = not button.hit
		elif event.type == pygame.MOUSEBUTTONUP:
			for s in slides:
				s.hit = False
		for box in input_boxes:
			box.handle_event(event)

	# Update screen
	screen.fill(c.BLACK)
	for box in input_boxes:
		box.update()
	for s in slides:
		if s.hit:
			s.move()
	for obj in [slides, actions, checkboxes, cells, algorithms, env_buttons, input_boxes]:
		for t in obj:
			t.draw()
	drawGrid()
	showForm()
	drawEnvironment()
	reset.draw()
	copyValues()

	pygame.display.flip()
