import datetime
import sqlite3
from sqlite3.dbapi2 import Cursor


class Repository:
  def __init__(self, db_name: str) -> None:
    self._db_name = db_name

  def connect(self):
    connection = sqlite3.connect(
        self._db_name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    connection.row_factory = dict_factory
    return connection

  def initialize_tables(self):
    connection = self.connect()
    cursor = connection.cursor()

    if not cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=:name''', {
            'name': 'twitter_users'}).fetchone():
      cursor.execute('''CREATE TABLE twitter_users
               (id text, name text, username text, profile_image_url text, date timestamp)''')

    if not cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=:name''', {
            'name': 'twitter_user_follows'}).fetchone():
      cursor.execute('''CREATE TABLE twitter_user_follows
               (followed_id text, follower_id text, date timestamp)''')

    connection.commit()
    connection.close()

  def insert_user(self, user: dict):
    connection = self.connect()
    cursor = connection.cursor()

    result = cursor.execute("insert into twitter_users values (:id, :name, :username, :profile_image_url, :date)", {"id": user['id'], "name": user['name'], "username": user['username'], "profile_image_url": user['profile_image_url'], "date": datetime.datetime.now()})

    connection.commit()
    connection.close()

  def insert_follow(self, follower_id: str, followed_id: str):
    connection = self.connect()
    cursor = connection.cursor()

    existing_row = cursor.execute(
        "select * from twitter_user_follows where followed_id=:followed_id and follower_id=follower_id)",
        {
            "followed_id": followed_id,
            "follower_id": follower_id
        }).fetchone()

    if existing_row is None:
      result = cursor.execute(
          "insert into twitter_user_follows (followed_id, follower_id, date)",
          {
              "followed_id": followed_id,
              "follower_id": follower_id,
              "date": datetime.datetime.now()
          })
    else:
      result = cursor.execute(
          "update twitter_user_follows set date=:date where followed_id=:followed_id and follower_id=:follower_id",
          {
              "followed_id": followed_id,
              "follower_id": follower_id,
              "date": datetime.datetime.now()
          })

    connection.commit()
    connection.close()

  def find_user_by_username(self, username: str):
    connection = self.connect()
    cursor = connection.cursor()

    result = cursor.execute(
        "select * from twitter_users where username=:username", {"username": username})

    return result.fetchone()

  def find_user_followers(self, user_id: str):
    connection = self.connect()
    cursor = connection.cursor()

    result = cursor.execute(
        "select * from twitter_user_follows where followed_id=:user_id", {"user_id": user_id})

    return result.fetchall()


def dict_factory(cursor: Cursor, row):
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d
