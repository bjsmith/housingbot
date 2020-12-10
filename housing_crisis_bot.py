#retweets tweets about the housing crisis

# Import Tweepy, sleep, credentials.py
import tweepy
import time
import pytz
from datetime import datetime, timezone, timedelta
import random
import sys, os

from authenticate import *

from daily_countdown import variable_ratio_daily_countdown_tweet

api = get_authenticated_api()

# get new zealand timezone
nztz = pytz.timezone("Pacific/Auckland")
# get now and today
now = datetime.now(nztz)
today = datetime.date(now)


def output_tweet(t):
    print('Tweet by: @' + t.user.screen_name + "; " + str(t.favorite_count) + ". " + t.text)
    print(t.in_reply_to_screen_name)

def try_retweet(t):
    try:
        t.retweet()
    except tweepy.TweepError as te:
        if te.args[0][0]['code']==327:
            print("tweet already tweeted, moving on")
        else:
            raise te

#set times to search with
search_start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
search_end = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")

#set times to limit retweeting (because we're running this every hour, we don't want to repeat.)
narrow_start = (datetime.now(timezone.utc) - timedelta(hours=2))
narrow_end = (datetime.now(timezone.utc) - timedelta(hours=1))
#give them a little bit of time to pick up



#modern housing tweets
modern_housing_tweets = [t for t in
          tweepy.Cursor(api.search,
                           q='from:@modernmultifam',
                        #'homeless' was returning way too many out-of-context tweets.
                        # had to make that one more specific
                           since=search_start,
                           until=search_end
                        ).items(50)
         ]# get the 20 MOST RECENT tweets that match the qualification
for t in modern_housing_tweets:
    try_retweet(t)
    time.sleep(60)


#housing crisis tweets
#get the tweets
tweets = [t for t in
          tweepy.Cursor(api.search,
                           q='"housing crisis" OR "affordable housing" OR "homelessness" OR "house price" OR "RMA" OR "NPS"',
                        #'homeless' was returning way too many out-of-context tweets.
                        # had to make that one more specific
                           since=search_start,
                           until=search_end,
                          geocode='-41.1,173.3,1500km' # in New Zealand
                        ).items(50)
         ]# get the 20 MOST RECENT tweets that match the qualification

variable_ratio_daily_countdown_tweet(api,60*5)

excepted_user_list = [
	'jimmywafer','economissive',
	'AlecMuses','PeterHarkessNZ',
	'TheBFD_nz','stanleystone76',
	'ElliotIkilei','pinko_hunter',
	'pitakakariki','Tat_Loo'

	]
excepted_user_list = [s.lower() for s in excepted_user_list]
#tweet any tweets that match criteria
for t in tweets:
    t_time = t.created_at.replace(tzinfo=timezone.utc)
    if((t_time>narrow_start) & (t_time<narrow_end)):#if it's in the right set
        #if it's not a retweet
        if t.user.screen_name.lower() in excepted_user_list:
            continue #we are ignoring this list of users, just go on to the next one.

        output_tweet(t)
        if hasattr(t,'retweeted_status')==False:
            #it's had at least one RT or favorite.
            #if (t.favorite_count>0) or (t.retweet_count>0):
            #go ahead and retweet it
            #output_tweet(t)

            try:
                tweet_full_url = "https://twitter.com/" + t.user.screen_name+ "/status/"  + t.id_str
            except:# (KeyError, AttributeError):
                tweet_full_url=None
                print("trouble getting the tweet URL")

            # if (datetime.date(datetime.strptime("2020-09-15","%Y-%m-%d")) ==today) and (tweet_full_url is not None):
            #     tweet_version = random.sample([0, 1, 2, 3], 1)[0]
            #     if tweet_version==0:
            #         api.update_status("actual #nzhellhole", attachment_url=tweet_full_url)
            #     elif tweet_version==1:
            #         api.update_status("and the rent keeps going up and up. no relief! #nzhellhole", attachment_url=tweet_full_url)
            #     elif tweet_version==2:
            #         api.update_status("more and more homeless and no government will address it #nzhellhole",
            #                           attachment_url=tweet_full_url)
            #     elif tweet_version==3:
            #         api.update_status("I guess it's comfortable to be smug about our #nzhellhole if you're not worried about affordable housing",
            #                           attachment_url=tweet_full_url)
            # else:

            try_retweet(t)

            #now follow that user if we aren't already
            if api.show_friendship(source_screen_name="aotearoayimby", target_id=t.author.id_str)[1].followed_by is False:
                #follow the user
                api.create_friendship(id=t.author.id_str)
            #have a sleep before you tweet another thing.
            time.sleep(600)                
