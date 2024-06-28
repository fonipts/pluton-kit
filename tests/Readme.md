#Unit test
## commmand
python -m unittest tests
pylint ./src/ --disable=missing-docstring
autopep8 --in-place --recursive ./src/plutonkit/