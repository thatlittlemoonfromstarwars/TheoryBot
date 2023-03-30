import pygame, sys
from pygame.locals import QUIT
from pygame import gfxdraw

# setup for pygame
pygame.init()
WIDTH = 1000
HEIGHT = 700
WINDOW_SIZE = (WIDTH, HEIGHT)
TREBLE_SIZE = (70,70)
BLACK = (0,0,0)

SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# https://replit.com/talk/learn/Pygame-Tutorial/143782

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
	# to print accidentals
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
		
	print()
	
	
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

	# remove space
	try:
		if mod[0] == ' ':
			mod = mod[1:]
	except:
		pass
	
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
	while True:
		# mode select
		print("----Modes----")
		print("1. Single Chord or Scale")
		print("2. Chord progression")
		mode = int(input("Choose a mode:"))
		if mode == 1 or mode == 2:
			return mode
		else:
			print("That is not a valid mode. Please enter a valid mode.")
			print()
			

def singleChordMode():
	while True:
		# single chord
		userin = input("Enter scale or chord (type m to see option menu): ")
		if userin[0] == "m" or userin[0] == "M":
			printMenu()
			continue
		root, mod = findRoot(userin)
	
		# if entrance format is incorrect, reenter input
		if root == -1:
			continue
	
		type = chooseType(mod)
		if type == -1:
			print("That is not a valid option. Please try again (type m to see option menu).")
			continue
		# printAccidentals(root)
		printScale(root, type)
		print()
		

def progressionMode():
	while True:
		numChords = input("Enter number of chords: ") # can be changed later
		try:
			numChords = int(numChords)
			break
		except:
			print("Please enter an integer.")
	
	chords = []
	x = 0
	while x < numChords:
		userin = input("Enter chord " + str(x+1) + " (type m to see option menu): ")
		if userin[0] == "m" or userin[0] == "M":
			printMenu()
			continue
		root, mod = findRoot(userin)
	
		# if entrance format is incorrect, reenter input
		if root == -1:
			continue
	
		type = chooseType(mod)
		if type == -1:
			print("That is not a valid option. Please try again (type m to see option menu).")
			continue

		tempChord = [root,mod,type]
		chords.append(tempChord)
		x += 1

	for temp in chords:
		print(temp[0]+temp[1])
		printScale(temp[0],temp[2])
		print()
		

def drawStaff(pos):
	# draw treble clef
	trebleClef = pygame.image.load("treble clef.png")
	trebleClef = pygame.transform.smoothscale(trebleClef, TREBLE_SIZE)
	SCREEN.blit(trebleClef, pos)

	LEFTX = pos[0]+10
	RIGHTX = WIDTH-(pos[0]+10)
	TOPY = pos[1]+5
	BOTTOMY = pos[1]+TREBLE_SIZE[1]-17
	SPACING = (BOTTOMY-TOPY)/4
	# left side vertical line
	pygame.draw.line(SCREEN, BLACK, (LEFTX,TOPY), (LEFTX,BOTTOMY))

	# right side vertical line
	pygame.draw.line(SCREEN, BLACK, (RIGHTX,TOPY), (RIGHTX,BOTTOMY))
		
	# horizontal staff lines
	for i in range(5):
		y = TOPY+SPACING*i
		pygame.draw.line(SCREEN, BLACK, (LEFTX,y), (RIGHTX,y))
		

def printNote(staffPos, noteName, oct, notePosX):
	# calculate x position
	xPos = (staffPos[0]+10) + (WIDTH-(staffPos[0]+10)*2)/90 + (WIDTH-(staffPos[0]+10)*2)/30*(notePosX+2)
	xPos = int(xPos)
	
	# calculate y position
	NOTE_SPACING = (TREBLE_SIZE[1]-23)/8

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
		
	yPos = int(middleCY - NOTE_SPACING*(mult + (oct-1)*8))

	# draw line through note if it qualifies
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
			
			sharp = pygame.image.load("sharp.png")
			sharp = pygame.transform.smoothscale(sharp, SHARP_SIZE)
			x = int(xPos + ACC_OFFSET - SHARP_SIZE[0]/2)
			y = int(yPos-SHARP_SIZE[1]/2)
			SCREEN.blit(sharp, (x, y))
		
		elif noteName[1] == 'b':
			
			flat = pygame.image.load("flat.png")
			flat = pygame.transform.smoothscale(flat, FLAT_SIZE)
			x = int(xPos + ACC_OFFSET - FLAT_SIZE[0]/2)
			y = int(yPos-FLAT_SIZE[1]/2) - 3
			SCREEN.blit(flat, (x,y))
	except:
		pass
		
	
# mode = chooseMode()
mode = 1
# Program Start
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONUP:
			print(pygame.mouse.get_pos())
			
	SCREEN.fill("white")

	
	drawStaff((10,20))
	printNote((10,20), "C#", 1, 0)
	printNote((10,20), "Bb", 1, 1)
	printNote((10,20), "D", 1, 2)
		
	pygame.display.update()
		
		
	# if mode == 1:
	# 	singleChordMode()
	# else:
	# 	progressionMode()
