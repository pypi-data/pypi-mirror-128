from heroku.account_manager import AccountManager
from heroku.db import DB, HerokuDB
from functools import partial
__version__ = '0.1'


Manager = partial(
    AccountManager, db=HerokuDB(DB()))
