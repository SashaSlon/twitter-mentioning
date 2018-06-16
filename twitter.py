import os
from datetime import datetime, timedelta
from itertools import groupby

import tweepy


class MentioningCounter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
        self.auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def count(self, words):
        mentioning = {}
        last_date = datetime.now() - timedelta(days=7)
        for word in words:
            tweets = []
            mentioning[word] = tweets
            for tweet in tweepy.Cursor(self.api.search, q=word, lang='ru', rpp=100, show_user=False).items():
                if tweet.created_at < last_date:
                    break
                tweets.append(tweet)
        for k, v in mentioning.items():
            mentioning[k] = list((k, sum(1 for _ in g)) for k, g in groupby(v, key=lambda x: x.created_at.date()))
        return mentioning
