# LensServer
Python server for Pickhacks 2021 Lens project

## A Flask API

This server uses Flask to accept HTTP messages from clients to interact with the Astra DataStax database. JSON messages are parsed and used to generate CQL to interact with the database. Flask then formats relevant information into a new JSON file and sends it back to the user.

## How to Run
Create a cheap server instance. Clone the project into a folder. Run the following commands:

```python3 -m venv auth
source auth/bin/activate
pip install -r requirements.txt
sudo apt install gunicorn
```
This willl install all the relevant tools and activate a Python virtual environment. To exit the venv, run:

`deactivate`

Finally, to start the server run:

`./run.sh`

## SSL Support - Future
In order for phones to interact with this server, we will need to enable SSL. We generated our own certificates in order to implement SSL, but since they are not trustworthy phones were unable to interact with the server. The web app was able to interact over SSL after the user trusted the certification.

Future versions of the server can get a legit signed certificate from a CA to allow the mobile app to function.

### Generate and Use SSL Certs
The first command generates the certificate and the private key to be used with gunicorn. 

```openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365```

The second runs gunicorn but forces HTTPS.

```gunicorn --certfile=cert.pem --keyfile=key.pem --bind :443 wsgi:app --preload```

## Database Layout
```
CREATE TABLE core.userdata
(
  username TEXT,
  bio TEXT,
  createdate TIMESTAMP, --default timestamp
  PRIMARY KEY (username)
);

CREATE TABLE core.uservotes
(
  postid UUID,
  username TEXT,
  upvoted BOOLEAN, --default false
  viewtime INT,
  PRIMARY KEY (postID, username)
);

CREATE TABLE core.posts
(
  postid UUID,
  parentid TEXT,
  title TEXT,
  author TEXT, --default user(username)
  content TEXT,
  contenttype TEXT,
  views INT, --default 0
  upvotes INT, --default 0
  downvotes INT,  --default 0 
  watchtime INT, --default 0
  dateposted TIMESTAMP, --default TIMESTAMP
  Primary KEY (postID),
);

CREATE TABLE core.comments
(
  postid UUID,
  author TEXT, --default user(username)
  content TEXT,
  views INT, --default 0
  upvotes INT, --default 0
  downvotes INT,  --default 0 
  watchtime INT, --default 0
  dateposted TIMESTAMP, --default TIMESTAMP
  Primary KEY (postID),
);

CREATE TABLE auth.users
(
  username TEXT,
  password TEXT,
);

CREATE TABLE core.topics
(
  bio TEXT,
  name TEXT,
  followers INT, --default 0
  PRIMARY KEY (name)
);

CREATE TABLE core.following
(
  username TEXT, 
  follows TEXT,
  PRIMARY KEY (username)
);

CREATE TABLE core.childcomments
(
  parentid UUID,
  childid UUID,
  PRIMARY KEY (parentid, childid)
);

CREATE TABLE childposts
(
  parentid TEXT,
  childid UUID,
  PRIMARY KEY (parentid, childid)
);
```
