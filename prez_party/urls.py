from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout


from talk_app.views import CreateAccountView, ProfileView, IndexView, DinnerPartyCreateView, DinnerPartyListView, USFinanceListView, LocalFinanceListView, TweetListView, PopularTweetListView, QuizCreateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout, name='logout'),
    url(r'^create_account/$', CreateAccountView.as_view(), name='create_account_view'),
    url(r'accounts/profile/$', ProfileView.as_view(), name='profile_view'),

    # url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^party/create/$', DinnerPartyCreateView.as_view(), name='dinner_party_create_view'),
    url(r'^party/view/$', DinnerPartyListView.as_view(), name='dinner_party_list_view'),
    url(r'^finance/national/$', USFinanceListView.as_view(), name='us_finance_list_view'),
    url(r'^finance/local/$', LocalFinanceListView.as_view(), name='local_finance_list_view'),
    url(r'^tweets/$', TweetListView.as_view(), name='tweet_list_view'),
    url(r'^tweets/popular/$', PopularTweetListView.as_view(), name='popular_tweet_list_view'),
    url(r'^quiz/video/$', QuizCreateView.as_view(), name='quiz_create_view'),

]
