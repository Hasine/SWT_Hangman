import unittest
from unittest.mock import patch
import hangman
import words
# this import is is needed for testing (even though it seems not to be doing anything)!!
import sys
from io import StringIO
from contextlib import contextmanager
import logging


class TestHangman(unittest.TestCase):
    """Class for testing hangman.py"""

    @contextmanager
    def capture(self, command, *args):
        out, sys.stdout = sys.stdout, StringIO()
        try:
            command(*args)
            sys.stdout.seek(0)
            yield sys.stdout.read()
        finally:
            sys.stdout = out

    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def test_get_word(self):
        """Test function that chooses a word"""
        result1 = hangman.get_word()
        result2 = hangman.get_word()
        self.assertIn(result1, words.words)
        self.assertIn(result2, words.words)

    def test_get_guess(self):
        # TC1: ans = quit
        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.get_guess)

        # TC2: ans = a, already_guessed = None
        with patch('builtins.input', return_value='a'):
            self.assertEqual(hangman.get_guess(), 'a')

        # TC3: ans = ab
        with patch('builtins.input', return_value='ab', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("Please enter a single LETTER", output)

        # TC4: ans =,
        with patch('builtins.input', return_value=',', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("Please enter a single LETTER", output)

        # TC4: ans =,,
        with patch('builtins.input', return_value=',,', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("Please enter a single LETTER", output)

        # TC6: ans = a, already_guessed = a
        user_input = ['a', 'quit']
        already_guessed = 'a'

        with patch('builtins.input', side_effect=user_input):
            with self.assertRaises(SystemExit):
                self.assertIn("You have already guessed that letter", self.capture(hangman.get_guess(already_guessed)))

        # TC7: ans = b, already_guessed = a
        with patch('builtins.input', return_value='a'):
            self.assertEqual(hangman.get_guess('b'), 'a')

    def test_play_again(self):
        # TC1: ans = 'quit'
        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.play_again)

        # TC2: ans = 'asdf'
        with patch('builtins.input', return_value='asdf', side_effect='Do you want to play another game? y/n'):
            with self.capture(hangman.play_again) as output:
                self.assertIn("y/n", output)

        # TC3: ans = 'y'
        with patch('builtins.input', return_value='y'):
            self.assertEqual(hangman.play_again(), True)

        # TC4: ans = 'n'
        with patch('builtins.input', return_value='n'):
            self.assertEqual(hangman.play_again(), False)

    def test_display_status(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        hangman.display_status(['d', 'e', '_', '_', '_'], hangman.CONST_MAX_GUESSES,
                               0, ['a', 'f', 'q', 'x', 'l'], 0, 1, '\nYou lost!')
        sys.stdout = sys.__stdout__
        string = captured_output.getvalue()
        self.assertIn('Number of guesses left', string)
        self.assertIn('Wrongly guessed letters', string)
        self.assertIn('Tally', string)

    def test_letter_in_word(self):
        secret_word = 'banana'

        # TC1: guessing_string =['b','_','n','_','n','_'], guess = a, correct_guesses = bn
        correct_guesses1, guessing_string1, message_str1, game_is_done1, wins_player1 = \
            hangman.letter_in_word('a', 'bn', ['b', '_', 'n', '_', 'n', '_'], secret_word, 0)

        self.assertTrue(game_is_done1)
        self.assertEqual(message_str1, '\nCorrect!\nThe word is "' + secret_word + '"!\n')
        self.assertEqual(correct_guesses1, 'bna')
        self.assertEqual(guessing_string1, ['b', 'a', 'n', 'a', 'n', 'a'])
        self.assertEqual(wins_player1, 1)

        # TC2: guessing_string =['_','_','n','_','n','_'] , guess = a, correct_guesses = n
        correct_guesses2, guessing_string2, message_str2, game_is_done2, wins_player2 = \
            hangman.letter_in_word('a', 'n', ['_', '_', 'n', '_', 'n', '_'], secret_word, 0)

        self.assertFalse(game_is_done2)
        self.assertEqual(message_str2, '\nKeep going!')
        self.assertEqual(correct_guesses2, 'na')
        self.assertEqual(guessing_string2, ['_', 'a', 'n', 'a', 'n', 'a'])
        self.assertEqual(wins_player2, 0)

    def test_letter_not_in_word(self):
        # TC1: num_wrong_guesses = CONST_MAX_GUESSES
        message_str1, game_is_done1, wins_computer1 = hangman.letter_not_in_word('word', 0, hangman.CONST_MAX_GUESSES)
        self.assertTrue(game_is_done1)
        self.assertEqual(message_str1, '\nYou lost!\nThe correct word is "' + 'word' + '"!\n')
        self.assertEqual(wins_computer1, 1)

        # TC2: num_wrong_guesses = 0
        message_str2, game_is_done2, wins_computer2 = hangman.letter_not_in_word('word', 0, 0)
        self.assertFalse(game_is_done2)
        self.assertEqual(message_str2, '\nWrong guess!')
        self.assertEqual(wins_computer2, 0)

    def test_initiate_game(self):
        # TC1: word_ind = 1
        word, guessing_string, message_str = hangman.initiate_game(1)
        self.assertEqual(word, 'abacus')
        self.assertEqual(guessing_string, ['_', '_', '_', '_', '_', '_'])
        self.assertEqual(message_str, '\nGood luck! Starting the game')

        # TC2: word_ind = Null
        word, guessing_string, message_str = hangman.initiate_game()
        self.assertIn(word, words.words)
        self.assertEqual(guessing_string, ['_'] * len(word))
        self.assertEqual(message_str, '\nGood luck! Starting the game')

    def test_run_game(self):
        word_id = 245  # banana

        # TC1: b, a, c, n, n
        user_input1 = ['b', 'a', 'c', 'n', 'n']

        with patch('builtins.input', side_effect=user_input1):
            with self.assertRaises(SystemExit):
                with self.captured_output() as (out, err):
                    hangman.run_game(word_id)

        output = out.getvalue().strip()
        self.assertIn("Wrong guess!", output)
        self.assertIn("Correct!", output)

        # TC2: b, a, n, quit
        user_input2 = ['b', 'a', 'n', 'quit']

        with patch('builtins.input', side_effect=user_input2):
            with self.assertRaises(SystemExit):
                self.assertIn("Correct!", self.capture(hangman.run_game(word_id)))

        # TC3: b, a, n, y, quit
        user_input3 = ['b', 'a', 'n', 'y', 'quit']

        with patch('builtins.input', side_effect=user_input3):
            with self.assertRaises(SystemExit):
                with self.captured_output() as (out, err):
                    hangman.run_game(word_id)

        output3 = out.getvalue().strip()
        self.assertIn("Correct!", output3)
        self.assertIn("Tally. Player: 1", output3)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestHangman.test_get_guess").setLevel(logging.DEBUG)
    unittest.main()
