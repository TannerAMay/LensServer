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
    print("FEFE")
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
        return jsonify("{'100': 'Success! The user was added to core.userdata and auth.users.'")
    else:
        if not createResult[0] and not createResult[1]:
            return jsonify("{'101': 'Failure! The user not added to core.userdata nor auth.users.'")

        if createResult[0]:
            return jsonify("{'102': 'Failure! The user was not added to auth.users.'")

    return jsonify("{'103': 'Failure! The user was not added to core.userdata.'")


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
        #return redirect(url_for('app.profile'))

    return jsonify("{'201': 'Failure! The user was not found in auth.users and could not be logged in.'")
    

@app.route('/submit_post', methods=["POST"])
@login_required
def submit_post():
    """Submit a new post to a topic or user.

    JSON Expectation:
    {
        'title': '<title text>',
        'contenttype': '<text="text" or "link"',
        'content': '<text>',
        'author': '<username text>',
        'parentid': text -> Username or name of a topic
    }

    Codes: Code Signature: 3
        300: Post successfully submitted.
        301: Failure. The post was not added to to core.posts, core.childposts, nor core.uservotes.
        302: Failure. The post was not added to core.posts nor core.childposts.
        303: Failure. The post was not added to core.posts nor core.uservotes.
        304: Failure. The post was not added to core.childposts nor core.uservotes.
        305: Failure. The post was not added to core.posts.
        306: Failure. The post was not added to core.childposts.
        307: Failure. The post was not added to core.uservotes.

    return: JSON object describing result of command.
    """
    submitResult = db_astra.submit_post(
        title=request.form['title'],
        contentType=request.form['contenttype'],
        content=request.form['content'],
        author=request.form['author'],
        parentID=request.form['parentid']
    )

    if submitResult[0] and submitResult[1] and submitResult[2]:
        return jsonify("{'300': 'Success! The post was added to core.posts, core.childposts, and core.uservotes.")
    else:
        if not submitResult[0] and not submitResult[1] and not submitResult[2]:
            return jsonify("{'301': 'Failure! The post was not added to core.posts, core.childposts, nor core.uservotes.'")

        if not submitResult[0] and not submitResult[1]:
            return jsonify("{'302': 'Failure! The post was not added to core.posts nor core.childposts.'")

        if not submitResult[0] and not submitResult[2]:
            return jsonify("{'303': 'Failure! The post was not added to core.posts nor core.uservotes.'")

        if not submitResult[1] and not submitResult[2]:
            return jsonify("{'304': 'Failure! The post was not added to core.childposts nor core.uservotes.'")

        if not submitResult[0]:
            return jsonify("{'305': 'Failure! The post was not added to core.posts.'")

        if not submitResult[1]:
            return jsonify("{'306': 'Failure! The post was not added to core.childposts.'")

    return jsonify("{'307': 'Failure! The post was not added to core.uservotes.'")


@app.route('/submit_comment', methods=["POST"])
@login_required
def submit_comment():
    """Submit a new comment to a post.

    JSON Expectation:
    {
        'content': '<text>',
        'author': '<username text>',
        'parentid': UUID -> NO QUOTES!
    }

    Codes: Code Signature: 7
        700: Post successfully submitted.
        701: Failure. The post was not added to to core.comments, core.childcomments, nor core.uservotes.
        702: Failure. The post was not added to core.comments nor core.childcomments.
        703: Failure. The post was not added to core.comments nor core.uservotes.
        704: Failure. The post was not added to core.childcomments nor core.uservotes.
        705: Failure. The post was not added to core.comments.
        706: Failure. The post was not added to core.childcomments.
        707: Failure. The post was not added to core.uservotes.

    return: JSON object describing result of command.
    """
    submitResult = db_astra.submit_comment(
        content=request.form['content'],
        author=request.form['author'],
        parentID=request.form['parentid']
    )

    if submitResult[0] and submitResult[1] and submitResult[2]:
        return jsonify("{'700': 'Success! The post was added to core.comments, core.childcomments, and core.uservotes.")
    else:
        if not submitResult[0] and not submitResult[1] and not submitResult[2]:
            return jsonify("{'701': 'Failure! The post was not added to core.comments, core.childcomments, nor core.uservotes.'")

        if not submitResult[0] and not submitResult[1]:
            return jsonify("{'702': 'Failure! The post was not added to core.comments nor core.childcomments.'")

        if not submitResult[0] and not submitResult[2]:
            return jsonify("{'703': 'Failure! The post was not added to core.comments nor core.uservotes.'")

        if not submitResult[1] and not submitResult[2]:
            return jsonify("{'704': 'Failure! The post was not added to core.childcomments nor core.uservotes.'")

        if not submitResult[0]:
            return jsonify("{'705': 'Failure! The post was not added to core.comments.'")

        if not submitResult[1]:
            return jsonify("{'706': 'Failure! The post was not added to core.childcomments.'")

    return jsonify("{'707': 'Failure! The post was not added to core.uservotes.'")


