import unittest
from unittest.mock import patch, MagicMock
from plutonkit.command.action.clone_project import CloneProject
from plutonkit.framework.exception.validation_exception import ValidationException

class TestCloneProject(unittest.TestCase):
    def setUp(self):
        self.argv = ["plutonkit", "clone_project", "source=foo.yaml"]
        self.clone_project = CloneProject(self.argv)

    def test_comment(self):
        self.assertEqual(self.clone_project.comment(), "Clone your project from project.yaml file")

    def test_execute_missing_source(self):
        clone = CloneProject(["plutonkit", "clone_project"])
        with self.assertRaises(ValidationException):
            clone.execute()

    @patch("plutonkit.command.action.clone_project.get_arg_cmd_value", return_value={})
    def test_execute_source_not_in_args(self, mock_get_arg_cmd_value):
        clone = CloneProject(["plutonkit", "clone_project", "other=val"])
        with self.assertRaises(ValidationException):
            clone.execute()

    @patch("plutonkit.command.action.clone_project.get_arg_cmd_value", return_value={"source": "foo.yaml"})
    @patch.object(CloneProject, "acces_lobby_blueprint")
    def test_execute_valid(self, mock_access, mock_get_arg_cmd_value):
        self.clone_project.execute()
        mock_access.assert_called_with("foo.yaml")

    @patch("plutonkit.command.action.clone_project.ArchitectureRequest")
    @patch("plutonkit.command.action.clone_project.load", return_value={"blueprint": "x", "default_choices": {}})
    @patch.object(CloneProject, "project_details_execute")
    def test_access_lobby_blueprint_valid(self, mock_pde, mock_load, mock_arch):
        mock_arch.return_value.isValidReq = True
        mock_arch.return_value.getValidReq = "abc"
        self.clone_project.acces_lobby_blueprint("foo.yaml")
        mock_pde.assert_called_with("x", {})

    @patch("plutonkit.command.action.clone_project.ArchitectureRequest")
    def test_access_lobby_blueprint_invalid(self, mock_arch):
        mock_arch.return_value.isValidReq = False
        mock_arch.return_value.errorMessage = "err!"
        with self.assertRaises(ValidationException):
            self.clone_project.acces_lobby_blueprint("foo.yaml")

    @patch("plutonkit.command.action.clone_project.input", return_value="ab")
    @patch("plutonkit.command.action.clone_project.print")
    @patch("plutonkit.command.action.clone_project.sys.exit")
    def test_project_details_execute_short_name(self, mock_exit, mock_print, mock_input):
        clone = CloneProject(["plutonkit", "clone_project", "source=foo.yaml"])
        inquiry_val = {}
        clone.project_details_execute("remote_blueprint", inquiry_val)
        mock_print.assert_any_call("Please specify atleast three char")
        mock_exit.assert_called_with(0)
