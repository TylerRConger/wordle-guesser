# imports
import json
import argparse
from wordListCleaner import *
from random import randint

# Read the sortedWords file to get a word list
def read_json_to_array(filename):
    with open(filename, 'r') as file:
        words = json.load(file)
    return words

# Must keep track of black letters
BLACK_LETTERS = []
# Key's are position 1 - 5 and values are letters a - z
# Must keep track of yellow letters and banned positions
YELLOW_LETTERS = {}
# Must keep track of green letters and allowed position
GREEN_LETTERS = {}

# Keep track of current guess
GUESS_NUM = 1

# Completes one action
# 1. Remove all words that do not contain a letter at specified position
def greenFilter(words_list):
    filtered_words = []
    
    for word in words_list:
        add_word = True
        for position, letter in GREEN_LETTERS.items():
            # Check if the word contains the letter at the specified position
            if not (position <= len(word) and word[position - 1] == letter):
                add_word = False
                break
        
        if add_word:
            filtered_words.append(word)
    
    return filtered_words

# Completes two actions
# 1. Remove all the words that do not contain a yellow letter
# 2. Remove all the words that contain the yellow letter but only at yellow position
def yellowFilter(words_list):
    filtered_words = []
    letters_to_include = set(YELLOW_LETTERS.values())
    
    for word in words_list:
        # Check if the word contains any of the letters in the positions_dict values
        if not any(letter in word for letter in letters_to_include):
            filtered_words.append(word)
            continue
        
        add_word = True
        for position, letter in YELLOW_LETTERS.items():
            # Check if the word contains the letter at the specified position
            if position <= len(word) and word[position - 1] == letter:
                add_word = False
                break
        
        if add_word:
            filtered_words.append(word)
    return filtered_words        

# Uses information about other two dictionaries and guess to determine black letters
# Some tough situations to consider
    # 1. We overwrote a yellow position earlier - not a consideration, should be non issue
    # 2. We guess 2 of the same letter and second one is black - make list into set before adding to black letters
def addBlackLetters(guess):
    yellowLettersList = set(YELLOW_LETTERS.values())
    greenLettersList = set(GREEN_LETTERS.values())

    for char in guess:
        if char not in yellowLettersList and char not in greenLettersList:
            BLACK_LETTERS.append(char)


# Use info about the black letters to filter all such words
def blackFilter(words_list):
    filtered_words = []
    
    for word in words_list:
        # Check if the word contains any of the specified letters
        contains_letter = False
        for letter in BLACK_LETTERS:
            if letter in word:
                contains_letter = True
                break
        
        # If the word does not contain any of the specified letters, add it to the filtered list
        if not contains_letter:
            filtered_words.append(word)
    
    return filtered_words

def guesser(words, verbose=False, random=False):
    global GUESS_NUM

    # If its random, randomly pick
    if random:
        guess = words[randint(0, len(words))]
    # If verbose let them pick from the first few
    elif verbose:
        topGuesses = words[:5]
        
        # Step 1: Create a formatted string for each element with its index
        formatted_elements = ', '.join(f"{index + 1}: {element}" for index, element in enumerate(topGuesses))

        # Step 2: Format the final string
        formatted_string = f"Which of the best guesses would you like ({formatted_elements}): "

        selection = input(formatted_string)
        guess = words[int(selection) - 1]
    # Otherwise just pick the absolute best
    else:
        guess = words[0]

    
    if verbose:
        print("There are " + str(len(words)) + " potential words remaining.")
    # Make an initial guess
    print("Guess 1: " + guess) 

    solved = input("Did we solve it? (y/n): ")


    # Repeat until correctly guessed
    while (solved != 'y'):
        # Gather yellow inputs
        yellowsString = input("What were the yellows? (Format _y_er): ")

        # Gather green inputs
        greensString = input("What were the greens? (Format t_l__): ")

        # Default to empty
        while (len(yellowsString) < len(guess)):
            yellowsString += "_"
        
        while (len(greensString) < len(guess)):
            greensString += "_"

        # Convert to dictionary
        for i in range(0,len(guess)):
            if yellowsString[i] != '_':
                YELLOW_LETTERS[i + 1] =  yellowsString[i]
            if greensString[i] != '_':
                GREEN_LETTERS[i + 1] =  greensString[i]

        # Add black'ed out letters by elimination
        addBlackLetters(guess)

        # Do the elimination step
        words = blackFilter(words)
        words = yellowFilter(words)
        words = greenFilter(words)

        # List possible guesses
            # List a best guess with most used letters
        GUESS_NUM = GUESS_NUM + 1
        # If its random, randomly pick
        if random:
            guess = words[randint(0, len(words))]
        # If verbose let them pick from the first few
        elif verbose:
            topGuesses = words[:5]
        
            # Step 1: Create a formatted string for each element with its index
            formatted_elements = ', '.join(f"{index + 1}: {element}" for index, element in enumerate(topGuesses))

            # Step 2: Format the final string
            formatted_string = f"Which of the best guesses would you like ({formatted_elements}): "

            selection = input(formatted_string)
            guess = words[int(selection) - 1]
        # Otherwise just pick the absolute best
        else:
            guess = words[0]


        if verbose:
            print("There are " + str(len(words)) + " potential words remaining.")
        print("Guess " + str(GUESS_NUM) + ": " + guess)
        solved = input("Did we solve it? (y/n): ")
            

if __name__ == "__main__":

    # Initialize ArgumentParser
    parser = argparse.ArgumentParser(description="Word Guessing Game")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase game verbose-ness as well as allowing for picking word at each round")
    parser.add_argument("-r", "--random", action="store_true", help="Instead of picking only first (best) option, pick a random one to make the game different each day")
    parser.add_argument("-f", "--filename", nargs='?', help="Use a new file for the dictionary (not the default one). Try and use a csv file, but might work with other types too!?")
    #parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    if args.filename:
        # If you pass a json do it right please, and make it look like mine
        if args.filename.endswith('.json'):
            words = read_json_to_array(args.filename)
        else:
            allWords = readFile(args.filename)
            analyzedWords = analyzeWords(allWords)
            saveWordList(analyzedWords, 'sortedWords.json')
            # Read the sortedWords file to get a word list
            words = read_json_to_array('sortedWords.json')        
    else:
        words = read_json_to_array('sortedWords.json')


    # Start the guessing
    guesser(words, verbose=args.verbose, random=args.random)
