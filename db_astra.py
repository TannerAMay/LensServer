from typing import Tuple

from time import time
import uuid
import hashlib

from db_connect import gen_session


READING_RATE = 250  # Words per minute
POSTS_PER_REQUEST = 10  # How many post UUIDs to return to client when asked for posts


def create_user(username: str, password: str, salt: bytes) -> Tuple[bool, bool]:
    """Add user to core.userdata and auth.user tables.

    username: Username of the user.
    password: User's hashed password.
    Return: First index is result of adding to core.userdata, second is result of adding to auth.user.
    """
    SESSION = gen_session()

    hash = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )

    addUserToUserdata = SESSION.execute(f"INSERT INTO core.userdata (username, bio, createdate) "
                                        f"VALUES ('{username}', '', '{int(time())}') "
                                        f"IF NOT EXISTS").one()
    addUserToAuth = SESSION.execute(f"INSERT INTO auth.users (username, password, salt) "
                                    f"VALUES ('{username}', {hash.hex()}, {salt.hex()}) "
                                    f"IF NOT EXISTS").one()

    return addUserToUserdata[0], addUserToAuth[0]


def login(username: str, password: str) -> bool:
    """Log user in.

    Check if username exists and if password matches the hash in auth.users.

    username: Username of the user.
    password: User's hashed password.
    Return: True if username-password combo exists in auth.users, else false.
    """
    SESSION = gen_session()
    cmd = SESSION.execute(f"SELECT * FROM auth.users WHERE username='{username}'").one()

    hash = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        cmd[2],  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )

    # If select returned results or more than two columns or passwords do not match, return false.
    if cmd is None or len(cmd) != 2 or cmd[1] != hash.hex():
        return False

    return True


def submit_post(title: str, contentType: str, content: str, author: str, parentID: str):
    if contentType == 'text':
        watchTime = len(content) // READING_RATE + 1
    else:
        watchTime = 0

    thisUUID = uuid.uuid4()

    SESSION = gen_session()
    # Add new post to posts table
    addToPosts = SESSION.execute(f"INSERT INTO core.posts "
                                 f"(postid, parentid, title, author, content, contenttype, views, upvotes, downvotes, watchtime, dateposted) "
                                 f"VALUES "
                                 f"({thisUUID}, '{parentID}', '{title}', '{author}', '{content}', '{contentType}', {1}, {1}, {0}, {watchTime}, {int(time())}) "
                                 f"IF NOT EXISTS").one()
    # Associate new post with topic or user
    addToChildPosts = SESSION.execute(f"INSERT INTO core.childposts "
                                      f"(parentid, childid) "
                                      f"VALUES ('{parentID}', {thisUUID}) "
                                      f"IF NOT EXISTS").one()
    # Add initial vote to uservotes table
    addToUservotes = SESSION.execute(f"INSERT INTO core.uservotes "
                                     f"(postid, username, upvoted, viewtime) "
                                     f"VALUES "
                                     f"({thisUUID}, '{author}', {True}, {watchTime}) "
                                     f"IF NOT EXISTS").one()

    return addToPosts[0], addToChildPosts[0], addToUservotes[0]


def submit_comment(author: str, content: str, parentID: uuid.UUID):
    watchTime = len(content) // READING_RATE + 1

    thisUUID = uuid.uuid4()
    SESSION = gen_session()
    # Add new comment to comment table
    addToComments = SESSION.execute(f"INSERT INTO core.comments "
                                    f"(postid, author, content, views, upvotes, downvotes, watchtime, dateposted) "
                                    f"VALUES "
                                    f"({thisUUID}, '{author}', '{content}', {1}, {1}, {0}, {watchTime}, {int(time())})"
                                    f"IF NOT EXISTS").one()
    # Associate new comment with a post
    addToChildComments = SESSION.execute(f"INSERT INTO core.childcomments "
                                         f"(parentid, childid) "
                                         f"VALUES "
                                         f"({parentID}, {thisUUID}) "
                                         f"IF NOT EXISTS").one()
    # Add initial vote score to comment
    addToUserVotes = SESSION.execute(f"INSERT INTO core.uservotes "
                                     f"(postid, username, upvoted, viewtime) "
                                     f"VALUES "
                                     f"({thisUUID}, '{author}', {True}, {watchTime})"
                                     f"IF NOT EXISTS").one()

    return addToComments[0], addToChildComments[0], addToUserVotes[0]


def retrieve_post_comment_data(postUUID: uuid.UUID, comment: bool):
    SESSION = gen_session()
    if comment:
        cmd = SESSION.execute(f"SELECT * FROM core.comments WHERE postid={postUUID}").one()
    else:
        cmd = SESSION.execute(f"SELECT * FROM core.posts WHERE postid={postUUID}").one()

    if cmd is not None:
        return cmd

    return tuple()


def cast_vote_record_viewtime(username: str, source: uuid.UUID, upvote: bool, viewtime: int, comment: bool):
    SESSION = gen_session()
    # Create row in uservotes table
    addToUservotes = SESSION.execute(f"INSERT INTO core.uservotes "
                                     f"(postid, username, upvoted, viewtime) "
                                     f"VALUES "
                                     f"({source}, '{username}', {upvote}, {viewtime}) "
                                     f"IF NOT EXISTS").one()

    # Update values in post or comments table
    table = "core.comments" if comment else "core.posts"
    voteType = "upvotes" if upvote else "downvotes"
    incrementValue = SESSION.execute(f"SELECT views, {voteType}, watchtime FROM {table} "
                                     f"WHERE postid={source}").one()
    updateTable = SESSION.execute(f"UPDATE {table} "
                                  f"SET views={incrementValue[0] + 1}, {voteType}={incrementValue[1] + 1},"
                                  f"watchtime={incrementValue[2] + int(viewtime)} "
                                  f"WHERE postid={source} "
                                  f"IF EXISTS").one()
    return addToUservotes[0], updateTable[0]


def retrieve_post_from_topic_or_user(source: str, username: str, numPosts: int):
    SESSION = gen_session()
    cmd = SESSION.execute(f"SELECT childid FROM core.childposts WHERE parentid='{source}'").all()

    # Get UUIDs of numPosts number of posts
    postUUIDs = []
    for row in cmd:
        if SESSION.execute(f"SELECT username FROM core.uservotes WHERE username='{username}' and postid={row[0]}").one() is not None:
            continue
        if len(postUUIDs) > numPosts - 1:
            break
        postUUIDs.append(row[0])

    return postUUIDs


def get_followed_topics(username: str):
    SESSION = gen_session()
    cmd = SESSION.execute(f"SELECT follows FROM core.following "
                          f"WHERE username='{username}'").all()
    topics = SESSION.execute(f"SELECT name FROM core.topics").all()

    followedTopics = []
    for f in cmd:
        if f in topics:
            followedTopics.append(f[0])

    return followedTopics


def follow(name: str, username: str):
    SESSION = gen_session()
    cmd = SESSION.execute(f"INSERT INTO core.following "
                          f"(username, follows) "
                          f"VALUES "
                          f"('{username}', '{name}') "
                          f"IF NOT EXISTS").one()
    return cmd[0]

