from datetime import datetime
from cachedclient import CachedTwitterClient
from client import TwitterClient
from environment import get_app_configuration
from persistence import Repository

SETTINGS = {
    'TWITTER_API_BASE_URL': 'https://api.twitter.com',
    'USE_BEARER_TOKEN': False
}


'''
Steps
1- Fetch as many of the targeted users as possible
1.a- Filter down users based on (?) to determine whether they fit to the given category of {TR software developers}
2- Download and run color analysis on profile images
3- 
'''


def initialize_twitter_client(app_configuration: dict):
  if SETTINGS['USE_BEARER_TOKEN']:
    twitter_client = TwitterClient(
        SETTINGS['TWITTER_API_BASE_URL'],
        app_configuration['TWITTER_API_KEY'],
        app_configuration['TWITTER_API_KEY_SECRET'],
        app_configuration['TWITTER_BEARER_TOKEN'])
  else:
    twitter_client = TwitterClient(
        SETTINGS['TWITTER_API_BASE_URL'],
        app_configuration['TWITTER_API_KEY'],
        app_configuration['TWITTER_API_KEY_SECRET'],
        None)
  
  return twitter_client


def main():
  app_configuration = get_app_configuration()

  print('Found Twitter Api Key', app_configuration['TWITTER_API_KEY'])

  print('Found Twitter Api Key Secret',
        app_configuration['TWITTER_API_KEY_SECRET'])

  print('Found Twitter Bearer Token',
        app_configuration['TWITTER_BEARER_TOKEN'])


  twitter_client = initialize_twitter_client(app_configuration)

  # twitter_client.get_access_token()

  # twitter_client.get_user_by_username('ahmetcanturker')

  repository = Repository('test.db')
  # twitter_client.get_followers('')

  cached_twitter_client = CachedTwitterClient(
      repository, twitter_client, 100000, 10000)

  cached_twitter_client.initialize()

  print('@ahmetcanturker', cached_twitter_client.get_user_by_username('ahmetcanturker'))


if __name__ == "__main__":
  main()
