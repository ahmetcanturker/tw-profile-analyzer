from datetime import datetime
from persistence import Repository
from client import TwitterClient


class CachedTwitterClient:
  def __init__(self,
               repository: Repository,
               client: TwitterClient,
               user_max_age: int,
               follow_max_age: int) -> None:
    self._repository = repository
    self._client = client
    self._user_max_age = user_max_age
    self._follow_max_age = follow_max_age

  def initialize(self):
    self._repository.initialize_tables()

  def get_user_by_username(self, username: str):
    db_user = self._repository.find_user_by_username(username)
    if db_user is not None and (datetime.now() - db_user['date']).seconds <= self._user_max_age:
      print('Found cached entry', db_user['id'])
      return db_user

    api_user = self._client.get_user_by_username(username)
    if api_user is not None:
      self._repository.insert_user(api_user)

    return api_user

  def get_followers(self, user_id: str):
    db_followers = self._repository.find_user_followers(user_id)
    for follower in db_followers:
      if (datetime.now() - follower['date']).seconds <= self._follow_max_age:
        # TODO: Delete actual data?
        db_followers.remove(follower)

    # TODO: Follow cursor...
    api_followers = self._client.get_followers(user_id)
    if api_followers is not None:
      for api_follower in api_followers:
        self._repository.insert_follow(user_id, api_follower['id'])

    return api_followers