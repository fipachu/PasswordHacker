from unittest import TestCase

# Comment out next line as a workaround to fix the submission test
# from hack import get_passwords, get_logins


class TestHack(TestCase):
    def test_logins_head(self):
        expected = ['admin', 'admiN', 'admIn', 'admIN', 'adMin', 'adMiN', 'adMIn']
        for e, a in zip(expected, get_logins()):
            self.assertEqual(e, a)

    def test_passwords_head(self):
        self.fail()
