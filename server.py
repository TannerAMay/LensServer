from flask import Blueprint, Flask, request, Response, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user, LoginManager

import db_astra

from models import User
from keys import FLASK_SECRET_KEY

# from app import app

# db = SQLAlchemy()

# main = Blueprint('main', __name__)

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

# db.init_app(app)

# from .main import main as main_blueprint
# app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(username):
    """Load user from Astra by username, load into User object
    
    current_user calls this function
    """
    user = User()
    user.username = username
    user.password = "test"
    ## add all data from astra for this user
    
    return user


@app.route("/")
def home():
    return "Eat me"


@app.route("/create_user", methods=["POST"])
def create_user():
    """Add user data to database.

    JSON Expectation:
    {
        'user': '<username text>',
        'pass': '<hashed password text>',
        'bio': '<bio text>'
    }

    Codes: Code Signature: 1
        100: User successfully added to both core.userdata and auth.users.
        101: Failed to add to auth.user table.
        102: Failed to add to core.userdata table.

    return: JSON object describing result of command.
    """
    createResult = db_astra.create_user(request.form['user'], request.form['pass'])

    if createResult[0] and createResult[1]:
        return jsonify("{'100': 'Success! The user was added to core.user and auth.user.'")

    if createResult[0]:
        return jsonify("{'101': 'Failure! The user was not added to auth.user.'")

    return jsonify("{'102': 'Failure! The user was not added to core.user.'")


@app.route("/login", methods=["POST"])
def login():
    """Log in a user.

    JSON Expectation:
    {
        'user': '<username text>',
        'pass': '<hashed password text>'
    }

    Codes: Code Signature: 2
        200: User was found in auth.users and successfully logged in.
        201: Failed to find user in user.auth.

    return: JSON object describing result of command.
    """

    remember = True if request.form.get('remember') else False

    # Checks for valid login
    if db_astra.login(request.form['user'], request.form['pass']):
        user_to_test = User()
        user_to_test.username = request.form['user']
        user_to_test.password = request.form['pass']  # Might not need
        login_user(user_to_test, remember=remember)

        return jsonify("{'200': 'Success! The user is logged in.'")
        #return redirect(url_for('main.profile'))

    return jsonify("{'201': 'Failure! The user was not found in auth.users and could not be logged in.'")
    

@app.route('/profile')
@login_required
def profile():
    return current_user.username

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return "logged out"


"""
DOCSTRINGS FOR FUTURE FUNCTIONS
"""

# Submitting post
"""Submit a new post to a topic or user.

JSON Expectations:
{
    'title': '<title text>',
    'contenttype': '<text="text" or "link"',
    'author': '<username text>',
    'timeposted': timestamp -> int(time.time())
    'parentid': UUID -> Empty if submitting to a user
}

Codes: Code Signature: 3
    300: Post successfully submitted.
    ... add more errors as function is made

return: JSON object describing result of command.
"""

# Viewing a post
"""Retrieve a post from the database.

JSON Expectations:
{
    'postid': UUID
}

Codes: Code Signature: 4
    400: Post successfully retrieved.
    ... add more errors as function is made

return: JSON object describing result of command.
"""

# Casting a vote and recording viewtime
"""Send an upvote or downvote to post and record how long the user viewed it.

JSON Expectations:
{
    'username': '<username text>',
    'postID': UUID,
    'upvote': bool,
    'viewtime': int
}

Codes: Code Signature: 5
    500: Post successfully submitted.
    ... add more errors as function is made

return: JSON object describing result of command.
"""

# Get posts from user or in topic
"""Retrieve posts from a topic or user.

JSON Expectations:
{
    'username': '<username text>' -> Put topic names in this field too but make sure to mark topicbool as true,
    'istopic': bool
}

Codes: Code Signature: 6
    600: Post successfully submitted.
    ... add more errors as function is made

return: JSON object describing result of command.
"""
if __name__ == "__main__":
    app.run()
