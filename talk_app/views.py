from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Sum
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from TwitterAPI import TwitterAPI
import requests
import os

from talk_app.models import (Tweet, Candidate, DinnerParty, USFinance,
                            StateFinance, ZIPFinance, Survey, Profile, Video)
from talk_app.forms import VideoForm


class CreateAccountView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class ProfileView(ListView):
    model = Profile
    template_name = 'talk_app/profile_list.html'

    def get_queryset(self):
        return DinnerParty.objects.filter(host=self.request.user)

class IndexView(TemplateView):
    template_name = 'index.html'


class DinnerPartyCreateView(CreateView):
    template_name = 'party_create.html'
    model = DinnerParty
    fields = ['party_name', 'pundit', 'candidate', 'video', 'friend_names', 'friend_mix']
    success_url = reverse_lazy('profile_view')

    # this method is NOT yet allowing user to add a video to the party
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['video_form'] = Video.objects.all()
        print(context)
        return context

    def form_valid(self, form):
        dinnerparty = form.save(commit=False)
        dinnerparty.host = self.request.user
        return super().form_valid(form)


class DinnerPartyListView(ListView):
    template_name = 'view_party.html'
    model = DinnerParty

    def get_queryset(self):
        return DinnerParty.objects.filter(host=self.request.user)


class VideoListView(ListView):
    model = Video
    template_name = 'video_list.html'

    # def get_queryset(self):
    #     keynote = DinnerParty.objects.get()

    def get_context_data(self, **kwargs):
        clinton = self.request.GET.get('clinton')
        trump = self.request.GET.get('trump')
        pundit = self.request.GET.get('pundit')
        candidates = Candidate.objects.all()
        clinton_url = 'https://www.youtube.com/embed/_j8xh_naQ6w?rel=0&amp;showinfo=0'
        trump_url = 'https://www.youtube.com/embed/pWcez2OwT9s?rel=0&amp;showinfo=0'
        pundit_url = 'https://www.youtube.com/embed/A43vWc9vdqM?rel=0&amp;showinfo=0'
        m_obama_url = 'https://www.youtube.com/watch?v=AaKju-TrEmU'
        url = ''
        video = ''
        if clinton:
            video = 'clinton'
            url = clinton_url
        elif trump:
            video = 'trump'
            url = trump_url
        elif pundit:
            video = 'pundit'
            url = pundit_url

        photos = Candidate.objects.all()
        context = {
            'candidates': candidates,
            'video': video,
            'url': url,
            'photos': photos,
            }
        return context


class QuizCreateView(CreateView):
    model = Survey
    template_name = 'quiz.html'
    fields = ['dinner', 'discussion_intensity', 'change_mind', 'what_changed',
            'made_choice', 'who_choose', 'top_topic']
    widgets = {'change_mind': forms.RadioSelect, 'made_choice': forms.RadioSelect}
    success_url = reverse_lazy('party_over_view')

    def form_valid(self, form):
        quiz = form.save(commit=False)  #  half saves it
        quiz.host = self.request.user  #  attaches the user in the DB
        return super().form_valid(form)  #  fully saves and creates


class USFinanceListView(ListView):
    model = USFinance
    template_name = 'us_finance.html'

    def get_context_data(self):
        x_api_key = os.environ["x_api_key"]
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
                defaults = {
                'name': item['name'],
                'total': item['total_receipts'],
                'party': item['party'],
                'as_of': item['date_coverage_to'],
                'cash_on_hand': item['cash_on_hand'],
                'candidate_name': item['candidate_name'],
                })
        republican = USFinance.objects.filter(party='R')[:2]
        r_total = USFinance.objects.filter(party='R').aggregate(Sum('total'))
        democrat = USFinance.objects.filter(party='D')[:2]
        d_total = USFinance.objects.filter(party='D').aggregate(Sum('total'))
        libertarian = USFinance.objects.filter(party='L')
        green = USFinance.objects.filter(party='G')
        clinton = USFinance.objects.filter(slug='clinton')
        trump = USFinance.objects.filter(slug='trump')
        republicans = self.request.GET.get('republicans')
        democrats = self.request.GET.get('democrats')
        party_compare = False
        if republicans or democrats:
            context = {
                'party_compare': party_compare,

                }
        context = {
            'republican': republican,
            'democrat': democrat,
            'r_total': r_total,
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
        x_api_key = os.environ["x_api_key"]

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


class PopularTweetListView(TemplateView):
    template_name = 'popular_tweets.html'

    def get_context_data(self, **kwargs):
        tw_consumer_key = os.getenv("tw_consumer_key")
        tw_consumer_secret = os.getenv("tw_consumer_secret")
        api = TwitterAPI(tw_consumer_key,
                         tw_consumer_secret,
                         auth_type='oAuth2')

        candidates = Candidate.objects.all()
        candidate = '@realDonaldTrump'
        # candidate = self.request.GET.get('candidate')
        popular_tweets = []
        popular = []

        if candidate:
            candidate = candidate[1:]
            content = api.request('statuses/user_timeline', {'screen_name': candidate})
            for tweet in content:
                Tweet.objects.update_or_create(
                    twt_id = tweet['id'],
                    defaults={
                    'username': tweet['user']['screen_name'],
                    'created_at': tweet['created_at'],
                    'text': tweet['text'],
                    'retweet_count': tweet['retweet_count'],
                    'favorite_count': tweet['favorite_count'],
                    'popular': (tweet['retweet_count'] + tweet['favorite_count']),
                    })

            popular = Tweet.objects.filter(username=candidate).order_by('-popular')[:5]
            tweet_ids = []
            for tweet in popular:
                tweet_ids.append(tweet.twt_id)
            for item in tweet_ids:
                tweet = requests.get("https://api.twitter.com/1.1/statuses/oembed.json?id={}".format(item)).json()["html"]
                popular_tweets.append(tweet)

        context = {
            'candidates': candidates,
            'popular_tweets': popular_tweets,
            }
        return context


# this should go on a 'Go Deep' page that includes search plus links to candidate sites too
class TweetListView(ListView):
    model = Tweet
    template_name = 'tweets.html'


class PartyOverView(TemplateView):
    template_name = 'party_over.html'
