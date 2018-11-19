
set -e

if [ "$1" = "p2" ]; then
   ENV_DIR="p2"
   virtualenv -p python2 "$ENV_DIR"
   echo "Testing python2"
else
   ENV_DIR="p3"
   virtualenv -p python3 "$ENV_DIR"
   echo "Testing python3"
fi;

#activate environment
. "$ENV_DIR/bin/activate"


if [ "$2" = "from-github" ]; then
    pip install https://github.com/realead/exetest/zipball/master
else
    (python setup.py install)
fi;

pip freeze

#run tests
(cd tests && python -m unittest discover -s . -v)


#clean or keep the environment
if [ "$3" = "keep" ]; then
   echo "keeping enviroment $ENV_DIR"
else
   rm -r "$ENV_DIR"
fi;




