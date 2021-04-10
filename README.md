# LensServer
Python server for Pickhacks 2021 Lens project


python3 -m venv auth
source auth/bin/activate
pip install -r requirements.txt
pip install flask flask-sqlalchemy flask-login cassandra-driver
export FLASK_APP=project
export FLASK_DEBUG=1

deactivate