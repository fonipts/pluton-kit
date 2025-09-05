import unittest
from unittest.mock import patch, MagicMock
from plutonkit.command.action.create_project import CreateProject
from plutonkit.framework.exception.validation_exception import ValidationException
from plutonkit.framework.exception.warning_exception import WarningException

class TestCreateProject(unittest.TestCase):
    def setUp(self):
        self.argv = ["plutonkit", "create_project"]
        self.proj = CreateProject(self.argv)

    def test_comment(self):
        self.assertEqual(self.proj.comment(), "Start creating your project in our listed framework or clone if you have project.yaml in source")

    def test_execute_no_args(self):
        with patch.object(self.proj, "acces_lobby_blueprint") as mock_access:
            self.proj.execute()
            mock_access.assert_called()

    @patch("plutonkit.command.action.create_project.get_arg_cmd_value", return_value={})
    def test_execute_invalid_source(self, mock_get_arg):
        proj = CreateProject(["plutonkit", "create_project", "foo=bar"])
        with self.assertRaises(ValidationException):
            proj.execute()

    @patch("plutonkit.command.action.create_project.get_arg_cmd_value", return_value={"source": "val"})
    @patch.object(CreateProject, "git_lobby_bluprint")
    def test_execute_git_lobby_bluprint(self, mock_git, mock_get_arg):
        proj = CreateProject(["plutonkit", "create_project", "source=val"])
        with patch("plutonkit.command.action.create_project.check_if_default_name", return_value=False):
            proj.execute()
            mock_git.assert_called_with("val")

    @patch("plutonkit.command.action.create_project.get_arg_cmd_value", return_value={"source": "val"})
    @patch.object(CreateProject, "project_details_execute")
    def test_execute_project_details_execute(self, mock_pde, mock_get_arg):
        proj = CreateProject(["plutonkit", "create_project", "source=val"])
        with patch("plutonkit.command.action.create_project.check_if_default_name", return_value=True):
            proj.execute()
            mock_pde.assert_called_with("val")

    @patch("plutonkit.command.action.create_project.git_name", return_value="foo")
    @patch.object(CreateProject, "project_details_execute")
    def test_git_lobby_bluprint_default(self, mock_pde, mock_git_name):
        with patch("plutonkit.command.action.create_project.VAR_DEFAULT_BLUEPRINT", ["foo"]):
            self.proj.git_lobby_bluprint("foo")
            mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.git_name", return_value="foo")
    @patch.object(CreateProject, "project_details_execute")
    def test_git_lobby_bluprint_value_error(self, mock_pde, mock_git_name):
        with patch("plutonkit.command.action.create_project.VAR_DEFAULT_BLUEPRINT", []):
            self.proj.git_lobby_bluprint("foo")
            mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.input", side_effect=["1"])
    @patch.object(CreateProject, "query_execute")
    def test_callback_execute(self, mock_query, mock_input):
        ref_val = {"details": {}, "command": []}
        step = [{"option_name": "foo", "name": "foo", "type": "t", "field_type": "f", "config": [], "question": "Q"}]
        self.proj.callback_execute(ref_val, "question", step)
        mock_query.assert_called()

    @patch("plutonkit.command.action.create_project.get_config", return_value={"framework": "foo"})
    @patch.object(CreateProject, "project_details_execute")
    def test_query_execute(self, mock_pde, mock_get_config):
        self.proj.query_execute({"dummy": "val"})
        mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.get_arg_cmd_value", return_value={"source": "val"})
    @patch.object(CreateProject, "project_details_execute")
    def test_execute_project_details_execute(self, mock_pde, mock_get_arg):
        proj = CreateProject(["plutonkit", "create_project", "source=val"])
        with patch("plutonkit.command.action.create_project.check_if_default_name", return_value=True):
            proj.execute()
            mock_pde.assert_called_with("val")

    @patch("plutonkit.command.action.create_project.git_name", return_value="foo")
    @patch.object(CreateProject, "project_details_execute")
    def test_git_lobby_bluprint_default(self, mock_pde, mock_git_name):
        with patch("plutonkit.command.action.create_project.VAR_DEFAULT_BLUEPRINT", ["foo"]):
            self.proj.git_lobby_bluprint("foo")
            mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.git_name", return_value="foo")
    @patch.object(CreateProject, "project_details_execute")
    def test_git_lobby_bluprint_value_error(self, mock_pde, mock_git_name):
        with patch("plutonkit.command.action.create_project.VAR_DEFAULT_BLUEPRINT", []):
            self.proj.git_lobby_bluprint("foo")
            mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.input", side_effect=["1"])
    @patch.object(CreateProject, "query_execute")
    def test_callback_execute(self, mock_query, mock_input):
        ref_val = {"details": {}, "command": []}
        step = [{"option_name": "foo", "name": "foo", "type": "t", "field_type": "f", "config": [], "question": "Q"}]
        self.proj.callback_execute(ref_val, "question", step)
        mock_query.assert_called()

    @patch("plutonkit.command.action.create_project.get_config", return_value={"framework": "foo"})
    @patch.object(CreateProject, "project_details_execute")
    def test_query_execute(self, mock_pde, mock_get_config):
        self.proj.query_execute({"dummy": "val"})
        mock_pde.assert_called()

    @patch("plutonkit.command.action.create_project.FrameworkBluePrint")
    @patch("builtins.input", return_value="myproject")
    @patch("sys.exit")
    def test_project_details_execute_valid(self, mock_exit, mock_input, mock_fb):
        mock_fb_instance = mock_fb.return_value
        self.proj.project_details_execute("remote_blueprint_url")
        mock_fb.assert_called_with("remote_blueprint_url")
        mock_fb_instance.set_folder_name.assert_called_with("myproject")
        mock_fb_instance.execute_create_project.assert_called_once()
        mock_exit.assert_called_once_with(0)

    @patch("builtins.input", return_value="ab")
    @patch("builtins.print")
    @patch("sys.exit")
    def test_project_details_execute_short_name(self, mock_exit, mock_print, mock_input):
        self.proj.project_details_execute("remote_blueprint_url")
        mock_print.assert_any_call("Please specify atleast three char")
        mock_exit.assert_called_with(0)
