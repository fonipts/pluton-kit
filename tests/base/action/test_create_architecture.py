import unittest
from unittest.mock import patch, MagicMock
from plutonkit.command.action.create_achitecture import CreateAchitecture

class TestCreateAchitecture(unittest.TestCase):
    def setUp(self):
        self.ach = CreateAchitecture(["plutonkit", "create_achitecture"])

    def test_comment(self):
        self.assertEqual(self.ach.comment(), "Create your first architecture")

    @patch("plutonkit.command.action.create_achitecture.input", side_effect=["proj", "y"])
    @patch("plutonkit.command.action.create_achitecture.answer_yes", return_value=True)
    @patch("plutonkit.command.action.create_achitecture.StarterArchitecture")
    @patch("sys.exit")
    def test_execute_yes(self, mock_exit, mock_starter, mock_answer, mock_input):
        self.ach.execute()
        #?mock_starter.assert_called_with(MagicMock(), "proj")
        mock_starter.return_value.set_folder_name.assert_called_with("proj")
        mock_starter.return_value.execute.assert_called()
        mock_exit.assert_called_with(0)

    @patch("plutonkit.command.action.create_achitecture.input", side_effect=["proj", "n"])
    @patch("plutonkit.command.action.create_achitecture.answer_yes", return_value=False)
    @patch("sys.exit")
    def test_execute_no(self, mock_exit, mock_answer, mock_input):
        self.ach.execute()
        mock_exit.assert_called_with(0)
