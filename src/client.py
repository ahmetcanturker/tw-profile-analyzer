from datetime import datetime
import requests
import urllib.parse
import base64


class RateLimit:
  def __init__(self, key, window, limit) -> None:
    self._key = key
    self._limit = limit
    self._request_count = 0
    self._window = window
    self._window_start = datetime.now()

  def increase(self, by: int = 1):
    pass

  # def has_exceeded(self):
  #   return self.will_exceed(0)

  # def will_exceed(self, by: int = 1):
  #   if self._request_count + by < self._limit:
  #     return False

  #   if self._window_start + self._window


class RateLimitTracker:
  def __init__(self) -> None:
    self.data = dict()

  # def increase(self, key: str, value: int = 1):
  #   if key in self.data:
  #     self.data =


class TwitterClient:
  def __init__(self, base_url: str, api_key: str, api_key_secret: str, bearer_token: str) -> None:
    self._base_url = base_url
    self._api_key = api_key
    self._api_key_secret = api_key_secret
    self._bearer_token = bearer_token
    self._rate_limit_tracker = dict()

  def _request_headers(self, auto_retrieve: bool):
    if not self._bearer_token and auto_retrieve:
      if not self.retrieve_access_token():
        raise Exception('Unable to retrieve access token')

    return {"Authorization": "Bearer " + self._bearer_token}

  def _increase_request_rate(self, key: str, value: int = 1):
    if key in self._rate_limit_tracker:
      pass

  def retrieve_access_token(self):
    if not self._api_key or not self._api_key_secret:
      raise Exception(
          'Can not retrieve access token without api key and secret.')

    api_key = urllib.parse.quote_plus(self._api_key)
    api_key_secret = urllib.parse.quote_plus(self._api_key_secret)
    credentials = api_key + ':' + api_key_secret
    # print('Crendetials', credentials)
    encoded_credentials = base64.b64encode(
        credentials.encode('ascii')).decode('ascii')
    print('Encoded credentials', encoded_credentials)
    response = requests.post(f'{self._base_url}/oauth2/token',
                             data={'grant_type': 'client_credentials'},
                             headers={
                                 'Authorization': 'Basic ' + encoded_credentials,
                                 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                             })

    if (response.ok):
      # self.
      result = response.json()
      if result['token_type'] == 'bearer':
        self._bearer_token = result['access_token']
        return True

    return False

  def get_user_by_username(self, username: str):
    response = self.get(
        f'/2/users/by/username/{username}?user.fields=profile_image_url')
    # print('Response', response.json())
    if response.ok:
      data = response.json()
      return data['data']

    # TODO: Log error.
    return None

  def get_followers(self, user_id: str):
    response = self.get(f'/2/users/{id}/following')
    if response.ok:
      # print('Response', response.json())
      data = response.json()
      return data['data']

    # TODO: Log error.
    return None

  def get(self, resource: str):
    resource = resource if resource.startswith('/') else f'/{resource}'
    return requests.get(
        f'{self._base_url}{resource}',
        headers=self._request_headers(True))
