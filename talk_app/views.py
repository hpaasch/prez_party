from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from TwitterAPI import TwitterAPI
from bs4 import BeautifulSoup
import requests
from django.core.urlresolvers import reverse_lazy


from talk_app.models import Tweet, DinnerParty
import os


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(request):

        tw_consumer_key = os.getenv("tw_consumer_key")
        tw_consumer_secret = os.getenv("tw_consumer_secret")
        x_api_key = os.getenv("x_api_key")

        api = TwitterAPI(tw_consumer_key,
                         tw_consumer_secret,
                         auth_type='oAuth2')

        candidates = [
            '@hillaryclinton',
            '@realdonaldtrump',
            '@drjillstein',
            '@govgaryjohnson',
            ]

        for candidate in candidates:

            content = api.request('statuses/user_timeline', {'screen_name': candidate})

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


class DinnerPartyCreateView(CreateView):
    template_name = 'party_create.html'
    model = DinnerParty
    fields = ['name', 'pundit', 'candidate']
    success_url = reverse_lazy('index_view')

    def form_valid(self, form):
        dinnerparty = form.save(commit=False)
        dinnerparty.host = self.request.user
        return super().form_valid(form)


class DinnerPartyListView(ListView):
    template_name = 'view_party.html'
    model = DinnerParty

    # def get_context_data(request):
