# ╔══════╗ #
# ║ 800J ║ #
# ╚══════╝ #

# Discord bot that puts memey randomly generated rap lyrics into a channel

import discord
import sys
import random

"""
Generates a Markov model based on args.
param words: a list of words parsed from the input txt file
param order: the order of the markov model
returns: the model (a dictionary)
"""
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

"""
Prints a line of markov-generated text
param model: The model to use
param key: the key to start on
param output: output string to append stuff to
returns: a tuple containing the output text to append and the next key
"""
def printLine(model, key):
    lastWord = False
    # build current line
    line = ''
    while not lastWord:
        # get next word using chain
        try:
            nextWord = random.choice(model[key])
            if ('\n' in nextWord):
                lastWord = True
            #if the next word starts a new line, you don't want to also print a space
            if (nextWord[len(nextWord)-1] == '\n'):
                # print(nextWord, end = '')
                line += nextWord
            else:
                # print(nextWord, end = ' ')
                line += (nextWord + ' ')
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

    returnTup = (line, key)
    return returnTup


TOKEN = 'NTA5OTIwMjM4MzYwMzMwMjQy.DsU0gA.Lx_Pazmxg0_RnSROjtv-Tv2XyC0'

client = discord.Client()

# get lyrics from txt file and clean them up
f = open('madeintyo.txt', 'r')
words = f.read()

words = words.replace('\n\n', '\n').replace('\n','\n ').split(' ')

for i in range(0, len(words)):
    for char in ['!','?','.',':',';','\"']:
        words[i] = words[i].replace(char, '')
words = tuple(words)
f.close()

# generate the markov model
model = generateModel(words, 1)
# list of supported artists, should change this depending on lyrics api stuff
artists = ['madeintyo']

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if '10 freaky girls' in message.content.lower():
        await client.send_message(message.channel, ':poggers:')
        return

    # basic function
    if message.content.startswith('!say'):
        args = message.content.split(' ')
        # verify args are valid
        if len(args) != 3:
            await client.send_message(message.channel, 'Invalid arguments\nUse \"!say [artist] [number of lines]\"')
            return
        if not args[2].isnumeric():
            await client.send_message(message.channel, 'Invalid arguments\nUse \"say [artist] [number of lines]\"')
            return
        if args[1] not in artists:
            await client.send_message(message.channel, 'idk this artist :(')
            return
        length = int(args[2])
        if length < 1:
            await client.send_message(message.channel, 'Invalid arguments\nUse \"!say [artist] [number of lines]\"')
            return
        if length > 10:
            await client.send_message(message.channel, 'no spam plz :monkaGun:')
            return

        # first select a random chain to start with
        key = random.choice(list(model.keys()))
        keyStart = 0
        #make sure the chain didn't start inside an ad-lib or newline
        keyText = ''.join(list(key))
        while '(' in keyText or ')' in keyText or '\n' in keyText:
            key = random.choice(list(model.keys()))
            keyText = ''.join(list(key))

        #build output string as we go
        output = ''

        # print the relevant words of the starting key
        for i in range(keyStart, 1):
            word = key[i]
            #if the next word starts a new line, you don't want to also print a space
            if (word[len(word)-1] == '\n'):
                output += word
                length -= 1
                if length == 0:
                    return
            else:
                output += (word + ' ')

        for i in range(0, length):
            # print one line
            returnTup = printLine(model, key)
            output += returnTup[0]
            key = returnTup[1]

        # TODO: tts? lol
        await client.send_message(message.channel, output)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)