import unittest
from unittest.mock import patch, MagicMock
from plutonkit.framework.blueprint.generate_blueprint import FrameworkBluePrint

class TestFrameworkBluePrint(unittest.TestCase):
    def setUp(self):
        self.bp = FrameworkBluePrint("../../../raw/test")
        self.bp.folder_name = "test_folder"
        self.bp.directory = "../../../raw/py"

    def test_set_folder_name(self):
        self.bp.set_folder_name("abc")
        self.assertEqual(self.bp.folder_name, "abc")

    @patch("plutonkit.framework.blueprint.generate_blueprint.ArchitectureRequest")
    @patch("plutonkit.framework.blueprint.generate_blueprint.generate_project_folder_cwd")
    @patch("plutonkit.framework.blueprint.generate_blueprint.load")
    def test_execute_clone_project_valid(self, mock_load, mock_genfolder, mock_archreq):
        mock_arch = MagicMock(isValidReq=True, getValidReq="{}")
        mock_archreq.return_value = mock_arch
        mock_load.return_value = {"files": {}, "script": {}, "bootscript": [], "env": {}}
        with patch.object(self.bp, "_bootloader_project") as mock_boot:
            self.bp.execute_clone_project(ans_ref={})
            mock_boot.assert_called_once()

    @patch("plutonkit.framework.blueprint.generate_blueprint.ArchitectureRequest")
    def test_execute_clone_project_invalid(self, mock_archreq):
        mock_arch = MagicMock(isValidReq=False, errorMessage="Error")
        mock_archreq.return_value = mock_arch
        with self.assertRaises(SystemExit):
            self.bp.execute_clone_project(ans_ref={})

    def test_script_template(self):
        configs = {"myscript": {"command": ["echo {{foo}}"], "description": "desc"}}
        args = {"foo": "bar"}
        result = self.bp._script_template(configs, args)
        self.assertEqual(result["myscript"]["command"][0], "echo bar")

    @patch("plutonkit.framework.blueprint.generate_blueprint.PyValidateContent")
    @patch("plutonkit.framework.blueprint.generate_blueprint.importlib.import_module")
    @patch("os.path.isfile", return_value=True)
    def test_review_blueprint_script_ok(self, mock_isfile, mock_import, mock_validate):
        mock_validate.return_value.get_class_import.return_value = {"Blueprint": "Blueprint"}
        mock_validate.return_value.get_class_call.return_value = {"Blueprint": "Blueprint"}
        mock_validate.return_value.is_run_func_available.return_value = False
        mock_mod = MagicMock()
        mock_import.return_value = mock_mod
        self.bp.path = "../../../raw/py"
        self.assertIsNone(self.bp._review_blueprint_script())

    def test_files_handles_empty(self):
        # Should not raise with empty files
        self.bp.arch_req = MagicMock(getBlob=lambda x: [])
        self.bp._files({"default": []}, {})

  #?  @patch("plutonkit.framework.blueprint.generate_blueprint.write_file_content")
  #?  def test_files_with_valid_file(self, mock_write):
  #?      mock_blob = [MagicMock(isObjFile=lambda: True, value={"file": "foo"}, get_save_files=lambda: ["foo"])]
  #?      mock_arch_req = MagicMock(getBlob=lambda x: mock_blob, getFiles=lambda f: {"is_valid": True, "content": "abc"})
  #?      self.bp.arch_req = mock_arch_req
  #?      self.bp._files({"default": ["somefile"]}, {})
  #?      mock_write.assert_called()

    @patch("plutonkit.framework.blueprint.generate_blueprint.write_file_content")
    def test_files_with_invalid_file(self, mock_write):
        mock_blob = [MagicMock(isObjFile=lambda: True, value={"file": "foo"}, get_save_files=lambda: ["foo"])]
        mock_arch_req = MagicMock(getBlob=lambda x: mock_blob, getFiles=lambda f: {"is_valid": False, "content": "abc"})
        self.bp.arch_req = mock_arch_req
        self.bp._files({"default": ["somefile"]}, {})
        mock_write.assert_not_called()
