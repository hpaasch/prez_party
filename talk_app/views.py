from django.shortcuts import render
from django.views.generic import TemplateView
from TwitterAPI import TwitterAPI
from bs4 import BeautifulSoup
import requests

from talk_app.models import Tweet

tw_consumer_key = ''
tw_consumer_secret = ''

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(request):
        api = TwitterAPI(tw_consumer_key,
                         tw_consumer_secret,
                         auth_type='oAuth2')

        content = api.request('statuses/user_timeline', {'screen_name': '@hillaryclinton'})

        new_tweet_ids = []
        for tweet in content:
            new_tweet_ids.append(tweet['id'])

        old_tweet_ids = []
        old_tweets = Tweet.objects.all()
        for tweet in old_tweets:
            old_tweet_ids.append(tweet.twt_id)

        for tweet in content:
            if tweet['id'] not in old_tweet_ids:
                twt_id = tweet['id']
                username = tweet['user']['screen_name']
                created_at = tweet['created_at']
                text = tweet['text']
                retweet_count = tweet['retweet_count']
                Tweet.objects.create(twt_id=twt_id, username=username, created_at=created_at, text=text, retweet_count=retweet_count)

        tweet_list = Tweet.objects.all()
        context = {
            'tweet_list': tweet_list,
            }

        return context
