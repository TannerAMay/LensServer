from time import time
from typing import Tuple

from db_connect import SESSION


def create_user(username: str, password: str) -> Tuple[bool, bool]:
    """Add user to core.user and auth.user tables.

    Returns: First index is result of adding to core.user, second is result of adding to auth.user.
    """
    addUserToUser = SESSION.execute(f"insert into core.user (username, bio, create_date) "
                                    f"values ('{username}', '', '{int(time())}') "
                                    f"if not exists").one()
    addUserToAuth = SESSION.execute(f"insert into auth.users (username, password) "
                                    f"values ('{username}', '{password}') "
                                    f"if not exists").one()

    return addUserToUser[0], addUserToAuth[0]


def login(username: str, hpassword: str) -> bool:
    """Log user in.

    Check if username exists and if password matches the hash in auth.users."
    """
    cmd = SESSION.execute(f"select * from auth.users where username='{username}'").one()

    # If select returned results or more than two columns or passwords do not match, return false.
    if cmd is None or len(cmd) != 2 or cmd[1] != hpassword:
        return False

    return True

