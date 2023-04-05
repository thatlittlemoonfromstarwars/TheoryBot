import pygame, sys
import pygame_textinput
from pygame.locals import QUIT
from pygame import gfxdraw

# global constants
WIDTH = 1200
HEIGHT = 500
WINDOW_SIZE = (WIDTH, HEIGHT)
TREBLE_SIZE = (70,70)
ACC_OFFSET = 11
SHARP_SIZE = (40,40)
FLAT_SIZE = (8,18)
STAFF_POS = (10,20)
NOTES_PER_STAFF = int(WIDTH/1000*28)
NOTE_SPACING_Y = (TREBLE_SIZE[1]-23)/8
NOTE_SPACING_X = (WIDTH-(STAFF_POS[0]+10)*2)/(NOTES_PER_STAFF+2)
BLACK = (0,0,0)

# global variables
notesOnStaff = [None] * NOTES_PER_STAFF	# represents all the notes added to the staff
										# formatted: (noteName, octave, text)
										# index represents xPos
mode = 2 # set mode here - 1 is single chord mode, 2 is progression mode
notePos = 0 # for progression mode

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

# setup for pygame
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
SUBSCRIPT_FONT = pygame.font.Font("Roboto/Roboto-Medium.ttf", 15)
INPUT_FONT = pygame.font.Font("Roboto/Roboto-Light.ttf", 25)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# load treble clef
trebleClef = pygame.image.load("treble clef.png")
trebleClef = pygame.transform.smoothscale(trebleClef, TREBLE_SIZE)
# load accidentals
sharp = pygame.image.load("sharp.png")
sharp = pygame.transform.smoothscale(sharp, SHARP_SIZE)
flat = pygame.image.load("flat.png")
flat = pygame.transform.smoothscale(flat, FLAT_SIZE)
# set caption
if mode == 1:
	pygame.display.set_caption('TheoryBot - Single Chord Mode')
else:
	pygame.display.set_caption('TheoryBot - Progression Mode')
# https://replit.com/talk/learn/Pygame-Tutorial/143782

# for text input
textinput = pygame_textinput.TextInputVisualizer()
textinput.antialias = True
textinput.font_object = INPUT_FONT
textinput.cursor_width = 2
# https://github.com/Nearoo/pygame-text-input

def findRoot(userin):
	# seperates user input into root note and modifier
	if allNotes.count(userin[0].capitalize()) == 0:
		return -1, -1
		
	if userin.find('b') == 1 or (userin.find('b') == 0 and userin[1] == 'b'):
		ind = allNotes.index(userin[0].capitalize())-1
		if ind == -1:
			ind = 11
		return allNotes[ind], userin[2:]
		
	elif userin.find('#') == 1:
		ind = allNotes.index(userin[0].capitalize())+1
		if ind == 12:
			ind = 0
		return allNotes[ind], userin[2:]
		
	else:
		return userin[0].capitalize(), userin[1:]

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
	# returns the corresponding step list, taking the
	# modifier as input
	match mod:	
		case "":
			return dom7 # default choice
		case "maj":
			return major
		case "min":
			return minor
		case "pM":
			return pentatonicM
		case "pm":
			return pentatonicm
		case "B":
			return blues
		case "M":
			return maj
		case "M7":
			return maj7
		case "M9":
			return maj9
		case "M11":
			return maj11
		case "m":
			return min
		case "m7":
			return min7
		case "m9":
			return min9
		case "m11":
			return min11
		case "dim":
			return dim
		case "dom7":
			return dom7
		case "7":
			return dom7
		case "dom9":
			return dom9
		case "9":
			return dom9
		case "sus2":
			return sus2
		case "sus4":
			return sus4
		case "aug":
			return aug
		case _:
			return -1
			
def processSingleChord(userin):
	# prints a single chord or scale
	
	global notesOnStaff
	notesOnStaff = [None] * NOTES_PER_STAFF
	
	root, mod = findRoot(userin)

	# if entrance format is incorrect, reenter input
	if root == -1:
		return 1

	# remove space from mod
	try:
		if mod[0] == ' ':
			mod = mod[1:]
	except:
		pass

	# get step list
	type = chooseType(mod)
	if type == -1:
		return 1
	
	# add notes to notesOnStaff
	addScaleToStaff(root, mod, type, 0)
	print(root+mod)
	printScale(root, type)
	print()

	return 0
		
def processChordProgression(userin):
	# prints a chord progression

	global notesOnStaff
	global notePos
	# if user types clear, clear chords
	if userin.lower() == "clear":
		notesOnStaff = [None]*NOTES_PER_STAFF
		notePos = 0
		return 0

	root, mod = findRoot(userin)

	# if entrance format is incorrect, reenter input
	if root == -1:
		return 1

	# remove space from mod
	try:
		if mod[0] == ' ':
			mod = mod[1:]
	except:
		pass

	# get step list
	type = chooseType(mod)
	if type == -1:
		return 1
	
	# add notes to notesOnStaff
	tempNotePos = addScaleToStaff(root, mod, type, notePos)
	if tempNotePos == -1: # prevents note overflow
		return 2
	notePos = tempNotePos
	print(root+mod)
	printScale(root, type)
	print()

	return 0

