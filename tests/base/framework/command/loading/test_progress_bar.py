# python

import sys
import pytest

from plutonkit.framework.command.loading.progress_bar import ProgressBar


def test_progress_bar_default_init():
    pb = ProgressBar()
    assert pb.width == 50
    assert pb.fill == "."
    assert pb.empty == " "
    assert pb.limit_percentage == 100
    assert pb.load_message == "Progress"

def test_progress_bar_custom_init():
    pb = ProgressBar(width=10, fill="#", empty="-", limit_percentage=20, load_message="Load")
    assert pb.width == 10
    assert pb.fill == "#"
    assert pb.empty == "-"
    assert pb.limit_percentage == 20
    assert pb.load_message == "Load"

@pytest.mark.parametrize("i,expected_percent", [
    (0, "0.0%"),
    (50, "50.0%"),
    (100, "100.0%"),
])
def test_progress_bar_update_output(capsys, i, expected_percent):
    pb = ProgressBar(width=10, fill="*", empty="-", limit_percentage=100, load_message="Test")
    pb.update(i)
    captured = capsys.readouterr().out
    assert f"Test[" in captured
    assert expected_percent in captured

def test_progress_bar_update_over_limit_prints_newline(capsys):
    pb = ProgressBar(width=10, limit_percentage=10)
    pb.update(15)
    captured = capsys.readouterr().out
    assert "\n" in captured

def test_progress_bar_completed_prints_newline(capsys):
    pb = ProgressBar()
    pb.completed()
    captured = capsys.readouterr().out
    assert captured == "\n"

def test_progress_bar_integration_sequence(capsys):
    pb = ProgressBar(width=5, fill="*", empty=".", limit_percentage=5, load_message="Run")
    for i in range(6):
        pb.update(i)
    pb.completed()
    captured = capsys.readouterr().out
    # Should have 6 progress bar updates and a final newline
    assert captured.count("Run[") == 6
    assert captured.endswith("\n")
