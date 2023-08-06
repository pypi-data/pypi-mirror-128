import heroku.errors as errors
from typing import (
    Any
)
import requests


class Buildpack:
    def __init__(self, buildpack: str = None, ordinal: int = 0):
        self.buildpack = buildpack
        self.ordinal = ordinal

    def raw(self) -> dict:
        return {
            "buildpack": self.buildpack,
            "ordinal": self.ordinal
        }


class Buildpacks:
    def __init__(self, app, api=None):
        self.app = app
        if api is None:
            self._ = app._
            return
        self._ = api

    def list(self) -> dict:
        data = self._.call(
            endpoint=f"apps/{self.app['id']}/buildpack-installations",
            method="GET"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def new(
        self,
        buildpacks,
        update: bool = False
    ) -> dict:
        out: dict = {"updates": []}
        for b in buildpacks:
            b = b.raw()
            out["updates"].insert(b["ordinal"], {
                "buildpack": b["buildpack"]
            })

        data = self._.call(
            endpoint=f"apps/{self.app['id']}/buildpack-installations",
            method="PUT",
            data=out,
            json=True,
            headers={
                "Content-Type": "application/json"
            }
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]


class APP:
    def __init__(self, app: dict, api) -> None:
        self.app = app
        self._ = api
        self.buildpacks = Buildpacks(self)

    def delete(self) -> dict:
        return self._.app.delete(self.app["id"])

    def info(self) -> dict:
        return self._

    def update_info(self) -> None:
        self.app = self._.app.get_info(self.app["id"])

    def update(self, **data) -> None:
        self.app = self._.app.update(self.app["id"], **data)

    def __getitem__(self, item) -> Any:
        return self.app[item]

    def __getattr__(self, attr) -> Any:
        return self.app[attr]

    def __repr__(self) -> str:
        return "Heroku.APP: " + self.app.__repr__()


class APPApi:
    def __init__(self, api):
        self._ = api

    def get_info(self, _id: str):
        data = self._.call(
            endpoint=f"apps/{_id}",
            method="GET"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def get(self, _id: str) -> APP:
        app = APP(self.get_info(_id), self._)
        return app

    def update(self, _id: str, data: dict) -> APP:
        data = self._.call(
            endpoint=f"apps/{_id}",
            method="PATCH",
            data=data
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def new(self, name: str, region: str, stack: str) -> APP:
        data = self._.call(
            endpoint="apps",
            method="POST",
            data={
                "name": name,
                "region": region,
                "stack": stack
            }
        )
        if data[0] == 201:
            return APP(data[1], self._)
        raise errors.common["-1"]

    def delete(self, _id) -> dict:
        data = self._.call(
            endpoint=f"apps/{_id}",
            method="DELETE"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def list(self, user: str = None) -> dict:
        data = self._.call(
            endpoint=(
                "apps" if user is None
                else "users/{user}/apps"
            ),
            method="GET"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]


class Account:
    def __init__(self, api):
        self._ = api
        self.getRateLimit = self.get_rate_limit

    def me(self) -> dict:
        data = self._.call(
            endpoint="account",
            method="GET"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def update(self, data: dict) -> dict:
        data = self._.call(
            endpoint="account",
            method="PATCH",
            data=data,
            json=True,
            headers={
                "Content-Type": "application/json"
            }
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def delete(self, data: dict, confirm: bool = False) -> dict:
        """
            Delete's your account

            Warning: this action can't be undone
        """
        if confirm is False:
            while True:
                q = input(
                    "You are going to delete" +
                    " your account, please confirm: [Y/n]"
                )
                if q.lower() in ["y", "yes", "ok", "do", "go"]:
                    del q
                    break
                elif q.lower() in ["no", "not", "n"]:
                    del q
                    print("Cancelled!")
                    return {"cancelled": True}
                else:
                    print("Invalid response!")

        data = self._.call(
            endpoint="account",
            method="DELETE"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]

    def get_rate_limit(self):
        data = self._.call(
            endpoint="account/rate-limits",
            method="GET"
        )
        if data[0] == 200:
            return data[1]
        raise errors.common["-1"]


class HerokuApi:
    def __init__(
        self, api_key, email: str = None,
        alias: str = None
    ) -> None:
        self.key = api_key
        self.alias = alias
        self.email = email

        self.session = requests.Session()
        self.session.headers["Accept"] = \
            "application/vnd.heroku+json; version=3"

        self.app = APPApi(self)
        self.account = Account(self)

    def __repr__(self):
        return f"<HerokuAPI email='{self.email}' alias='{self.alias}'>"

    def call(
        self, endpoint: str, method: str, json: bool = False,
        data: dict[Any, Any] = None, *args, **kwargs
    ) -> Any:
        _call = self.session.request(
            method, f"https://api.heroku.com/{endpoint}",
            auth=("", self.key), *args, **kwargs,
            **({"json": data} if json else {"data": data}), 
        )
        call = _call.json()

        if _call.status_code == 429:
            raise errors.common["-2"]

        if "message" in call:
            if call["id"] == "rate_limit":
                raise errors.RateLimitExceded._exec()
            raise errors.Message(call["message"])

        if "error" in call:
            raise errors.InvalidRequest(
                call["id"] +
                ": " + call["error"] +
                "\r\n" + call["url"]
            )
        return (_call.status_code, call)
