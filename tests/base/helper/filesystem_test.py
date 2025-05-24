import unittest
import os
from unittest.mock import patch, mock_open, MagicMock

import plutonkit.helper.filesystem as filesystem

class TestFilesystem(unittest.TestCase):
    def test_is_glob(self):
        self.assertTrue(filesystem.is_glob("*file"))
        self.assertTrue(filesystem.is_glob("[abc]"))
        self.assertTrue(filesystem.is_glob("?name"))
        self.assertFalse(filesystem.is_glob("file.txt"))

    def test_default_project_name(self):
        self.assertEqual(filesystem.default_project_name("foo"), "foo")

    @patch("os.getcwd", return_value="/tmp/testcwd")
    @patch("os.makedirs")
    def test_generate_project_folder_cwd(self, mock_makedirs, mock_getcwd):
        filesystem.generate_project_folder_cwd("myproject")
        mock_makedirs.assert_called_with("/tmp/testcwd/myproject")

    @patch("os.getcwd", return_value="/tmp/testcwd")
    @patch("builtins.open", new_callable=mock_open)
    @patch("yaml.dump", return_value="yaml: content")
    def test_create_yaml_file(self, mock_yaml_dump, mock_open_func, mock_getcwd):
        filesystem.create_yaml_file("myproj", "config.yaml", {"a": 1})
        mock_open_func.assert_called_with("/tmp/testcwd/myproj/config.yaml", "w", encoding="utf-8")
        mock_yaml_dump.assert_called_with({"a": 1}, default_flow_style=False)
        handle = mock_open_func()
        handle.write.assert_called_with("yaml: content")
        handle.close.assert_called()

    @patch("plutonkit.helper.filesystem.convert_shortcode", side_effect=lambda c, a: c)
    @patch("plutonkit.helper.filesystem.convert_template", side_effect=lambda c, a, b: c + "_tpl")
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    @patch("os.path.dirname", return_value="dir1/dir2")
    @patch("os.path.splitext", return_value=("file", ".tpl"))
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("builtins.open", new_callable=mock_open)
    def test_write_file_content_as_template(
        self, mock_open_func, mock_path_join, mock_splitext, mock_dirname, mock_exists, mock_makedirs,
        mock_convert_tmpl, mock_convert_shortcode
    ):
        filesystem.write_file_content("pdir", "fname", "dir1/dir2/file.tpl", "content", args={"foo": "bar"}, block=None)
        mock_makedirs.assert_called()
        handle = mock_open_func()
        handle.write.assert_called_with("content_tpl")
        handle.close.assert_called()

    @patch("plutonkit.helper.filesystem.convert_shortcode", side_effect=lambda c, a: c)
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    @patch("os.path.dirname", return_value="")
    @patch("os.path.splitext", return_value=("file", ".txt"))
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("builtins.open", new_callable=mock_open)
    def test_write_file_content_regular(
        self, mock_open_func, mock_path_join, mock_splitext, mock_dirname, mock_exists, mock_makedirs, mock_convert_shortcode
    ):
        filesystem.write_file_content("pdir", "fname", "file.txt", "content", args={"foo": "bar"})
        handle = mock_open_func()
        handle.write.assert_called_with("content")
        handle.close.assert_called()

    @patch("plutonkit.helper.filesystem.convert_shortcode", side_effect=lambda c, a: c)
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    @patch("os.path.dirname", return_value="dir1")
    @patch("os.path.splitext", return_value=("dir1/file.tpl", ""))
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    @patch("plutonkit.helper.filesystem.convert_template", side_effect=lambda c, a, b: c + "_tpl")
    @patch("builtins.open", new_callable=mock_open)
    def test_write_file_content_template_in_name(
        self, mock_open_func, mock_convert_tmpl, mock_path_join, mock_splitext, mock_dirname, mock_exists, mock_makedirs, mock_convert_shortcode
    ):
        filesystem.write_file_content("pdir", "fname", "dir1/file.tpl", "content", args={"foo": "bar"})
        handle = mock_open_func()
        handle.write.assert_called_with("content_tpl")
        handle.close.assert_called()
