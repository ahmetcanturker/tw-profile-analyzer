import os
from dotenv import load_dotenv


def get_app_configuration():
  load_dotenv()

  TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
  TWITTER_API_KEY_SECRET = os.getenv('TWITTER_API_KEY_SECRET')
  TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

  return {
      'TWITTER_API_KEY': TWITTER_API_KEY,
      'TWITTER_API_KEY_SECRET': TWITTER_API_KEY_SECRET,
      'TWITTER_BEARER_TOKEN': TWITTER_BEARER_TOKEN
  }
