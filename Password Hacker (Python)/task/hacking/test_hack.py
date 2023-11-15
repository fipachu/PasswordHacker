from itertools import chain
from unittest import TestCase

# Comment out next line as a workaround to fix the submission test
# from hack import get_passwords


FIRST_FIVE = ['123456', 'password', 'passworD', 'passwoRd', 'passwoRD', ]


class TestGetPassword(TestCase):
    def test_head(self):
        actual = get_passwords()
        expected = FIRST_FIVE

        for password in expected:
            self.assertEqual(next(actual), password)
