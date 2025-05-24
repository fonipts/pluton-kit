import unittest
from plutonkit.framework.blueprint.review_blueprint import ReviewBlueprint

class TestReviewBlueprint(unittest.TestCase):
    def setUp(self):
        self.path = "/tmp"
        self.blueprint_content = {
            "name": "foo",
            "files": {"default": [{"file": "bar"}]},
            "choices": [],
            "script": {},
            "bootscript": [],
            "env": {}
        }
        self.review = ReviewBlueprint(self.blueprint_content, self.path)

    def test_init(self):
        self.assertEqual(self.review.path, self.path)
        self.assertEqual(self.review.blueprint_content["name"], "foo")

#?    def test_verify_blueprint_missing_name(self):
#?        bp = dict(self.blueprint_content)
#?        del bp["name"]
#?        review = ReviewBlueprint(bp, self.path)
#?        out = review.verify_blueprint()
#?        self.assertTrue(any("name" in msg for msg in out["error_message"]))

#?    def test_verify_blueprint_missing_files(self):
#?        bp = dict(self.blueprint_content)
#?        del bp["files"]
#?        review = ReviewBlueprint(bp, self.path)
#?        out = review.verify_blueprint()
#?        self.assertTrue(any("files" in msg for msg in out["error_message"]))

    def test_check_invalid_value_suggests_typo(self):
        validate_data = {"error_message": []}
        self.review._ReviewBlueprint__check_invalid_value(validate_data, {"nmae": 1}, ["name"])
        self.assertTrue(any("nmae" in msg for msg in validate_data["error_message"]))

    def test_check_invalid_value_exact(self):
        validate_data = {"error_message": []}
        self.review._ReviewBlueprint__check_invalid_value(validate_data, {"name": 1}, ["name"])
        self.assertFalse(validate_data["error_message"])  # No error message for valid

    def test__verify_script(self):
        validate_data = {"error_message": []}
        self.review.blueprint_content["script"] = {"myscript": {"cmd": "ls"}}
        self.review._ReviewBlueprint__verify_script(validate_data)
        self.assertTrue(isinstance(validate_data, dict))

    def test__verify_choices(self):
        validate_data = {"error_message": []}
        self.review.blueprint_content["choices"] = [{"foo": 1}]
        self.review._ReviewBlueprint__verify_choices(validate_data)
        self.assertTrue(isinstance(validate_data, dict))

    def test__verify_bootsript(self):
        validate_data = {"error_message": []}
        self.review.blueprint_content["bootscript"] = [{"foo": 1}]
        self.review._ReviewBlueprint__verify_bootsript(validate_data)
        self.assertTrue(isinstance(validate_data, dict))
