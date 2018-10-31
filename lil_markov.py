# ╔══════╗ #
# ║ 800J ║ #
# ╚══════╝ #

# Takes a .txt file containing input text as a command line argument
# and randomly generates text based on the input using a Markov model


# TODO: choose artist?
# TODO: have it cut off only at the end of a line, otherwise it ends awkwardly on random words
# TODO: be able to choose the starting word
# TODO: adlibs (in parentheses) should be treated as one word

# possible user flow:
# 1. enter artist as command line arg
# 2. ask how many lines they want
# 3. output lines
# 4. ask if they want to continue, if yes goto 2, if no exit

import sys
import random

def generateModel(words, order):
	model = {}
	for i in range(0, len(words) - order):
		chainLeft = words[i:i+order] # get block of words whose length corresponds to order
		chainRight = words[i+order] # get next word to complete chain
		# Model implemented with a dictionary, where both key and value are lists 
		# The key is the initial state
		# The value is a list of words that are the possible final states
		if chainLeft not in model:
			model[chainLeft] = []
		model[chainLeft].append(chainRight)
	return model

def generateText(words, order, length, start):
	#generate model
	model = generateModel(words, order)

	# first select a random chain to start with
	key = random.choice(list(model.keys()))
	keyStart = 0
	#make sure the chain didn't start inside an ad-lib
	while '(' in ''.join(list(key)) or ')' in ''.join(list(key)):
		key = random.choice(list(model.keys()))

	# start word was specified, find starting point for chain with that word
	if start:
		keyList = list(model.keys())[:]
		exists = False
		for k in keyList:
			if start in k:
				exists = True
				break
		if exists:
			print('Specified starting word not in text. Picking random start')
		else:
			# don't know how to do this faster
			# right now just gonna make a copy of the key list and randomly
			# go through the keys til you find one that has the start word,
			# and removing the ones that don't
			
			key = None
			while(not key):
				i = random.randomint(0,len(keyList))
				if start in list(keyList[i]):
					key = keyList[i]
				else:
					#remove from keyList
					keyList.pop(i)
			keyStart = list(key).index(start)


			

	# just a padding to see text in command line more clearly
	print('')

	for i in range(keyStart, order):
		word = key[i]
		#if the next word starts a new line, you don't want to also print a space
		if (word[len(word)-1] == '\n'):
			print(word, end = '')
		else:
			print(word, end = ' ')

	for i in range(0, length):
		# get next word using chain
		try:
			nextWord = random.choice(model[key])
			#if the next word starts a new line, you don't want to also print a space
			if (nextWord[len(nextWord)-1] == '\n'):
				print(nextWord, end = '')
			else:
				print(nextWord, end = ' ')
		# a KeyError can happen when the chain formed happens to be the last in the model text
		except (KeyError, IndexError) as e:
			# if this happens we'll just keep going with a random chain
			key = random.choice(list(model.keys()))
			while '(' in ''.join(list(key)) or ')' in ''.join(list(key)):
				key = random.choice(list(model.keys()))
			i -= 1
			continue

		#create next key to use
		end = len(key)
		start = 1
		key = list(key[start:end])
		key.append(nextWord)
		key = tuple(key)

	# just a padding to see text in command line more clearly
	print('')

# process the text so that ad-lib type segments in parentheses will be treated as one word
# strategy is to replace whitespace in between parentheses with underscores then replace back later

# idk how to do this so for now im just making sure that the markov chain can't start near parentheses.
# this was causing the most weird output; with a high enough order markov model it will probably just go
# though the whole sequence inside the parentheses so that shouldn't be a huge issue

# if parentheses aren't closed properly somewhere in the text this will screw everything up so
# something you could do is have a flag on command line that enables/disables this function
# def processParens(words):


# read in txt file, split into list by whitespace
if len(sys.argv) < 3 or len(sys.argv) > 4:
	print("Run using \"python lil_markov.py *markov chain order* *# of words* *starting word*(optional)\"")
	sys.exit(0)
#get order number and output size from command line
order = sys.argv[1]
length = sys.argv[2]
start = None
if len(sys.argv) == 4:
	start = sys.argv[3]
	print('\nFYI this function is currently broken\n')
if not order.isnumeric():
	print("order number must be a number\nexiting")
	sys.exit(0)
if not length.isnumeric():
	print("length must be a number\nexiting")
	sys.exit(0)
order = int(order)
length = int(length)


#get list of words sans special characters from txt file

# TODO: txt file currently hard coded in
f = open('madeintyo.txt', 'r')
words = f.read()

words = words.replace('\n\n', '\n').replace('\n','\n ').split(' ')

for i in range(0, len(words)):
	for char in ['!','?','.',':',';','\"']:
		words[i] = words[i].replace(char, '')
words = tuple(words)
f.close()

# output the text
generateText(words, order, length, start)



