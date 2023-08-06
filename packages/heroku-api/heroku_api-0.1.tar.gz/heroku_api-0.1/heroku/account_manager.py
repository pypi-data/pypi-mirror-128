from heroku.calls import HerokuApi
from heroku.db import HerokuDB
from typing import Any


class AccountManager:
    def __init__(self, db: HerokuDB):
        self.db = db
        if db is None:
            self.db = HerokuDB()
        self.db.setup_db()

    def new_user(
        self, email: str = None,
        alias: str = None, token: str = None
    ) -> Any:
        return self.db.new_user(
            email=email, alias=alias, token=token)

    def get_accounts(self):
        def get(self):
            query = "select email, token, alias from heroku_users"
            self.execute(query)
            out = []
            data = self.fetchall()
            for c in data:
                out.append(HerokuApi(email=c[0], api_key=c[1], alias=c[2]))

            return out

        return self.db.db.exec(get)
