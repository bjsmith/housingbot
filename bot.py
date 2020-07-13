# Import Tweepy, sleep, credentials.py
import tweepy
from time import sleep

from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

from datetime import datetime, timezone, timedelta
start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
end = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
#this is EXCLUSIVE of 'end', 
#so we have to put in the end to be TOMORROW 
#if we want it to get tweets from today

tweets = [t for t in 
          tweepy.Cursor(api.search,
                           q='housing',
                           since=start,
                           until=end,
                          geocode='-41.1,173.3,1500km').items(20)
         ]# get the 20 MOST RECENT tweets that match the qualification


tweet_to_rt_index =  fav_counts.index(max(fav_counts)) # get the index of an arbitrary tweet with the most favorites
tweet_to_rt = tweets[tweet_to_rt_index]

rt_result = tweet_to_rt.retweet()