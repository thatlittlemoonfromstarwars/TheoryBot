import pygame, sys
import pygame_textinput
from pygame.locals import QUIT
from pygame import gfxdraw

# global constants
WIDTH = 1000
HEIGHT = 200
WINDOW_SIZE = (WIDTH, HEIGHT)
TREBLE_SIZE = (70,70)
NOTE_SPACING = (TREBLE_SIZE[1]-23)/8
STAFF_POS = (10,20)
BLACK = (0,0,0)

# global variables
notesOnStaff = []

# setup for pygame
pygame.init()
pygame.font.init()
FONT = pygame.font.Font("Roboto/Roboto-Medium.ttf",15)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Theory Bot')
# https://replit.com/talk/learn/Pygame-Tutorial/143782

# for text input
textinput = pygame_textinput.TextInputVisualizer()
# https://github.com/Nearoo/pygame-text-input
clock = pygame.time.Clock()

allNotes = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
accidentals = [0,-5,2,-3,4,-1,6,1,-4,3,-2,5]
orderOfSharps = ['F','C','G','D','A','E','B']

# integers in lists represent the steps between notes
# 1 represents a half step, 2 represents a whole step, and so on
# scales
major = [2,2,1,2,2,2,1]
minor = [2,1,2,2,1,2,2]
pentatonicM = [2,2,3,2,3]
pentatonicm = [3,2,2,3,2]
blues = [3,2,1,1,3,2]

# chords
maj = [4,3]
maj7 = [4,3,4]
maj9 = [4,3,4,3]
maj11 = [4,3,4,3,3]

min = [3,4]
min7 = [3,4,3]
min9 = [3,4,3,4]
min11 = [3,4,3,4,3]

dim = [3,3]
dom7 = [4,3,3]
dom9 = [4,3,3,4]
sus2 = [2,5]
sus4 = [5,2]
aug = [4,4]

def findRoot(userin):
	# seperates user input into root note and modifier
	if allNotes.count(userin[0]) == 0:
		return -1, -1
		
	if userin.find('b') == 1:
		ind = allNotes.index(userin[0])-1
		if ind == -1:
			ind = 11
		return allNotes[ind], userin[2:]
		
	elif userin.find('#') == 1:
		ind = allNotes.index(userin[0])+1
		if ind == 12:
			ind = 0
		return allNotes[ind], userin[2:]
		
	else:
		return userin[0], userin[1:]


def printAccidentals(root):
	# to print accidentals in a scale
	acc = accidentals[allNotes.index(root)]
	if acc == 0:
		print(root, " has no sharps or flats.")
	elif acc == -1:
		print(root, " has 1 flat. It is Bb.")
	elif acc == 1:
		print(root, " has 1 sharp. It is F#.")
	elif acc < -1:
		acc *= -1
		flats = ""
		for x in range(acc):
			if x == acc-1:
				flats += "and " + orderOfSharps[6-x] + "b."
			else:
				flats += orderOfSharps[6-x] + "b, "
		print(root, " has ", acc, " flats. They are", flats)

	else:
		sharps = ""
		for x in range(acc):
			if x == acc-1:
				sharps += "and " + orderOfSharps[x] + "#."
			else:
				sharps += orderOfSharps[x] + "#, "
		if acc == 1:
			print(root, " has ", acc, " sharp. It is", sharps)
		else:
			print(root, " has ", acc, " sharps. They are", sharps)
			

def printScale(root, steps):
	# prints the note names of the notes in the scale
	ind = allNotes.index(root)
	if accidentals[ind] > 0:
		sharpScale = True
	else:
		sharpScale = False
		
	for x in range(len(steps)+1):
		note = allNotes[ind%12]
		if sharpScale and note.count('b') == 1:
			note = allNotes[ind%12-1] + "#"
			
		print(note, end=" ")

		ind += steps[x%(len(steps))]
		
	pygame.display.update()
	
def printMenu():
	print("-----Scales-----")
	print("M - Major")
	print("m - Minor")
	print("pM - Pentatonic Major")
	print("pm - Pentatonic Minor")
	print("B - blues")
	print()
	print("-----Chords-----")
	print("maj - Major")
	print("maj7 - Major 7")
	print("maj9 - Major 9")
	print("maj11 - Major 11")
	print("min - Minor")
	print("min7 - Minor 7")
	print("min9 - Minor 9")
	print("min11 - Minor 11")
	print("dim - Diminished")
	print("dom7 - Dominant 7")
	print("dom9 - Dominant 9")
	print("sus2 - Sus2")
	print("sus4 - Sus4")
	print("aug - Augmented")
	print()
	
	
