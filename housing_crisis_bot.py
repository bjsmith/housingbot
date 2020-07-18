#retweets tweets about the housing crisis

# Import Tweepy, sleep, credentials.py
import tweepy
from time import sleep
from datetime import datetime, timezone, timedelta

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from credentials import *
from os import environ
# consumer_key = environ['consumer_key']
# consumer_secret = environ['consumer_secret']
# access_token = environ['access_token']
# access_token_secret = environ['access_token_secret']


# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def output_tweet(t):
    print('Tweet by: @' + t.user.screen_name + "; " + str(t.favorite_count) + ". " + t.text)
    print(t.in_reply_to_screen_name)


#set times to search with
search_start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
search_end = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")

#set times to limit retweeting (because we're running this every hour, we don't want to repeat.)
narrow_start = (datetime.now(timezone.utc) - timedelta(hours=2))
narrow_end = (datetime.now(timezone.utc) - timedelta(hours=1))
#give them a little bit of time to pick up

#get the tweets
tweets = [t for t in 
          tweepy.Cursor(api.search,
                           q='"housing crisis" OR "affordable housing" OR "homeless" OR "house price" OR "RMA"',
                           since=search_start,
                           until=search_end,
                          geocode='-41.1,173.3,1500km' # in New Zealand
                        ).items(50)
         ]# get the 20 MOST RECENT tweets that match the qualification

#tweet any tweets that match criteria
for t in tweets:
    t_time = t.created_at.replace(tzinfo=timezone.utc)
    if((t_time>narrow_start) & (t_time<narrow_end)):#if it's in the right set
        #if it's not a retweet
        output_tweet(t)
        if hasattr(t,'retweeted_status')==False:
            #it's had at least one RT or favorite.
            #if (t.favorite_count>0) or (t.retweet_count>0):
            #go ahead and retweet it
            #output_tweet(t)
            t.retweet()
            #now follow that user if we aren't already
            if api.show_friendship(source_screen_name="aotearoayimby", target_id=t.author.id_str)[1].followed_by is False:
                #follow the user
                api.create_friendship(id=t.author.id_str)
            #have a sleep before you tweet another thing.
            time.sleep(600)                
