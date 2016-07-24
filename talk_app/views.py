from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from TwitterAPI import TwitterAPI
from django.db.models import Sum
from django import forms

import requests
from django.core.urlresolvers import reverse_lazy

from talk_app.forms import SurveyForm
from talk_app.models import Tweet, DinnerParty, USFinance, StateFinance, ZIPFinance, Survey
import os


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        clinton = self.request.GET.get('clinton')
        trump = self.request.GET.get('trump')
        pundit = self.request.GET.get('pundit')
        clinton_url = 'https://www.youtube.com/embed/_j8xh_naQ6w?rel=0&amp;showinfo=0'
        trump_url = 'https://www.youtube.com/embed/pWcez2OwT9s?rel=0&amp;showinfo=0'
        pundit_url = 'https://www.youtube.com/embed/A43vWc9vdqM?rel=0&amp;showinfo=0'
        url = ''
        video = ''
        quiz = {}
        if clinton:
            video = 'clinton'
            url = clinton_url
        elif trump:
            video = 'trump'
            url = trump_url
        elif pundit:
            video = 'pundit'
            url = pundit_url
        elif quiz:
            quiz = SurveyForm()
        context = {
            'video': video,
            'url': url,
            'quiz': quiz,
            }
        return context


class QuizCreateView(CreateView):
    model = Survey
    template_name = 'quiz.html'
    fields = ['dinner', 'discussion_level', 'change_mind', 'changed', 'made_choice', 'chose', 'top_area']
    widgets = {'change_mind': forms.RadioSelect, 'made_choice': forms.RadioSelect}
    success_url = reverse_lazy('us_finance_list_view')

    def form_valid(self, form):
        quiz = form.save(commit=False)  #  half saves it
        quiz.host = self.request.user  #  attaches the user in the DB
        return super().form_valid(form)  #  fully saves and creates


class PopularTweetListView(TemplateView):
    template_name = 'popular_tweets.html'

    def get_context_data(request):

        tw_consumer_key = os.getenv("tw_consumer_key")
        tw_consumer_secret = os.getenv("tw_consumer_secret")

        api = TwitterAPI(tw_consumer_key,
                         tw_consumer_secret,
                         auth_type='oAuth2')

        candidates = [
            '@hillaryclinton',
            '@realdonaldtrump',
            '@drjillstein',
            '@govgaryjohnson',
            '@timkaine',
            '@cherihonkala',
            '@govbillweld',
            '@mike_pence',
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
                    popular = tweet['retweet_count'] + tweet['favorite_count']

                    Tweet.objects.create(
                        twt_id=tweet['id'],
                        username=tweet['user']['screen_name'],
                        created_at=tweet['created_at'],
                        text=tweet['text'],
                        retweet_count=tweet['retweet_count'],
                        favorite_count=tweet['favorite_count'],
                        popular = popular
                        )

        tweet_list = Tweet.objects.all()
        clinton_popular = Tweet.objects.filter(username='HillaryClinton').order_by('-popular')[:5]
        trump_popular = Tweet.objects.filter(username='realDonaldTrump').order_by('-popular')[:5]
        stein_popular = Tweet.objects.filter(username='DrJillStein').order_by('-popular')[:5]
        johnson_popular = Tweet.objects.filter(username='GovGaryJohnson').order_by('-popular')[:5]

        context = {
            'tweet_list': tweet_list,
            'clinton_popular': clinton_popular,
            'trump_popular': trump_popular,
            'stein_popular': stein_popular,
            'johnson_popular': johnson_popular,
            }

        return context


class TweetListView(ListView):
    model = Tweet
    template_name = 'tweets.html'

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


class USFinanceListView(ListView):
    model = USFinance
    template_name = 'us_finance.html'

    def get_context_data(request):
        x_api_key = os.getenv("x_api_key")
        us_url = 'https://api.propublica.org/campaign-finance/v1/2016/president/totals.json'

        headers = {
            "X-API-Key": x_api_key
            }

        us_response = requests.get(us_url, headers=headers).json()
        us_results = us_response['results']
        us_total = 1363831  # libertarian
        us_cash_on_hand = 0
        for item in us_results:
            us_total += item['total_receipts']
            us_cash_on_hand += item['cash_on_hand']
            USFinance.objects.update_or_create(
                slug=item['slug'],
                name=item['name'],
                total=item['total_receipts'],
                party=item['party'],
                as_of=item['date_coverage_to'],
                cash_on_hand=item['cash_on_hand'],
                candidate_name=item['candidate_name'])
        republican = USFinance.objects.filter(party='R')
        r_total = USFinance.objects.filter(party='R').aggregate(Sum('total'))
        democrat = USFinance.objects.filter(party='D')
        d_total = USFinance.objects.filter(party='D').aggregate(Sum('total'))
        libertarian = USFinance.objects.filter(party='L')
        green = USFinance.objects.filter(party='G')
        clinton = USFinance.objects.filter(slug='clinton')
        trump = USFinance.objects.filter(slug='trump')
        context = {
            'republican': republican,
            'r_total': r_total,
            'democrat': democrat,
            'd_total': d_total,
            'libertarian': libertarian,
            'green': green,
            'clinton': clinton,
            'trump': trump,
            'us_total': us_total,
            'us_cash_on_hand': us_cash_on_hand,
            }
        return context


class LocalFinanceListView(ListView):
    model = StateFinance
    template_name = 'state_finance.html'

    def get_context_data(request):
        x_api_key = os.getenv("x_api_key")

        headers = {
            "X-API-Key": x_api_key
            }
        states = ['NC', 'SC']
        for state in states:
            state_url = 'https://api.propublica.org/campaign-finance/v1/2016/president/states/{}.json'.format(state)
            state_response = requests.get(state_url, headers=headers).json()
            state_results = state_response['results']
            state_total = 0
            for item in state_results:
                state_total += float(item['total'])
                StateFinance.objects.update_or_create(
                    full_name=item['full_name'],
                    candidate=item['candidate'],
                    party=item['party'],
                    total=item['total'],
                    contribution_count=item['contribution_count'],
                    state=item['state'],
                    )
        nc_total = StateFinance.objects.filter(state='NC').aggregate(Sum('total'))
        sc_total = StateFinance.objects.filter(state='SC').aggregate(Sum('total'))
        clinton_list = StateFinance.objects.filter(full_name='Hillary Clinton')
        trump_list = StateFinance.objects.filter(full_name='Donald J. Trump')
        context = {
            'nc_total': nc_total,
            'sc_total': sc_total,
            'clinton_list': clinton_list,
            'trump_list': trump_list,
            }
        return context
