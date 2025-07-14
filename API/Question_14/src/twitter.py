#=========== Handles Authentication and return tweepy.clinet ============================

import os
from dotenv import load_dotenv
import tweepy

load_dotenv()
Bearer_Token=os.getenv("BEARER_TOKEN")

def get_client():
    return tweepy.Client(bearer_token=Bearer_Token,wait_on_rate_limit=True)