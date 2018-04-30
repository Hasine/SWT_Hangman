import unittest
import hangman


class TestMain(unittest.TestCase):

    def test_get_num_of_words(self):
        self.assertEqual(hangman.get_num_of_words('testfiles/test_list1.txt'), 5)
        self.assertEqual(hangman.get_num_of_words('testfiles/test_list2.txt'), 2)

    def test_get_random_word(self):
        result1 = hangman.get_random_word('testfiles/test_list1.txt')
        words1 = ['one', 'two', 'three', 'four', 'five']
        result2 = hangman.get_random_word('testfiles/test_list2.txt')
        words2 = ['one', 'two']
        self.assertIn(result1, words1)
        self.assertIn(result2, words2)


if __name__ == '__main__':
    unittest.main()
