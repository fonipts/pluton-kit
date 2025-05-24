import unittest
from plutonkit.framework.analysis.word_distance import WordDistance

class TestWordDistance(unittest.TestCase):
    def setUp(self):
        # Use some sample valid words
        self.valid_words = ['apple', 'apply', 'ape']
        self.word_distance = WordDistance(self.valid_words)

    def test_init(self):
        self.assertEqual(self.word_distance.valid_words, self.valid_words)

    def test_get_ave_distance_length(self):
        word = 'apple'
        result = self.word_distance.get_ave_distance(word)
        self.assertEqual(len(result), len(self.valid_words))

    def test_get_ave_distance_values(self):
        # For identical word, expect maximum score
        result = self.word_distance.get_ave_distance('apple')
        self.assertAlmostEqual(result[0], 1.0, delta=0.01)  # 'apple' vs 'apple'

        # For a word with some overlap
        result = self.word_distance.get_ave_distance('ape')
        self.assertTrue(all(isinstance(x, float) for x in result))

    def test_word_distance_private(self):
        # Accessing the "private" method for completeness
        wd = self.word_distance._WordDistance__word_distance
        self.assertEqual(wd('apple', 'apple'), 5)
        self.assertEqual(wd('apple', 'apxle'), 2)
        self.assertEqual(wd('apple', 'zzzzz'), 0)
        self.assertEqual(wd('apple', 'app'), 3)
        self.assertEqual(wd('app', 'apple'), 3)
