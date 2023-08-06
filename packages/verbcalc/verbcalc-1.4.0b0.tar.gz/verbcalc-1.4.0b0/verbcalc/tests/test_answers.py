"""
    Tests how custom answers work.
"""
import unittest
from unittest.mock import patch
from random import Random
from verbcalc.core.answers import CustomAnswers


class TestCustomAnswers(unittest.TestCase):
    """
    Tests how custom answers work.
    """
    def setUp(self):
        self.random = Random(666)

    def test_default_phrase(self):
        self.assertEqual(CustomAnswers().get_phrase(default=True),
                         'The result is')

    # pylint: disable=W0212
    @patch('verbcalc.core.answers.random')
    def test_random_phrase(self, random):
        phrases = CustomAnswers()
        self.assertEqual(phrases.get_phrase() in phrases._answers, True)

        random.randrange._mock_side_effect = self.random.randrange
        self.assertEqual(CustomAnswers().get_phrase(), 'The total is')


if __name__ == '__main__':
    unittest.main()
