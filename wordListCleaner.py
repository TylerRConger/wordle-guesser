import csv
import string
import matplotlib.pyplot as plt
import json


# Length of the word, default is 5
WORD_LEN = 5

# Saves the words to be used latter, this just means we don't have to do all this analysis each day
# instead do it once and reuse it
def saveWordList(words, filename):
    with open(filename, 'w') as file:
        json.dump(words, file)
    

# Reads the csv input file and returns a list of all items within the file, cleaned
def readFile(input):

    csv_ele = []

    with open(input, mode='r') as file:
        csv_reader = csv.reader(file)


        for row in csv_reader:
            for ele in row:
                if len(ele) == WORD_LEN:
                    csv_ele.append(ele.lower())

    return csv_ele

def graphHisto(alphabet_dict):
    letters = list(alphabet_dict.keys())
    freqs = list(alphabet_dict.values())

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.bar(letters, freqs, color='skyblue')

    # Add title and labels
    plt.title('Frequency of Letters from Word List')
    plt.xlabel('Letters')
    plt.ylabel('Frequency')

    # Save the plot
    plt.savefig('Frequency.png')

# Sort the words by how many 'good' letters they contain, more common letters is better, but no duplicate letters
def wordScorer(word, freqs):
    uniqued_word = set(word)
    return sum(freqs.get(letter, 0) for letter in uniqued_word)

# Analyze all the words in the dictionary to find the most common letters
def analyzeWords(allWords):
    alphabet_dict = {letter: 0 for letter in string.ascii_lowercase}

    for word in allWords:
        for char in word:
            #print(char)
            alphabet_dict[char] = alphabet_dict[char] + 1
    
    # Show Histogram graph
    graphHisto(alphabet_dict)

    # Sort the words by most used letter occurance
    sorted_words = sorted(allWords, key=lambda word: wordScorer(word, alphabet_dict), reverse=True)

    #print(sorted_words)

    # Print the dictionary to verify its contents
    #print(alphabet_dict)

    return sorted_words


#allWords = readFile('dictionary.csv')
#analyzedWords = analyzeWords(allWords)
#saveWordList(analyzedWords, 'sortedWords.json')