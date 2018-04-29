import numpy as np


def get_num_of_words(filename: str) -> int:
    with open(filename, 'r') as file:
        i = 0
        for _ in file:
            i += 1
        return i


def get_random_word(filename: str) -> str:
    randint = np.random.randint(0, get_num_of_words(filename))
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i == randint:
                return line.strip()


def get_guess(already_guessed):
    while True:
        print('Guess a letter/word: ')
        ans = input()
        ans = ans.lower()
        if ans.lower() == 'quit':
            exit(0)
        elif len(ans) != 1:
            print('Please enter a single letter.')
        elif ans in already_guessed:
            print('You have already guessed that letter. Guess again.')
        elif ans not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return ans


def play_again():
    not_returned = True
    while not_returned:
        print('Do you want to play another game? y/n')
        answer = input()
        if answer.lower().startswith('y') or answer.lower().startswith('n'):
            return answer.lower().startswith('y')


def display_status(guessing_string, num_wrong_guesses, num_guesses_left, wrong_letters,
                   player_wins, computer_wins, message_string):
    print(' '.join(guessing_string))
    print('\n')
    print('Number of wrong guesses:', num_wrong_guesses)
    print('Number of guesses left:', num_guesses_left)
    print("Wrongly guessed letters: ", list(wrong_letters))
    print('Tally. You: {}, Computer:{}'.format(player_wins, computer_wins))
    print(message_string)


secret_word = get_random_word('nouns_long.txt')
print(secret_word)
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

print('You can always quit by typing \'quit\'')

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
                message_str = 'Keep going!'
                break
        if foundAllLetters:
            print('Correct! The word is "' + secret_word + '"!')
            message_str = 'You have won!'
            wins_player += 1
            gameIsDone = True

    else:
        wrong_letters = wrong_letters + guess
        num_wrong_guesses += 1
        guesses_left -= 1
        if num_wrong_guesses == max_guesses:
            wins_computer += 1
            message_str = 'You lost!'
            display_status(guessing_string, num_wrong_guesses, guesses_left, wrong_letters,
                           wins_player, wins_computer, message_str)
            gameIsDone = True

    if gameIsDone:
        if play_again():
            secret_word = get_random_word('nouns_long.txt')
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
