import os
import unittest

from core import os_utils


class TestOsUtils(unittest.TestCase):

    def test_find_file(self):
        native_path = os.getcwd() + "\\test_native"
        expected = native_path + "\\Sounds\\arrow_body_hit_01.ogg"
        actual = os_utils.find_first_file(native_path, "arrow_body_hit_01.ogg")
        self.assertEqual(expected, actual, "expected: {0}\nactual: {1}".format(expected, actual))

    if __name__ == '__main__':
        unittest.main()
