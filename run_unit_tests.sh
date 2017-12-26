
export PYTHONPATH="${PYTHONPATH}:.."
(cd tests && python2.7 -m unittest discover -s . -v)

