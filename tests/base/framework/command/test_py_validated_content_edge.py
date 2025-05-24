import unittest
from unittest.mock import patch, mock_open

from plutonkit.framework.command.py_validate_content import PyValidateContent

class TestPyValidateContentEdge(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_file(self, mock_file):
        pvc = PyValidateContent("fakefile.py")
        self.assertFalse(pvc.is_run_func_available())
        self.assertEqual(pvc.get_class_import(), {})
        self.assertEqual(pvc.get_class_call(), {})

    @patch("builtins.open", new_callable=mock_open, read_data="from plutonkit import Blueprint\nX = Blueprint()\ndef foo(): pass\n")
    def test_multiple_class_calls(self, mock_file):
        pvc = PyValidateContent("fake.py")
        calls = pvc.get_class_call()
        self.assertIn("Blueprint", calls)

    @patch("builtins.open", new_callable=mock_open, read_data="from plutonkit import Blueprint as BP\n")
    def test_alias_import(self, mock_file):
        pvc = PyValidateContent("fake.py")
        imports = pvc.get_class_import()
        self.assertIn("Blueprint", imports)
        self.assertEqual(imports["Blueprint"], "BP")
