import unittest

from plutonkit.framework.command.schema_command import SchemaCommand

class TestSchemaCommandEdge(unittest.TestCase):
    def test_empty_reference(self):
        sc = SchemaCommand({})
        errors = sc.get_error()
        self.assertEqual(errors, [])

    def test_script_with_multiple_invalids(self):
        sc = SchemaCommand({"script": {"foo": {"cmmand": "ls", "descriptin": "oops"}}})
        errors = sc.get_error()
        self.assertTrue(any("cmmand" in e or "descriptin" in e for e in errors))

    def test_group_deeply_nested(self):
        sc = SchemaCommand({
            "script": {
                "a": {
                    "command": "ls",
                    "group": {
                        "b": {
                            "commad": "ls"
                        }
                    }
                }
            }
        })
        errors = sc.get_error()
        self.assertTrue(any("commad" in e for e in errors))
