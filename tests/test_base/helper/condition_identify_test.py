from plutonkit.management.logic.ConditionIdentify import ConditionIdentify
import unittest

class TestConditionIdentify(unittest.TestCase):
    def test_condition_valid(self):
        cond = ConditionIdentify('        choices.database == "postgres"', {'choices': {'database': 'postgres'}})

        self.assertTrue(cond.validCond())

    def test_condition_invalid(self):
        cond = ConditionIdentify('        choices.database == "mysql"', {'choices': {'database': 'postgres'}})

        self.assertFalse(cond.validCond())
