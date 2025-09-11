from plutonkit.framework.tymplu.condition.condition_delimiter import ConditionDelimiter
import unittest

class TestConditionDelimiter(unittest.TestCase):
    def test_condition_valid(self):
        cond = ConditionDelimiter('        choices.database == "postgres" && choices.redis == "local"')

        self.assertTrue(len(cond.arg_list)>0)
        self.assertTrue(len(cond.error_recording)<=0)

    def test_condition_invalid(self):
        cond = ConditionDelimiter('        choices.database == "postgres"   choices.redis == "local"')
        self.assertTrue(len(cond.arg_list)<=0)
        self.assertTrue(len(cond.error_recording)>0)