@app.route('/rtup', methods=["GET"])
@login_required
def rtup():
    """Retrieve post UUID(s) from a topic or user.

    JSON Expectation:
    {
        'source': '<text>' -> Usernames or topics can go in this field
    }

    Codes: Code Signature: 6
        600: Post UUID(s) successfully retrieved from core.childposts.
        601: Failure. Post UUID(s) could not be retrieved from core.childposts.

    return: JSON Result:
    {
        '<error number string>': '<error description string>',
        'contents': '<Python list containing up to zero to ten, inclusive, UUIDs>'
    }
    """
    postUUIDs = db_astra.retrieve_post_from_topic_or_user(request.form["source"])

    if postUUIDs:
        # return jsonify("\{'600': 'Success! Post UUID(s) have been retrieved frm core.childposts.', 'contents': {}\}".format(postUUIDs))
        return jsonify('{' + f"'600': 'Success! Post UUID(s) have been retrieved from core.childposts.', 'contents': {postUUIDs}" + "}")

    return jsonify('{' + f"'601': 'Failure! Post UUID(s) could not be retrieved from core.childposts.', 'contents': {[]}" + "}")


@app.route('/rpcd', methods=["GET"])
@login_required
def rpcd():
    """Retrieve post or comment data.

    JSON Expectation:
    {
        'source': UUID of post/comment -> NO QUOTES!.
        'iscomment': bool -> True if requesting a comment.
    }

    Codes: Code Signature: 4
        400: Post/comment data successfully retrieved.
        401: Post/comment data could not be retrieved from core.posts or core.comments, respectively.

    return: JSON Result:
    {
        '<error number string>': '<error description string>',
        'contents': '<Python list containing all data associated with post/comment>'
    }
    """
    data = db_astra.retrieve_post_comment_data(request.form['source'], request.form['iscomment'][0] == 'T')

    if data:
        return jsonify('{' + f"'400': 'Success! Post/comment data successfully retrieved from core.posts or core.comments, respectively.',"
                             f"'contents': {data}" + "}")

    return jsonify('{' + f"'401': 'Failure! Post/comment data could not be retrieved from core.posts or core.comments, respectively.',"
                         f"'contents': {[]}" + "}")


@app.route('/cast_vote', methods=["POST"])
@login_required
def cast_vote():
    """Send an upvote or downvote to post and record how long the user viewed it.

    JSON Expectation:
    {
        'username': '<username text>',
        'source': UUID,
        'upvote': bool,
        'viewtime': int,
        'iscomment': bool
    }

    Codes: Code Signature: 5
        500: Post successfully submitted.
        ... add more errors as function is made

    return: JSON object describing result of command.
    """
    cmdResult = db_astra.cast_vote_record_viewtime(username=request.form['username'], source=request.form['source'],
                                                   upvote=request.form['upvote'][0] == 'T',
                                                   comment=request.form['iscomment'][0] == 'T',
                                                   viewtime=request.form['viewtime'])
    if cmdResult[0] and cmdResult[1]:
        return jsonify("{'500': 'Success! The user's vot has been cast and view time counted.'}")
    else:
        if not cmdResult[0] and not cmdResult[1]:
            return jsonify("{'501': 'Failure. The vote could not be added to core.uservotes and the post's data could"
                           "not be updated.'}")

        if not cmdResult[0]:
            return jsonify("{'502': 'Failure. The vote could not be added to core.uservotes.'}")

    return jsonify("{'503': 'Failure. The post's data could not be updated.'}")


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

# Casting a vote and recording viewtime
"""Send an upvote or downvote to post and record how long the user viewed it.

JSON Expectation:
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
