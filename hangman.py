import words
import random
from sys import exit


def get_word():
    """
    Chooses a random word to be guessed by player
    :return: str
            random string with a noun from words.py
    """
    num_words = len(words.words)
    randint = random.randint(0, num_words)
    return words.words[randint]


def get_guess(already_guessed=None):
    """
    Prompts player for a guess letter
    :param already_guessed: str
                        contains already letters, both wrong and correct
    :return: char guessed by player, otherwise quit if player prints 'quit'
    """
    while True:
        print('Guess a letter: ')
        ans = input().lower()
        if ans == 'quit':
            exit(0)
        elif len(ans) != 1:
            print('\nPlease enter a single letter.')
        elif already_guessed is not None and ans in already_guessed:
            print('\nYou have already guessed that letter. Guess again.')
        elif ans not in 'abcdefghijklmnopqrstuvwxyz':
            print('\nPlease enter a LETTER.')
        else:
            return ans


def play_again():
    """
    Asks player if they want to play again
    :return: True - if player types 'y', False - if 'n', exits if answer is 'quit'
    """
    not_returned = True
    while not_returned:
        print('Do you want to play another game? y/n')
        answer = input().lower()
        if answer == 'quit':
            exit(0)
        if answer.startswith('y') or answer.startswith('n'):
            return answer.startswith('y')


def display_status(player_guess, number_of_wrong_guesses, num_guesses_left, incorrect_letters,
                   player_wins, computer_wins, message_string):
    """
    Show the current state of the game
    :param player_guess: char
                         a letter guesses by player
    :param number_of_wrong_guesses: int
                        number of incorrect guesses so far
    :param num_guesses_left: int
                        number of attempts left
    :param incorrect_letters: list of characters
                        list of incorrectly guesses letters
    :param player_wins: int
                        number of player wins in the current session
    :param computer_wins: int
                        number of computer wins in the current session
    :param message_string: str
                        information string about current status
    :return: empty return
    """
    print()
    print(' '.join(player_guess))
    print('\nNumber of wrong guesses:', number_of_wrong_guesses)
    print('Number of guesses left:', num_guesses_left)
    print("Wrongly guessed letters: ", list(incorrect_letters))
    print('Tally. Player: {}, Computer:{}'.format(player_wins, computer_wins))
    print(message_string)


if __name__ == '__main__':

    #  This is the main body of the game

    secret_word = get_word()
    print(secret_word) # disable this in the final product
    guessing_string = ['_']*len(secret_word)
    num_wrong_guesses = 0
    correct_guesses = ''
    max_guesses = 5
    guesses_left = max_guesses
    wrong_letters = ''
    wins_player = 0
    wins_computer = 0
    message_str = '\nGood luck! Starting the game'
    gameIsDone = False

    print('\nYou can always quit by typing \'quit\'')

    while True:
        display_status(guessing_string, num_wrong_guesses, guesses_left, wrong_letters,
                       wins_player, wins_computer, message_str)
        guess = get_guess(wrong_letters + correct_guesses)
        if guess in secret_word:
            correct_guesses = correct_guesses + guess
            for i in range(len(guessing_string)):
                if guess == secret_word[i]:
                    guessing_string[i] = guess
            foundAllLetters = True
            for i in range(len(secret_word)):
                if secret_word[i] not in correct_guesses:
                    foundAllLetters = False
                    message_str = '\nKeep going!'
                    break
            if foundAllLetters:
                wins_player += 1
                message_str = '\nCorrect!\nThe word is "' + secret_word + '"!\n'
                display_status(guessing_string, num_wrong_guesses, guesses_left, wrong_letters,
                               wins_player, wins_computer, message_str)

                gameIsDone = True

        else:
            wrong_letters = wrong_letters + guess
            num_wrong_guesses += 1
            guesses_left -= 1
            message_str = '\nWrong guess!'
            if num_wrong_guesses == max_guesses:
                wins_computer += 1
                message_str = '\nYou lost!\nThe correct word is "' + secret_word + '"!\n'
                display_status(guessing_string, num_wrong_guesses, guesses_left, wrong_letters,
                               wins_player, wins_computer, message_str)
                gameIsDone = True

        if gameIsDone:
            if play_again():
                secret_word = get_word()
                print(secret_word)
                guessing_string = ['_'] * len(secret_word)
                num_wrong_guesses = 0
                correct_guesses = ''
                max_guesses = 5
                guesses_left = max_guesses
                wrong_letters = ''
                message_str = '\nGood luck! Starting the game'
                gameIsDone = False
            else:
                break