def addScaleToStaff(root, mod, steps, startingPos):
	# adds a scale or chord to notesOnStaff

	# determine whether to print sharps or flats
	noteInd = allNotes.index(root)
	if accidentals[noteInd] > 0:
		sharpScale = True
	else:
		sharpScale = False
	
	notePos = startingPos
	if startingPos + len(steps) + 1 > NOTES_PER_STAFF: # check for note overflow
		return -1
	for x in range(len(steps)+1):
		# get note name
		note = allNotes[noteInd%12]

		# if sharpScale, change flat note to it's equivalent sharp note
		if sharpScale and note.count('b') == 1:
			note = allNotes[noteInd%12-1] + "#"

		# find octave
		if noteInd < 12:
			oct = 1
		else:
			oct = 2

		# add notes to notesOnStaff
		if x == 0:
			notesOnStaff[notePos] = (note, oct, note+mod)
		else:
			notesOnStaff[notePos] = (note, oct, None)
		
		notePos += 1
		noteInd += steps[x%(len(steps))]

	return notePos

def drawStaff(pos):
	# draws the staff

	# staff dimensions
	LEFTX = pos[0]+10
	RIGHTX = WIDTH-(pos[0]+10)
	TOPY = pos[1]+5
	BOTTOMY = pos[1]+TREBLE_SIZE[1]-17
	STAFF_SPACING = (BOTTOMY-TOPY)/4

	# draw treble clef
	SCREEN.blit(trebleClef, pos)
	
	# draw left side vertical line
	pygame.draw.line(SCREEN, BLACK, (LEFTX,TOPY), (LEFTX,BOTTOMY))

	# draw right side vertical line
	pygame.draw.line(SCREEN, BLACK, (RIGHTX,TOPY), (RIGHTX,BOTTOMY))
		
	# draw horizontal staff lines
	for i in range(5):
		y = TOPY+STAFF_SPACING*i
		pygame.draw.line(SCREEN, BLACK, (LEFTX,y), (RIGHTX,y))
		
def drawNote(noteName, oct, notePosX, text):
	# draws a single note on the staff
	# returns note position

	# calculate x position
	xPos = (STAFF_POS[0]+10) + NOTE_SPACING_X/3 + NOTE_SPACING_X*(notePosX+2)
	xPos = int(xPos)
	
	# calculate y position
	# middle C is used as the reference position
	middleCY = STAFF_POS[1] + NOTE_SPACING_Y*11

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
		
	yPos = int(middleCY - NOTE_SPACING_Y*(mult + (oct-1)*7))

	# draw line through note if it is above or below staff
	if yPos > (STAFF_POS[1] + NOTE_SPACING_Y*10) or yPos < (STAFF_POS[1] - NOTE_SPACING_Y):
		pygame.draw.line(SCREEN, BLACK, (xPos-9,yPos), (xPos+9,yPos))
	
	# draw note
	gfxdraw.aacircle(SCREEN, xPos, yPos, 5, BLACK)
	gfxdraw.filled_circle(SCREEN, xPos, yPos, 5, BLACK)

	# draw accidental
	try:
		if noteName[1] == '#':
			# draw sharp symbol
			x = int(xPos - ACC_OFFSET - SHARP_SIZE[0]/2)
			y = int(yPos-SHARP_SIZE[1]/2)
			SCREEN.blit(sharp, (x, y))
		
		elif noteName[1] == 'b':
			# draw flat symbol
			x = int(xPos - ACC_OFFSET - FLAT_SIZE[0]/2)
			y = int(yPos-FLAT_SIZE[1]/2) - 3
			SCREEN.blit(flat, (x,y))
	except:
		pass
	
	if text != None:
		# if note is first note in the chord, write the chord name under the note
		printOnScreen(text, (xPos - 4, STAFF_POS[1] + NOTE_SPACING_Y*11+5))
		if notePosX != 0:
			# if note is not the first note on the staff, but the first note of a chord, draw a bar line
			p1 = (xPos-NOTE_SPACING_X*3/5, STAFF_POS[1]+NOTE_SPACING_Y)
			p2 = (xPos-NOTE_SPACING_X*3/5, STAFF_POS[1]+NOTE_SPACING_Y*9)
			pygame.draw.line(SCREEN, BLACK, p1, p2)
	
	return xPos, yPos

def drawNotes():
	# draws all notes in notesOnStaff onto the staff
	index = 0
	while index < len(notesOnStaff):
		if notesOnStaff[index] != None:
			try:
				drawNote(notesOnStaff[index][0], notesOnStaff[index][1], index, notesOnStaff[index][2])
			except:
				drawNote(notesOnStaff[index][0], notesOnStaff[index][1], index)
		index += 1

def printOnScreen(text, pos):
	# print text to screen (not console)
	toPrint = SUBSCRIPT_FONT.render(text, True, BLACK)
	SCREEN.blit(toPrint, pos)
	
# Program Start
printError = 0
while True:
	# every frame:
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
			# when enter is pressed
			if textinput.value == '':
				# if text is empty
				printError = 1
			elif mode == 1:
				printError = processSingleChord(textinput.value)
			else:
				printError = processChordProgression(textinput.value)
			if printError == 0:		
				textinput.value = ''

	# error menu
	if printError == 1:
		# incorrect input format
		printOnScreen("Invalid input. Please try again.", (20, HEIGHT-20))
	elif printError == 2:
		# staff overflow
		printOnScreen("The staff is full or almost full. Type \"clear\" to reset it.", (20, HEIGHT-20))
	pygame.display.update()
	clock.tick(30)
