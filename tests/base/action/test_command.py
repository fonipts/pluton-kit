import unittest
from unittest.mock import patch, MagicMock, mock_open
from plutonkit.command.action.command import Command
from plutonkit.framework.exception.validation_exception import ValidationException
from plutonkit.framework.exception.warning_exception import WarningException

class TestCommand(unittest.TestCase):
    def setUp(self):
        self.argv = ["plutonkit", "command"]
        self.cmd = Command(self.argv)

    def test_comment(self):
        self.assertEqual(self.cmd.comment(), "Executing command using plutonkit")

    def test_modify_argv_index(self):
        self.assertEqual(self.cmd.modify_argv_index(5), self.cmd)
        self.assertEqual(self.cmd.index, 5)

    @patch("os.getcwd", return_value="/tmp")
    @patch("os.path.exists", return_value=False)
    def test_execute_missing_command_file(self, mock_exists, mock_getcwd):
        with self.assertRaises(ValidationException):
            self.cmd.execute()

    @patch("os.getcwd", return_value="/tmp")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=False)
    def test_execute_invalid_command_file(self, mock_isfile, mock_exists, mock_getcwd):
        with self.assertRaises(ValidationException):
            self.cmd.execute()

    @patch("os.getcwd", return_value="/tmp")
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="foo: bar")
    @patch("yaml.load", return_value={"env":{}, "foo":"bar"})
    @patch.object(Command, "command_start")
    def test_execute_valid(self, mock_start, mock_load, mock_open, mock_isfile, mock_exists, mock_getcwd):
        self.cmd.execute()
        mock_start.assert_called()

    @patch("plutonkit.command.action.command.StructureCommand")
    @patch("plutonkit.command.action.command.setEnvironmentVariable")
    def test_command_start_with_errors(self, mock_setenv, mock_struct):
        mock_struct.return_value.get_error.return_value = ["err"]
        with self.assertRaises(ValidationException):
            self.cmd.command_start({"env":{}}, "/tmp")

    @patch("plutonkit.command.action.command.StructureCommand")
    @patch("plutonkit.command.action.command.setEnvironmentVariable")
    def test_command_start_with_command_value(self, mock_setenv, mock_struct):
        sc = mock_struct.return_value
        sc.get_error.return_value = []
        sc.get_list_commands.return_value = {"foo": {"command": ["ls"], "chdir": "/tmp"}}
        cmd = Command(["plutonkit", "command", "foo"])
        with patch("os.chdir"), patch("plutonkit.command.action.command.pip_run_command"), patch("sys.exit") as mock_exit:
            cmd.command_start({"env":{}}, "/tmp")
            mock_exit.assert_called()

#?    @patch("plutonkit.command.action.command.StructureCommand")
#?    @patch("plutonkit.command.action.command.setEnvironmentVariable")
#?    def test_command_start_python_file(self, mock_setenv, mock_struct):
#?        sc = mock_struct.return_value
#?        sc.get_error.return_value = []
#?        sc.get_list_commands.return_value = {}
#?        cmd = Command(["plutonkit", "command", "foo"])
#?        with patch("os.path.isfile", return_value=True), \
#?             patch("plutonkit.command.action.command.PyValidateContent") as mock_pvc, \
#?             patch("sys.exit") as mock_exit, \
#?             patch("sys.path.append"), \
#?             patch("importlib.import_module") as mock_mod:
#?            mock_pvc.return_value.is_run_func_available.return_value = True
#?            cmd.command_start({"env":{}}, "/tmp")
#?            mock_mod.assert_called()
#?            mock_exit.assert_not_called()  # sys.exit is after mod.run()

    @patch("plutonkit.command.action.command.StructureCommand")
    @patch("plutonkit.command.action.command.setEnvironmentVariable")
    def test_command_start_warning_exception(self, mock_setenv, mock_struct):
        sc = mock_struct.return_value
        sc.get_error.return_value = []
        sc.get_list_commands.return_value = {}
        cmd = Command(["plutonkit", "command", "foo"])
        with patch("os.path.isfile", return_value=True), \
             patch("plutonkit.command.action.command.PyValidateContent") as mock_pvc:
            mock_pvc.return_value.is_run_func_available.return_value = False
            with self.assertRaises(WarningException):
                cmd.command_start({"env":{}}, "/tmp")
