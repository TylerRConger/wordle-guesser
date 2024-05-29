## Word Guessing Game
Solve your Wordle answers 

### Installation
1. Clone the repository:
``` 
git clone https://github.com/yourusername/word-guessing-game.git
```

2 .Navigate to the project directory:
```
cd 'Wordle Fun'
```

3. Install the required dependencies:
(Everything else is included with python)
```
pip install matplotlib
```

### Usage
Run the script with the following command:

```
python script.py [-h] [-v] [-f FILENAME]
```

#### Optional Arguments:
-h, --help: Show help message and exit.
-v, --verbose: Increase output verbosity.
-f FILENAME, --filename FILENAME: Specify a filename. The file can be in JSON or CSV format containing the list of words. If not provided, the script will default to using 'sortedWords.json'.

### Gameplay Instructions:
1. The script will make an initial guess based on the word list.
2. You will be prompted to provide feedback on the guess.
3. Enter the positions of letters that are correct (yellow) and letters that are both correct and in the correct position (green).
4. The script will make subsequent guesses based on your feedback until the word is correctly guessed.