def chooseType(mod):
	# returns the corresponding step list, taking the
	# modifier as input
	match mod:	
		case "":
			return maj
		case "M":
			return major
		case "m":
			return minor
		case "pM":
			return pentatonicM
		case "pm":
			return pentatonicm
		case "B":
			return blues
		case "maj":
			return maj
		case "maj7":
			return maj7
		case "maj9":
			return maj9
		case "maj11":
			return maj11
		case "min":
			return min
		case "min7":
			return min7
		case "min9":
			return min9
		case "min11":
			return min11
		case "dim":
			return dim
		case "dom7":
			return dom7
		case "dom9":
			return dom9
		case "sus2":
			return sus2
		case "sus4":
			return sus4
		case "aug":
			return aug
		case _:
			return -1
			

def chooseMode():
	# choose between single chord or chord progression
	while True:
		print("----Modes----")
		print("1. Single Chord or Scale")
		print("2. Chord progression")
		mode = int(getUserIn("Choose a mode:"))
		if mode == 1 or mode == 2:
			return mode
		else:
			print("That is not a valid mode. Please enter a valid mode.")
			print()
			

def singleChordMode():
	# prints a single chord or scale
	while True:
		userin = input("Enter scale or chord (type m to see option menu): ")
		if userin[0] == "m" or userin[0] == "M":
			printMenu()
			continue
		root, mod = findRoot(userin)
	
		# if entrance format is incorrect, reenter input
		if root == -1:
			continue

		# remove space from mod
		try:
			if mod[0] == ' ':
				mod = mod[1:]
		except:
			pass

		# get step list
		type = chooseType(mod)
		if type == -1:
			print("That is not a valid option. Please try again (type m to see option menu).")
			continue
			
		# reset screen
		SCREEN.fill("white")
		drawStaff(STAFF_POS)
		pygame.display.update()
		
		# draw scale
		drawScale(root, mod, type, 0)
		printScale(root, type)
		print()
		

def progressionMode():
	# prints a chord progression
	# select number of chords
	while True:
		numChords = input("Enter number of chords: ") # can be changed later
		try:
			numChords = int(numChords)
			break
		except:
			print("Please enter an integer.")

	# reset screen
	SCREEN.fill("white")
	drawStaff(STAFF_POS)
	pygame.display.update()
	
	chords = []
	x = 0
	
	# get chord progression from user
	while x < numChords:
		userin = input("Enter chord " + str(x+1) + " (type m to see option menu): ")
		if userin[0] == "m" or userin[0] == "M":
			printMenu()
			continue
		root, mod = findRoot(userin)
	
		# if entrance format is incorrect, reenter input
		if root == -1:
			continue
			
		# remove space from mod
		try:
			if mod[0] == ' ':
				mod = mod[1:]
		except:
			pass

		# get step list
		type = chooseType(mod)
		if type == -1:
			print("That is not a valid option. Please try again (type m to see option menu).")
			continue

		# add chord to chord list
		tempChord = [root,mod,type]
		chords.append(tempChord)
		x += 1

	# print chord list
	notePos = 0
	for temp in chords:
		print(temp[0]+temp[1])
		printScale(temp[0],temp[2])
		notePos = drawScale(temp[0],temp[1],temp[2], notePos)
		print()
		

def drawStaff(pos):
	# draws the staff
	# staff dimensions
	LEFTX = pos[0]+10
	RIGHTX = WIDTH-(pos[0]+10)
	TOPY = pos[1]+5
	BOTTOMY = pos[1]+TREBLE_SIZE[1]-17
	STAFF_SPACING = (BOTTOMY-TOPY)/4

	# draw treble clef
	trebleClef = pygame.image.load("treble clef.png")
	trebleClef = pygame.transform.smoothscale(trebleClef, TREBLE_SIZE)
	SCREEN.blit(trebleClef, pos)
	
	# draw left side vertical line
	pygame.draw.line(SCREEN, BLACK, (LEFTX,TOPY), (LEFTX,BOTTOMY))

	# draw right side vertical line
	pygame.draw.line(SCREEN, BLACK, (RIGHTX,TOPY), (RIGHTX,BOTTOMY))
		
	# draw horizontal staff lines
	for i in range(5):
		y = TOPY+STAFF_SPACING*i
		pygame.draw.line(SCREEN, BLACK, (LEFTX,y), (RIGHTX,y))
		

