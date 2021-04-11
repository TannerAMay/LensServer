from typing import Tuple

from time import time
import uuid

from db_connect import SESSION


READING_RATE = 250  # Words per minute
POSTS_PER_REQUEST = 10  # How many post UUIDs to return to client when asked for posts


def create_user(username: str, password: str) -> Tuple[bool, bool]:
    """Add user to core.userdata and auth.user tables.

    username: Username of the user.
    password: User's hashed password.
    Return: First index is result of adding to core.userdata, second is result of adding to auth.user.
    """
    addUserToUserdata = SESSION.execute(f"INSERT INTO core.userdata (username, bio, createdate) "
                                        f"VALUES ('{username}', '', '{int(time())}') "
                                        f"IF NOT EXISTS").one()
    addUserToAuth = SESSION.execute(f"INSERT INTO auth.users (username, password) "
                                    f"VALUES ('{username}', '{password}') "
                                    f"IF NOT EXISTS").one()

    return addUserToUserdata[0], addUserToAuth[0]


def login(username: str, password: str) -> bool:
    """Log user in.

    Check if username exists and if password matches the hash in auth.users.

    username: Username of the user.
    password: User's hashed password.
    Return: True if username-password combo exists in auth.users, else false.
    """
    cmd = SESSION.execute(f"SELECT * FROM auth.users WHERE username='{username}'").one()

    # If select returned results or more than two columns or passwords do not match, return false.
    if cmd is None or len(cmd) != 2 or cmd[1] != password:
        return False

    return True


def submit_post(title: str, contentType: str, content: str, author: str, parentID: str):
    if contentType == 'text':
        watchTime = len(content) // READING_RATE + 1
    else:
        watchTime = 0

    thisUUID = uuid.uuid4()

    addToPosts = SESSION.execute(f"INSERT INTO core.posts "
                                 f"(postid, parentid, title, author, content, contenttype, views, upvotes, downvotes, watchtime, dateposted) "
                                 f"VALUES "
                                 f"({thisUUID}, '{parentID}', '{title}', '{author}', '{content}', '{contentType}', {1}, {1}, {0}, {watchTime}, {int(time())}) "
                                 f"IF NOT EXISTS").one()
    addToChildPosts = SESSION.execute(f"INSERT INTO core.childposts "
                                      f"(parentid, childid) "
                                      f"VALUES ('{parentID}', {thisUUID}) "
                                      f"IF NOT EXISTS").one()
    addToUservotes = SESSION.execute(f"INSERT INTO core.uservotes "
                                     f"(postid, username, upvoted, viewtime) "
                                     f"VALUES "
                                     f"({thisUUID}, '{author}', {True}, {watchTime}) "
                                     f"IF NOT EXISTS").one()

    return addToPosts[0], addToChildPosts[0], addToUservotes[0]


def submit_comment(author: str, content: str, parentID: uuid.UUID):
    watchTime = len(content) // READING_RATE + 1

    thisUUID = uuid.uuid4()

    addToComments = SESSION.execute(f"INSERT INTO core.comments "
                                    f"(postid, author, content, views, upvotes, downvotes, watchtime, dateposted) "
                                    f"VALUES "
                                    f"({thisUUID}, '{author}', '{content}', {1}, {1}, {0}, {watchTime}, {int(time())})"
                                    f"IF NOT EXISTS").one()
    addToChildComments = SESSION.execute(f"INSERT INTO core.childcomments "
                                         f"(parentid, childid) "
                                         f"VALUES "
                                         f"({parentID}, {thisUUID}) "
                                         f"IF NOT EXISTS").one()
    addToUserVotes = SESSION.execute(f"INSERT INTO core.uservotes "
                                     f"(postid, username, upvoted, viewtime) "
                                     f"VALUES "
                                     f"({thisUUID}, '{author}', {True}, {watchTime})"
                                     f"IF NOT EXISTS").one()

    return addToComments[0], addToChildComments[0], addToUserVotes[0]


def retrieve_post_data(postUUID: uuid.UUID):
    pass


def retrieve_comments(postUUID: uuid.UUID):
    pass


def post_cast_vote_record_viewtime(username: str, postUUID: uuid.UUID, upvote: bool, viewtime: int):
    pass


def retrieve_post_from_topic_or_user(source: str):
    cmd = SESSION.execute(f"SELECT childid FROM core.childposts WHERE parentid='{source}'").all()

    postUUIDs = []
    for i, row in enumerate(cmd):
        if i > POSTS_PER_REQUEST - 1:
            break
        postUUIDs.append(row[0])

    return postUUIDs

