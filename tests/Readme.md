# Unit test
## commmand
python -m unittest tests
pylint ./plutonkit/ --disable=missing-docstring
autopep8 --in-place --recursive ./plutonkit/
python -m unittest tests/test_base/helper/*.py
