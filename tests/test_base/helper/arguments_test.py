from plutonkit.helper.arguments import get_dict_value
import unittest

class TestAruments(unittest.TestCase):
    def test_convert_arguments_valid(self):
        self.assertEqual(get_dict_value(["name"],{"name":"FOO"}), 'FOO')

    def test_convert_arguments_invalid(self):
        self.assertNotEqual(get_dict_value(["name"],{"name":"FOO"}), 'FO')
 