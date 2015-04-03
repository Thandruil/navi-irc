import time

import ZODB
import ZODB.FileStorage
import BTrees
from persistent import Persistent


class UserInfo(Persistent):
    def __init__(self, username, info=None):
        self.username = username
        self.info_hist = BTrees.OOBTree.OOBTree()
        self.info_hist[time.time()] = info

    @property
    def info(self):
        return self.info_hist[self.info_hist.maxKey()]

    @info.setter
    def info(self, value):
        self.info_hist[time.time()] = value
        return value


def init_db(filename='lgbteens.fs'):
    """Initializes a ZODB database."""
    storage = ZODB.FileStorage.FileStorage(filename)
    db = ZODB.DB(storage)
    return db


def open_conn(db):
    connection = db.open()
    root = connection.root()
    if 'users' not in root:
        root.users = BTrees.OOBTree.OOBTree()
    return connection, root
