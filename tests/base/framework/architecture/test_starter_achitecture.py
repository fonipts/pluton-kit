import unittest
from unittest.mock import patch

from plutonkit.framework.architecture.starter_architecture import StarterArchitecture

class TestStarterArchitecture(unittest.TestCase):
    def setUp(self):
        self.directory = "/tmp"
        self.project_name = "SampleProject"
        self.sa = StarterArchitecture(self.directory, self.project_name)

    def test_initialization(self):
        self.assertEqual(self.sa.directory, self.directory)
        self.assertEqual(self.sa.project_name, self.project_name)
        self.assertEqual(self.sa.folder_name, "")

    def test_set_folder_name(self):
        self.sa.set_folder_name("myfolder")
        self.assertEqual(self.sa.folder_name, "myfolder")

    @patch("plutonkit.framework.architecture.starter_architecture.generate_project_folder_cwd")
    @patch("plutonkit.framework.architecture.starter_architecture.write_file_content")
    def test_execute_success(self, mock_write, mock_gen_folder):
        self.sa.set_folder_name("myfolder")
        self.sa.execute()
        mock_gen_folder.assert_called_with("myfolder")
        self.assertEqual(mock_write.call_count, 2)
        args1 = mock_write.call_args_list[0][0]
        self.assertIn("README.md", args1)
        args2 = mock_write.call_args_list[1][0]
        self.assertIn("architecture.yaml", args2)  # ARCHITECTURE_DETAILS_FILE default
        self.assertIn(self.directory, args1)
        self.assertIn(self.directory, args2)

    def test_get_architecture_content(self):
        content = self.sa._get_architecture_content()
        self.assertIn("name:", content)
        self.assertIn("files:", content)
