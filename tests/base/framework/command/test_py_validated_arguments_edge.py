import unittest

from plutonkit.framework.command.py_validate_arguments import PyValidateArguments

def only_kw(x=1): pass
def no_args(): pass

class TestPyValidateArgumentsEdge(unittest.TestCase):
    #?def test_empty_argv(self):
    #?    pva = PyValidateArguments([], {})
    #?    self.assertEqual(pva.get_index(), 0)
    #?    self.assertEqual(pva.getcmd_name(), "")
    #?    self.assertEqual(pva.getcmd_arg(), [])
    #?    self.assertEqual(pva.getcmd_arg_validated(), ([], {}))
    #?    valid, msg = pva.validated_cmd_arg()
    #?    self.assertTrue(valid)  # No args, no funcs

    def test_index_nonmatching(self):
        pva = PyValidateArguments(["foo"], {})
        self.assertEqual(pva.get_index(), 0)

    def test_argument_details_no_func(self):
        pva = PyValidateArguments(["foo"], {})
        arg_list, arg_dict, ord_list = pva.get_argument_details()
        self.assertEqual(arg_list, [])
        self.assertEqual(arg_dict, [])
        self.assertEqual(ord_list, [])

    #?def test_argument_details_all_kw(self):
    #?    pva = PyValidateArguments(["plutonkit", "only_kw"], {"only_kw": {"func": only_kw}})
    #?    arg_list, arg_dict, ord_list = pva.get_argument_details()
    #?    self.assertIn("x", ord_list)
    #?    self.assertTrue(any("default" in a for a in arg_dict))

    def test_argument_details_no_args(self):
        pva = PyValidateArguments(["plutonkit", "no_args"], {"no_args": {"func": no_args}})
        arg_list, arg_dict, ord_list = pva.get_argument_details()
        self.assertEqual(arg_list, [])
        self.assertEqual(arg_dict, [])
        self.assertEqual(ord_list, [])
