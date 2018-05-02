import unittest
from unittest.mock import patch
import hangman
import words
# this import is is needed for testing (even though it seems not to be doing anything)!!
import sys


class TestMain(unittest.TestCase):
    """Class for testing hangman.py"""

    def test_get_word(self):
        """Test function that chooses a word"""
        result1 = hangman.get_word()
        result2 = hangman.get_word()
        self.assertIn(result1, words.words)
        self.assertIn(result2, words.words)

    def test_play_again(self):
        with patch('builtins.input', return_value='No'):
            self.assertEqual(hangman.play_again(), False)

        with patch('builtins.input', return_value='Y'):
            self.assertEqual(hangman.play_again(), True)

        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.play_again)

    def test_get_guess(self):
        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.get_guess)

        with patch('builtins.input', return_value='S'):
            self.assertEqual(hangman.get_guess(), 's')

        with patch('builtins.input', return_value='S'):
            self.assertEqual(hangman.get_guess('aolla'), 's')

        with patch('builtins.input', return_value='abc', side_effect='\nPlease enter a single letter.'):
            self.assertTrue(hangman.get_guess())

        with patch('builtins.input', return_value='9', side_effect='\nPlease enter a LETTER.'):
            self.assertTrue(hangman.get_guess())

        with patch('builtins.input', return_value='a',
                   side_effect='\nYou have already guessed that letter. Guess again.'):
            self.assertTrue(hangman.get_guess('a'))


if __name__ == '__main__':
    unittest.main()
