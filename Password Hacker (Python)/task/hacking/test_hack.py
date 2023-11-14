import itertools as it
from unittest import TestCase

# Comment out next line as a workaround to fix the submission test
from hack import get_passwords

ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'

ONE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
       'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
       'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
TWO = (''.join(chars) for chars in it.product(ONE, repeat=2))
THREE = (''.join(chars) for chars in it.product(ONE, repeat=3))


class Test(TestCase):
    def test_get_passwords(self):
        actual = get_passwords()
        expected = it.chain(ONE, TWO, THREE)

        for password in expected:
            self.assertEqual(next(actual), password)