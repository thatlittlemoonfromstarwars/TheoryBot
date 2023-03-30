import pygame

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
	

while(True):
	# mode select
	print("----Modes----")
	print("1. Single Chord or Scale")
	print("2. Chord progression")
	mode = int(input("Choose a mode:"))
	if mode == 1 or mode == 2:
		break
	else:
		print("That is not a valid mode. Please enter a valid mode.")
		print()

while(True):
	if mode == 1:
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
		
	else:
		# progression
		while(True):
			numChords = input("Enter number of chords: ") # can be changed later
			try:
				numChords = int(numChords)
				break
			except:
				print("Please enter an integer.")
		
		chords = []
		x = 0
		while(x < numChords):
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
		
		
