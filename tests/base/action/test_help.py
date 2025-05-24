import unittest
from unittest.mock import patch, MagicMock
from plutonkit.command.action.help import Help

class TestHelp(unittest.TestCase):
    def setUp(self):
        self.h = Help(["plutonkit", "help"])

    def test_comment(self):
        self.assertEqual(self.h.comment(), "To see all available commands")

    @patch("plutonkit.command.action.help.ACTIONS", {"foo": MagicMock(comment=lambda: "bar")})
    @patch("builtins.print")
    @patch("sys.exit")
    def test_execute(self, mock_exit, mock_print):
        self.h.execute()
        mock_print.assert_called()
        mock_exit.assert_called_with(0)
