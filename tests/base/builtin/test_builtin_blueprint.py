import unittest
from plutonkit.built_in_module.blueprint import PLBlueprint

class TestPLBlueprint(unittest.TestCase):
    def setUp(self):
        self.bp = PLBlueprint()

    def test_block_registration(self):
        @self.bp.block("my_block")
        def foo():
            return 10

        self.assertIn("my_block", self.bp.local_block)
        self.assertEqual(self.bp.local_block["my_block"]["func"](), 10)

    def test_script_registration(self):
        @self.bp.script("my_script")
        def bar():
            return "hello"

        script = next((s for s in self.bp.bootscript if s["name"] == "my_script"), None)
        self.assertIsNotNone(script)
        self.assertEqual(script["func"](), "hello")

    def test_get_execute(self):
        @self.bp.block("block1")
        def foo(): return 1
        @self.bp.script("script1")
        def bar(): return 2
        result = self.bp.get_execute()
        self.assertIn("block", result)
        self.assertIn("script", result)
        self.assertIsInstance(result["block"], dict)
        self.assertIsInstance(result["script"], list)
