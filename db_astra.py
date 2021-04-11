from typing import Tuple

from time import time
from typing import Tuple

from db_connect import SESSION


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

