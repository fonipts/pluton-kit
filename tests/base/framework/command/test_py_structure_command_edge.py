import unittest
from plutonkit.framework.command.structure_command import StructureCommand

class TestStructureCommandEdge(unittest.TestCase):
    def test_no_script(self):
        sc = StructureCommand({}, "/tmp")
        cmds = sc.get_list_commands()
        self.assertEqual(cmds, {})

    def test_chdir_is_missing(self):
        sc = StructureCommand({"script": {"myscript": {"command": "ls"}}}, "/tmp")
        cmds = sc.get_list_commands()
        for v in cmds.values():
            self.assertIn("chdir", v)
            self.assertEqual(v["chdir"], "/tmp")

    #?def test_chdir_is_list(self):
    #    sc = StructureCommand({"script": {"myscript": {"command": "ls", "chdir": ["foo", "bar"]}}}, "/tmp")
    #?    cmds = sc.get_list_commands()
    #?    for v in cmds.values():
    #?        self.assertIsInstance(v["chdir"], list)

    def test_env_var_replacement(self):
        sc = StructureCommand({
            "script": {"myscript": {"command": "echo {$FOO}"}},
            "environment": {"FOO": "baz"}
        }, "/tmp")
        cmds = sc.get_list_commands()
        for v in cmds.values():
            self.assertIn("baz", v["command"])
