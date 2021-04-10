from time import time

from db_connect import SESSION


def create_user(username: str, password: str):
    addUser = SESSION.execute(f"insert into core.user (username, bio, create_date) "
                              f"values ('{username}', '', '{str(int(time()))}') "
                              f"if not exists").one()

    return addUser[0]


def login(username: str, hpassword: str):
    cmd = SESSION.execute(f"select * from auth.users where username='{username}'").one()

    if cmd is None or len(cmd) != 2 or cmd[1] != hpassword:
        return False

    return True

