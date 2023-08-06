"""
Tests calculating.
"""
import unittest
import verbcalc


class TestCalculate(unittest.TestCase):
    """
    Tests calculate function.
    """
    def test_calculations(self):
        self.assertEqual(verbcalc.calculate('2 plus 2', silent=True), '4')
        self.assertEqual(verbcalc.calculate
                         ('what is 2 minus 2', silent=True), '0')
        self.assertEqual(verbcalc.calculate
                         ('calculate 2 times 2', silent=True), '4')
        self.assertEqual(verbcalc.calculate
                         ('2 divided by 2', silent=True), '1')
        self.assertEqual(verbcalc.calculate
                         ('2 to the power of 2', silent=True), '4')
        self.assertEqual(verbcalc.calculate
                         ('Absolute value of -2', silent=True), '2')
        self.assertEqual(verbcalc.calculate
                         ('2 mod 2', silent=True), '0')
        self.assertEqual(verbcalc.calculate('2 root of 4', silent=True), '2')
        self.assertEqual(verbcalc.calculate('3 root of 27', silent=True), '3')
        self.assertEqual(verbcalc.calculate
                         ('2 divided by 0', silent=True),
                         'You cannot divide by zero!')
        self.assertEqual(verbcalc.calculate
                         ('2 plus 2 minus 1', silent=True), '3')
        self.assertEqual(verbcalc.calculate('2 2'),
                         'Your expression is invalid')


if __name__ == '__main__':
    unittest.main()
