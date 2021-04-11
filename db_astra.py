from time import time
from typing import Tuple

from db_connect import gen_session



def create_user(username: str, password: str) -> Tuple[bool, bool]:
    """Add user to core.userdata and auth.user tables.

    username: Username of the user.
    password: User's hashed password.
    Return: First index is result of adding to core.userdata, second is result of adding to auth.user.
    """

    SESSION = gen_session()

    addUserToUser = SESSION.execute(f"insert into core.userdata (username, bio, createdate) "
                                    f"values ('{username}', '', '{int(time())}') "
                                    f"if not exists").one()
 
    addUserToAuth = SESSION.execute(f"insert into auth.users (username, password) "
                                    f"values ('{username}', '{password}') "
                                    f"if not exists").one()

    return addUserToUser[0], addUserToAuth[0]


def login(username: str, password: str) -> bool:
    """Log user in.

    Check if username exists and if password matches the hash in auth.users.

    username: Username of the user.
    password: User's hashed password.
    Return: True if username-password combo exists in auth.users, else false.
    """
    SESSION = gen_session()

    cmd = SESSION.execute(f"select * from auth.users where username='{username}'").one()

    # If select returned results or more than two columns or passwords do not match, return false.
    if cmd is None or len(cmd) != 2 or cmd[1] != password:
        return False

    return True

