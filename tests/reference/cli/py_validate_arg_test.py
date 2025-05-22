
from plutonkit.framework.command.py_validate_arguments import PyValidateArguments

import unittest
import pytest


@pytest.fixture(scope="class")
def class_fixture(request):
    request.cls.command_test = PyValidateArguments(["command.py","test"],{"test":{
                "description":"",
                "func":None
                }})

@pytest.mark.usefixtures("class_fixture")
class TestPyValidateArg(unittest.TestCase):
    def test_python_file_exist(self):
       self.assertTrue(self.command_test.get_python_name_script())
    def test_get_index(self):
       self.assertEqual(self.command_test.get_index(), 1)
