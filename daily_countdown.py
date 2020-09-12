import pytz
from datetime import datetime
import time
import random

def variable_ratio_daily_countdown_tweet(api,delay_after_tweeting=0,tweet_inverse_odds=15):
    """tweets out a daily countdown to the wellington spatial plan submission
    does so probabilistically, i.e., when run n times a day, each time it is run there is a 1/n chance it will tweet
    so as to spread the tweets right across the period.
    """

    #get new zealand timezone
    nztz = pytz.timezone("Pacific/Auckland")
    #get now and today
    now = datetime.now(nztz)
    today = datetime.date(now)

    spatial_plan_deadline = datetime.strptime("2020-10-05 17:00","%Y-%m-%d %H:%M")
    days_left_to_submit = (spatial_plan_deadline.date() - today).days


    # for tweets going out between 8 AM and up to 11 PM
    permitted_start_time = datetime.combine(today,datetime.strptime("07:59", "%H:%M").time()).astimezone(nztz)
    permitted_end_time = datetime.combine(today, datetime.strptime("22:50", "%H:%M").time()).astimezone(nztz)

    #determine if now is within the permitted range
    is_within_time_range = (now>permitted_start_time) & (now < permitted_end_time)

    #this is about 15 hours of the day so that's what we'll use
    chance_of_tweeting = 1/tweet_inverse_odds
    random.seed(datetime.now())
    is_lucky_hour = (random.random() <chance_of_tweeting)

    if is_lucky_hour and is_within_time_range and days_left_to_submit>0:
        print("tweeting a reminder about wellington spatial plan")
        tweet_version = random.sample([0,1,2,3],1)[0]
        if tweet_version==0:
            tweet_text = (str(days_left_to_submit) +
            " days left to submit for the Wellington Spatial Plan. " +
            "All it takes is 10 minutes for you to influence the future of Wellington." +
            " Submit here: https://planningforgrowth.wellington.govt.nz/spatial-plan"
                          )
        elif tweet_version==1:
            tweet_text = (
            "There are " + str(days_left_to_submit) + " days to get in a submission for the Wellington Spatial Plan. " +
            "It sets the limits for how much housing can be built in Wellington for the next THIRTY YEARS! " +
            "Here's the link to submit. https://planningforgrowth.wellington.govt.nz/spatial-plan"
                          )
        elif tweet_version==2:
            tweet_text = (
                str(days_left_to_submit) + " sleeps left until the submission deadline for the Wellington Spatial Plan closes. " +
                "It takes 10 minutes of your time - if you haven't already, get your submission in now. " +
                "https://planningforgrowth.wellington.govt.nz/spatial-plan"
            )
        elif tweet_version==3:
            tweet_text = (
                str(days_left_to_submit) + " days left to have a say on the Wellington Spatial Plan. " +
                    "It takes 10 minutes and determines whether Wellington housing is affordable for the next 30 years." +
                    " tell the council we need more housing! " +
                    "https://planningforgrowth.wellington.govt.nz/spatial-plan"
            )

        print(tweet_text)

        api.update_status(tweet_text)

        time.sleep(delay_after_tweeting)

# from authenticate import *
#
# api = get_authenticated_api()
#
# for i in range(0,10):
#      variable_ratio_daily_countdown_tweet(api,1)