def drawNote(staffPos, noteName, oct, notePosX):
	# draws a single note on the staff
	# returns note position
	# calculate x position
	xPos = (staffPos[0]+10) + (WIDTH-(staffPos[0]+10)*2)/90 + (WIDTH-(staffPos[0]+10)*2)/30*(notePosX+2)
	xPos = int(xPos)
	
	# calculate y position
	# middle C is used as the reference position
	middleCY = staffPos[1] + NOTE_SPACING*11

	match noteName[0]:
		case "C":
			mult = 0
		case "D":
			mult = 1
		case "E":
			mult = 2
		case "F":
			mult = 3
		case "G":
			mult = 4
		case "A":
			mult = 5
		case "B":
			mult = 6
		case _:
			mult = -1
		
	yPos = int(middleCY - NOTE_SPACING*(mult + (oct-1)*7))

	# draw line through note if it is above or below staff
	if yPos > (staffPos[1] + NOTE_SPACING*10) or yPos < (staffPos[1] - NOTE_SPACING):
		pygame.draw.line(SCREEN, BLACK, (xPos-9,yPos), (xPos+9,yPos))
	
	# draw note
	gfxdraw.aacircle(SCREEN, xPos, yPos, 5, BLACK)
	gfxdraw.filled_circle(SCREEN, xPos, yPos, 5, BLACK)

	# draw accidental
	ACC_OFFSET = 14
	SHARP_SIZE = (40,40)
	FLAT_SIZE = (8,18)
	try:
		if noteName[1] == '#':
			# load and draw sharp symbol
			sharp = pygame.image.load("sharp.png")
			sharp = pygame.transform.smoothscale(sharp, SHARP_SIZE)
			x = int(xPos + ACC_OFFSET - SHARP_SIZE[0]/2)
			y = int(yPos-SHARP_SIZE[1]/2)
			SCREEN.blit(sharp, (x, y))
		
		elif noteName[1] == 'b':
			# load and draw flat symbol
			flat = pygame.image.load("flat.png")
			flat = pygame.transform.smoothscale(flat, FLAT_SIZE)
			x = int(xPos + ACC_OFFSET - FLAT_SIZE[0]/2)
			y = int(yPos-FLAT_SIZE[1]/2) - 3
			SCREEN.blit(flat, (x,y))
	except:
		pass

	return xPos, yPos
		

def drawScale(root, mod, steps, startingPos):
	# draws a scale or chord
	# determine whether to print sharps or flats
	ind = allNotes.index(root)
	if accidentals[ind] > 0:
		sharpScale = True
	else:
		sharpScale = False
	
	notePos = startingPos
	for x in range(len(steps)+1):
		# get note name
		note = allNotes[ind%12]

		# if sharpScale, change flat note to it's equivalent sharp note
		if sharpScale and note.count('b') == 1:
			note = allNotes[ind%12-1] + "#"

		# find octave
		if ind < 12:
			oct = 1
		else:
			oct = 2

		# draw the note
		noteCoords = drawNote(STAFF_POS, note, oct, notePos)

		# if note is first note in the scale, write the scale name the note
		if x == 0:
			printOnScreen(note+mod, (noteCoords[0] - 4, STAFF_POS[1] + NOTE_SPACING*11+5))
		
		notePos += 1
		pygame.display.update()
		
		ind += steps[x%(len(steps))]

	return notePos


def printOnScreen(text, pos):
	# print text to screen (not console)
	toPrint = FONT.render(text, True, BLACK)
	SCREEN.blit(toPrint, pos)
	pygame.display.update()
	
# Program Start

# select mode when first run
# mode = chooseMode()

def getUserIn(prompt):
	while True:
		SCREEN.fill("white")
		drawStaff(STAFF_POS)
		drawNotes()
		
		events = pygame.event.get()
		# Feed it with events every frame
		textinput.update(events)
		# Blit its surface onto the screen
		SCREEN.blit(textinput.surface, (20, HEIGHT-50))
	
		for event in events:
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
	
			if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
				return textinput.value
				
				textinput.value = ''
			# for testing
			# if event.type == pygame.MOUSEBUTTONDOWN:
			# 	print(pygame.mouse.get_pos())
	
	
		pygame.display.update()
		clock.tick(30)
	# 




mode = chooseMode()
if mode == 1:
	singleChordMode()
else:
	progressionMode()
