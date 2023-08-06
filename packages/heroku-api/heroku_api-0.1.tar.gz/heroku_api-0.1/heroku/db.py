from typing import (
    Optional,
    Callable,
    Union,
    Any
)
import sqlite3
import os


def remove_basename(name):
    if name[len(name) - 1] in ["/", "\\"] or \
            "\\" not in name and "/" not in name:
        return name

    return name.rstrip(os.path.basename(name))


class DB:
    def __init__(self, location: str = remove_basename(__file__)) -> None:
        self.db = sqlite3.connect(os.path.join(location, "heroku.db"))
        self.cursor: Union[sqlite3.Cursor, None] = None

    def exec(self, func: Callable, **kwargs) -> Any:
        if self.cursor is None:
            self.cursor = self.db.cursor()
        return func(self, **kwargs)

    def __getattr__(self, attr):
        try:
            return getattr(self.cursor, attr)
        except AttributeError:
            return getattr(self.db, attr)


class HerokuDB:
    def __init__(self, db):
        self.db = db

    def __getattr__(self, attr):
        def run(**data):
            return self.db.exec(getattr(self, "_" + attr), **data)
        return run

    def _setup_db(self, db: DB) -> None:
        query = "create table if not exists " + \
            "heroku_users(email string, token string, alias string)"
        db.execute(query)
        db.commit()

    def _get_user(
        self, db: DB,
        email: str = None,
        alias: str = None
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        if alias is None and email is None:
            raise Exception(
                "'ALIAS' and 'EMAIL' arg's " +
                "can't be None at the same time")

        if email is not None:
            query = "select token, alias from heroku_users where " + \
                f"email='{email}'"

        else:
            query = "select token, alias from heroku_users where " + \
                f"alias='{alias}' "

        db.execute(query)
        data = db.fetchall()

        if len(data) == 0:
            return (None, None, None)

        return (email, data[0][0], data[0][1])

    def _update_user(self, *args, **kwargs) -> Any:
        return self._new_user(*args, **kwargs)

    def _new_user(
        self, db, email,
        token, alias: str = None
    ) -> Any:
        user = self._get_user(db, email)
        if alias is None:
            if user[2] is not None:
                alias = user[2]

            else:
                alias = email

        if user[2] is None and email is None:
            raise Exception("'EMAIL' is None and user not exist's")

        if user[2] is None:
            query = "insert into heroku_users values( " + \
                        f"'{email}', '{token}', '{alias}'" + \
                    ")"
            db.execute(query)
            db.commit()

        else:
            query = "update heroku_users set " + \
                f"token='{token}', alias='{alias}' where email='{email}'"
            db.execute(query)
            db.commit()

        return email, token, alias
