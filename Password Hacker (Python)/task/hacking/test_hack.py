import itertools
import itertools as it
from unittest import TestCase

# Comment out next line as a workaround to fix the submission test
from hack import get_passwords

FIRST_TWO = ['123456', 'password']


class TestGetPassword(TestCase):
    def test_first_two(self):
        actual = get_passwords()
        expected = it.chain(FIRST_TWO)

        for password in expected:
            self.assertEqual(next(actual), password)

    def test_all(self):
        self.fail('Not implemented!')
