
class Hangman(object):

    def __init__(self, filename):
        self.MAX_GUESSES = 6
        self.word_list = ['animal', 'intelligent',
                     'uniform']  # whatever list of words, add things later, proccess seperately
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

    def updateCounters(self, input):
        # self.words_guessed
        pass

    def updateDisplay(self):
        pass

    def updateTally(self):
        pass

    def updateHangmanDisplay(self):
        pass

    def isaWord(self,input):
        return len(input) > 1

    def isaLetter(self,input):
        return len(input) == 1

    def runGame(self):
        while self.guesses_left > 0:
            var = raw_input("Please enter a word or a letter: ")
            


if __name__ == "__main__":
    hangman = Hangman()
    hangman.runGame()
