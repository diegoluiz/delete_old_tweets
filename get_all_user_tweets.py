#!/usr/bin/env python3

import sys
import twitter
import os
import datetime

from credentials import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    for tweet in timeline:
        tweet.created_at = datetime.datetime.fromtimestamp(tweet.created_at_in_seconds)

    return timeline


if __name__ == "__main__":
    api = twitter.Api(
        CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET
    )
    screen_name = sys.argv[1]
    now = datetime.datetime.now()
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    date_limit_in_days = 90

    tweets_to_delete = list(filter(lambda x: (now - x.created_at).days > date_limit_in_days, timeline))

    print('Deleting {} tweets older than {} days'.format(len(tweets_to_delete), date_limit_in_days))
    for tweet in tweets_to_delete:
        api.DestroyStatus(tweet.id)

    print('Tweets deleted')
