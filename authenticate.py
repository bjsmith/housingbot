from os import environ

import socket
import sys, os
import tweepy

if socket.gethostname().startswith("Benjamins"):
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from credentials import get_credentials

def get_authenticated_api():

    if socket.gethostname().startswith("Benjamins"):
        print("should have already got credentials")
        credentials = get_credentials()
        consumer_key = credentials['consumer_key']
        consumer_secret = credentials['consumer_secret']
        access_token = credentials['access_token']
        access_token_secret = credentials['access_token_secret']
    else:
        consumer_key = environ['consumer_key']
        consumer_secret = environ['consumer_secret']
        access_token = environ['access_token']
        access_token_secret = environ['access_token_secret']

    # Access and authorize our Twitter credentials from credentials.py
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return(api)
