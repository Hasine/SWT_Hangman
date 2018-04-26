var = raw_input("Please enter a word: ")
print "you entered", var

word_list = ['animal', 'intelligent', 'uniform'] # whatever list of words, add things later, proccess seperately

class Hangman(object):

    def __init__(self, filename):
        self.MAX_GUESSES = 6
        self.this_word = ''
        self.guesses_left = self.MAX_GUESSES
        self.letters_guessed = set()
        self.words_guessed = set()
        self.tally = {'wins':0,
                      'losses':0}

    def processInput(self, input):
        pass

    def showDisplay(self):
        pass

    def getMessage(self):
        pass

    def updateWordString(self):
        pass

    def updateCounters(self):
        pass

    def updateDisplay(self):
        pass

    def updateTally(self):
        pass

    def updateHangmanDisplay(self):
        pass

    def runGame(self):
        pass

if __name__ == "__main__":
    hangman = Hangman()
    hangman.runGame()
