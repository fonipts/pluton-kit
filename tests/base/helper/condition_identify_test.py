from plutonkit.framework.tymplu.condition.condition_identify import ConditionIdentify
from plutonkit.framework.tymplu.condition.condition_delimiter import ConditionDelimiter

import unittest

class TestConditionIdentify(unittest.TestCase):
    def test_condition_invalid_status(self):
        cond = ConditionDelimiter('        choices.database = "postgres"')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'choices': {'database': 'postgres'}})

        self.assertTrue(len(cond_valid.errors)>0)

    def test_condition_valid(self):
        cond = ConditionDelimiter('        choices.database == "postgres"')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'choices': {'database': 'postgres'}})

        self.assertTrue(cond_valid.validate())

    def test_condition_w_dict_valid(self):

        cond = ConditionDelimiter('        choices.database == choices.local')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'choices': {'database': 'postgres','local': 'postgres'}})

        self.assertTrue(cond_valid.validate())

    def test_condition_w_dict_invalid(self):

        cond = ConditionDelimiter('        choices.database == choices.local')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'choices': {'database': 'postgres','local': 'postgresss'}})
        self.assertFalse(cond_valid.validate())

    def test_condition_noteq_invalid(self):

        cond = ConditionDelimiter('     choices.database != "mysql"')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'choices': {'database': 'postgres'}})
        self.assertTrue(cond_valid.validate())

    def test_condition_valid_greater(self):

        cond = ConditionDelimiter('num.one < num.two')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'num': {'one': 1, 'two': 2}})
        self.assertTrue(cond_valid.validate())

    def test_condition_valid_less(self):

        cond = ConditionDelimiter('num.two > num.one')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'num': {'one': 1, 'two': 2}})
        self.assertTrue(cond_valid.validate())

    def test_condition_valid_greater_than(self):

        cond = ConditionDelimiter('num.one <= num.two')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'num': {'one': 1, 'two': 2}})
        self.assertTrue(cond_valid.validate())

    def test_condition_valid_less_than(self):
        cond = ConditionDelimiter('num.two >= num.one')
        cond_valid = ConditionIdentify(cond.arg_list,cond.error_recording, {'num': {'one': 1, 'two': 2}})
        self.assertTrue(cond_valid.validate())
