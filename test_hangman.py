import unittest
from unittest.mock import patch
import hangman
import words
# this import is is needed for testing (even though it seems not to be doing anything)!!
import sys
import io


class TestMain(unittest.TestCase):
    """Class for testing hangman.py"""

    def test_get_word(self):
        """Test function that chooses a word"""
        result1 = hangman.get_word()
        result2 = hangman.get_word()
        self.assertIn(result1, words.words)
        self.assertIn(result2, words.words)

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

    def test_play_again(self):
        with patch('builtins.input', return_value='No'):
            self.assertEqual(hangman.play_again(), False)

        with patch('builtins.input', return_value='Y'):
            self.assertEqual(hangman.play_again(), True)

        with patch('builtins.input', return_value='quit'):
            self.assertRaises(SystemExit, hangman.play_again)

    def test_display_status(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        hangman.display_status(['d','e','_','_','_'], 0, 0, ['a'], 0, 0, '\nKeep going!')
        print(captured_output.getvalue())
        hangman.display_status(['d', 'e', '_', '_', '_'], 5, 0, ['a','f','q','x','l'], 0, 1, '\nYou lost!')
        sys.stdout = sys.__stdout__
        print(captured_output.getvalue())

    def test_letter_in_word(self):
        secret_word = 'decoy'
        correct_guesses1, guessing_string1, message_str1, game_is_done1, wins_player1 = hangman.letter_in_word('y', 'deco',
                                                                                                  ['d','e','c','o','_'],
                                                                                                  secret_word, 0)
        correct_guesses2, guessing_string2, message_str2, game_is_done2, wins_player2 = hangman.letter_in_word('o','dec',
                                                                                                ['d','e','c','_','_'],
                                                                                                secret_word, 0)
        self.assertTrue(game_is_done1)
        self.assertEquals(message_str1, '\nCorrect!\nThe word is "' + secret_word + '"!\n')
        self.assertEquals(correct_guesses1, 'decoy')
        self.assertEquals(guessing_string1, ['d', 'e', 'c', 'o', 'y'])
        self.assertEquals(wins_player1, 1)

        self.assertFalse(game_is_done2)
        self.assertEquals(message_str2, '\nKeep going!')
        self.assertEquals(correct_guesses2, 'deco')
        self.assertEquals(guessing_string2, ['d', 'e', 'c', 'o', '_'])
        self.assertEquals(wins_player2, 0)

    def test_letter_not_in_word(self):
        message_str1, game_is_done1, wins_computer1 = hangman.letter_not_in_word('word', 0, 5)
        message_str2, game_is_done2, wins_computer2 = hangman.letter_not_in_word('word', 0, 0)
        self.assertTrue(game_is_done1)
        self.assertEquals(message_str1, '\nYou lost!\nThe correct word is "' + 'word' + '"!\n')
        self.assertEquals(wins_computer1, 1)
        self.assertFalse(game_is_done2)
        self.assertEquals(message_str2, '\nWrong guess!')
        self.assertEquals(wins_computer2, 0)

    def test_initiate_game(self):
        word, guessing_string, message_str = hangman.initiate_game(1)
        self.assertEquals(word, 'abacus')
        self.assertEquals(guessing_string, ['_','_','_','_','_','_'])
        self.assertEquals(message_str, '\nGood luck! Starting the game')

        word, guessing_string, message_str = hangman.initiate_game()
        self.assertIn(word, words.words)
        self.assertEquals(guessing_string, ['_']*len(word))
        self.assertEquals(message_str, '\nGood luck! Starting the game')



if __name__ == '__main__':
    unittest.main()
