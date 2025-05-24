import unittest
from unittest.mock import patch
from plutonkit.framework.terminal.inquiry_terminal import InquiryTerminal

class TestInquiryTerminal(unittest.TestCase):
    def test_init_and_state_methods(self):
        it = InquiryTerminal([{"name": "n", "question": "q", "type": "input"}])
        self.assertEqual(it.get_answer(), {})
        self.assertTrue(it.is_continue())
        self.assertFalse(it.is_terminate())

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", return_value="answer")
    def test_input_type_sets_answer(self, mock_input):
        choices = [{"name": "foo", "question": "What's your name", "type": "input", "default": "bar"}]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["foo"], "answer")
        self.assertTrue(it.is_terminate())

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", return_value="")
    def test_input_type_default(self, mock_input):
        choices = [{"name": "foo", "question": "What's your name", "type": "input", "default": "bar"}]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["foo"], "bar")

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", return_value="2")
    @patch("builtins.print")
    def test_single_choice(self, mock_print, mock_input):
        choices = [{
            "name": "color",
            "question": "Pick one",
            "type": "single_choice",
            "option": ["red", "green", "blue"],
        }]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["color"], "green")

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", return_value="1,3")
    @patch("builtins.print")
    def test_multiple_choice(self, mock_print, mock_input):
        choices = [{
            "name": "fruits",
            "question": "Select fruits",
            "type": "multiple_choice",
            "option": ["apple", "banana", "cherry"],
        }]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["fruits"], "1,3")

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", side_effect=["bad", "1"])
    @patch("builtins.print")
    def test_single_choice_invalid_retry(self, mock_print, mock_input):
        choices = [{
            "name": "pet",
            "question": "Pick a pet",
            "type": "single_choice",
            "option": ["dog", "cat"],
        }]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["pet"], "dog")

    @patch("plutonkit.framework.terminal.inquiry_terminal.input", side_effect=["bad", "2"])
    @patch("builtins.print")
    def test_multiple_choice_invalid_retry(self, mock_print, mock_input):
        choices = [{
            "name": "nums",
            "question": "Pick numbers",
            "type": "multiple_choice",
            "option": ["one", "two"],
        }]
        it = InquiryTerminal(choices)
        it.execute()
        self.assertEqual(it.get_answer()["nums"], "2")

    def test_empty_choices_sets_terminate(self):
        it = InquiryTerminal([])
        it.execute()
        self.assertTrue(it.is_terminate())
