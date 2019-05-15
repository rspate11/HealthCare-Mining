echo "***** this script sets up the project on home of the user who runs it ie. on ~ *****"
# upgrade pip
pip3 install --user --upgrade pip

# install virtualenv
pip3 install venv

# create a virtual environment
virtualenv venv

# set the python interpreter
virtualenv -p /usr/bin/python3 venv

# activate the venv
source venv/bin/activate

# install all pip dependencies
pip install -r requirements.txt

# run the django server
pushd -n $(pwd)
cd swmdjango
python manage.py runserver
popd
