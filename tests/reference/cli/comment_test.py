
from .base import command,create_achitecture,create_project,help,validate_blueprint

import unittest

class TestComment(unittest.TestCase):

    def test_command(self):
        self.assertEqual(command.comment(), 'Executing command using plutonkit')
    def test_create_achitecture(self):
        self.assertEqual(create_achitecture.comment(), 'Create your first architecture')
    def test_create_project(self):
        self.assertEqual(create_project.comment(), 'Start creating your project in our listed framework or clone if you have project.yaml in source')
    def test_help(self):
        self.assertEqual(help.comment(), 'To see all available commands')
    def test_validate_blueprint(self):
        self.assertEqual(validate_blueprint.comment(), 'Check your blueprint before issue before deploying')
