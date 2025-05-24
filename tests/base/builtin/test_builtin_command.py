import unittest
from plutonkit.built_in_module.command import PLCommand

class TestPLCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = PLCommand()

    def test_cli_registration(self):
        @self.cmd.cli("my_cmd", description="desc")
        def foo():
            return "ran"
        self.assertIn("my_cmd", self.cmd.local_cli)
        self.assertEqual(self.cmd.local_cli["my_cmd"]["description"], "desc")
        self.assertEqual(self.cmd.local_cli["my_cmd"]["func"](), "ran")

    def test_cli_decorator_default_name(self):
        @self.cmd.cli(description="desc2")
        def bar():
            return 99
        self.assertIn("bar", self.cmd.local_cli)
        self.assertEqual(self.cmd.local_cli["bar"]["description"], "desc2")
        self.assertEqual(self.cmd.local_cli["bar"]["func"](), 99)

