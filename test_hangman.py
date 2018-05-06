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

    def test_get_word(self):
        """Test function that chooses a word"""
        result1 = hangman.get_word()
        result2 = hangman.get_word()
        self.assertIn(result1, words.words)
        self.assertIn(result2, words.words)

    def test_get_guess(self):

        with patch('builtins.input', return_value='S'):
            self.assertEqual(hangman.get_guess(), 's')

        with patch('builtins.input', return_value='S'):
            self.assertEqual(hangman.get_guess('aolla'), 's')

        with patch('builtins.input', return_value='9', side_effect='Please enter a single LETTER'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("e", output)

        with patch('builtins.input', return_value='abc', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("Please enter a single LETTER", output)

        with patch('builtins.input', return_value=',', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("Please enter a single LETTER", output)

        with patch('builtins.input', return_value='', side_effect='\nPlease enter a single LETTER.'):
            with self.capture(hangman.get_guess) as output:
                self.assertIn("single", output)

    def test_play_again(self):
        with patch('builtins.input', return_value='No'):
            self.assertEqual(hangman.play_again(), False)

        with patch('builtins.input', return_value='Y'):
            self.assertEqual(hangman.play_again(), True)

        with patch('builtins.input', return_value='asdf', side_effect='Do you want to play another game? y/n'):
            with self.capture(hangman.play_again) as output:
                self.assertIn("y/n", output)

        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.play_again)

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
        secret_word = 'decoy'
        correct_guesses1, guessing_string1, message_str1, game_is_done1, wins_player1 = hangman.letter_in_word('y',
                                                                                                               'deco',
                                                                                                  ['d','e','c','o','_'],
                                                                                                  secret_word, 0)
        correct_guesses2, guessing_string2, message_str2, game_is_done2, wins_player2 = hangman.letter_in_word('o','dec',
                                                                                                ['d','e','c','_','_'],
                                                                                                secret_word, 0)
        self.assertTrue(game_is_done1)
        self.assertEqual(message_str1, '\nCorrect!\nThe word is "' + secret_word + '"!\n')
        self.assertEqual(correct_guesses1, 'decoy')
        self.assertEqual(guessing_string1, ['d', 'e', 'c', 'o', 'y'])
        self.assertEqual(wins_player1, 1)

        self.assertFalse(game_is_done2)
        self.assertEqual(message_str2, '\nKeep going!')
        self.assertEqual(correct_guesses2, 'deco')
        self.assertEqual(guessing_string2, ['d', 'e', 'c', 'o', '_'])
        self.assertEqual(wins_player2, 0)

    def test_letter_not_in_word(self):
        message_str1, game_is_done1, wins_computer1 = hangman.letter_not_in_word('word', 0, hangman.CONST_MAX_GUESSES)
        message_str2, game_is_done2, wins_computer2 = hangman.letter_not_in_word('word', 0, 0)
        self.assertTrue(game_is_done1)
        self.assertEqual(message_str1, '\nYou lost!\nThe correct word is "' + 'word' + '"!\n')
        self.assertEqual(wins_computer1, 1)
        self.assertFalse(game_is_done2)
        self.assertEqual(message_str2, '\nWrong guess!')
        self.assertEqual(wins_computer2, 0)

    def test_initiate_game(self):
        word, guessing_string, message_str = hangman.initiate_game(1)
        self.assertEqual(word, 'abacus')
        self.assertEqual(guessing_string, ['_', '_', '_', '_', '_', '_'])
        self.assertEqual(message_str, '\nGood luck! Starting the game')

        word, guessing_string, message_str = hangman.initiate_game()
        self.assertIn(word, words.words)
        self.assertEqual(guessing_string, ['_']*len(word))
        self.assertEqual(message_str, '\nGood luck! Starting the game')

    def test_run_game(self):
        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.run_game)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("TestHangman.test_get_guess").setLevel(logging.DEBUG)
    unittest.main()
