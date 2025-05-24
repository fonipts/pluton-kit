import unittest
from unittest.mock import patch, MagicMock
from plutonkit.command.action.validate_blueprint import ValidateBlueprint
from plutonkit.framework.exception.validation_exception import ValidationException

class TestValidateBlueprint(unittest.TestCase):
    def setUp(self):
        self.val = ValidateBlueprint(["plutonkit", "validate_blueprint", "foo.yaml"])

    def test_comment(self):
        self.assertEqual(self.val.comment(), "Check your blueprint before issue before deploying")

    @patch("plutonkit.command.action.validate_blueprint.ArchitectureRequest")
    @patch("plutonkit.command.action.validate_blueprint.load", return_value={})
    @patch("plutonkit.command.action.validate_blueprint.ReviewBlueprint")
    @patch("builtins.print")
    @patch("sys.exit")
    def test_execute_no_error(self, mock_exit, mock_print, mock_rb, mock_load, mock_arch):
        mock_arch.return_value.isValidReq = True
        mock_arch.return_value.getValidReq = "abc"
        mock_rb.return_value.verify_blueprint.return_value = {"error_message": []}
        self.val.execute()
        mock_print.assert_called_with("No error found")
        mock_exit.assert_called_with(0)

    @patch("plutonkit.command.action.validate_blueprint.ArchitectureRequest")
    @patch("plutonkit.command.action.validate_blueprint.load", return_value={})
    @patch("plutonkit.command.action.validate_blueprint.ReviewBlueprint")
    def test_execute_with_error(self, mock_rb, mock_load, mock_arch):
        mock_arch.return_value.isValidReq = True
        mock_arch.return_value.getValidReq = "abc"
        mock_rb.return_value.verify_blueprint.return_value = {"error_message": ["err"]}
        with self.assertRaises(ValidationException):
            self.val.execute()

    @patch("plutonkit.command.action.validate_blueprint.ArchitectureRequest")
    def test_execute_invalid_arch(self, mock_arch):
        mock_arch.return_value.isValidReq = False
        mock_arch.return_value.errorMessage = "err"
        with self.assertRaises(ValidationException):
            self.val.execute()

    def test_execute_no_argument(self):
        val = ValidateBlueprint(["plutonkit", "validate_blueprint"])
        with self.assertRaises(ValidationException):
            val.execute()
