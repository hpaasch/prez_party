
from django.conf.urls import url
from django.contrib import admin


from talk_app.views import IndexView, DinnerPartyCreateView, DinnerPartyListView, USFinanceListView, LocalFinanceListView, TweetListView, PopularTweetListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^party/create/$', DinnerPartyCreateView.as_view(), name='dinner_party_create_view'),
    url(r'^party/view/$', DinnerPartyListView.as_view(), name='dinner_party_list_view'),
    url(r'^finance/national/$', USFinanceListView.as_view(), name='us_finance_list_view'),
    url(r'^finance/local/$', LocalFinanceListView.as_view(), name='local_finance_list_view'),
    url(r'^tweets/$', TweetListView.as_view(), name='tweet_list_view'),
    url(r'^tweets/popular/$', PopularTweetListView.as_view(), name='popular_tweet_list_view'),

]
