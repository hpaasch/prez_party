from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout


from talk_app.views import (CreateAccountView, ProfileView, IndexView,
                            DinnerPartyCreateView,
                            PunditTweetListView,
                            USFinanceListView, USFinanceDeepListView,
                            LocalFinanceListView, LocalFinanceDeepListView,
                            TweetListView, PopularTweetListView, DinnerPartyUpdateView,
                            SurveyDetailView, VideoListView, CandidateKeynoteView,
                            PartyOverView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^logout/$', logout, name='logout'),
    url(r'^create_account/$', CreateAccountView.as_view(), name='create_account_view'),
    url(r'accounts/profile/$', ProfileView.as_view(), name='profile_view'),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^party/create/$', DinnerPartyCreateView.as_view(), name='dinner_party_create_view'),
    # url(r'^party/view/$', DinnerPartyListView.as_view(), name='dinner_party_list_view'),
    url(r'^opening/(?P<pk>\d+)/$', PunditTweetListView.as_view(), name='pundit_tweet_list_view'),
    url(r'^finance/national/(?P<pk>\d+)/$', USFinanceListView.as_view(), name='us_finance_list_view'),
    url(r'^finance/national/deep/(?P<pk>\d+)/$', USFinanceDeepListView.as_view(), name='us_finance_deep_list_view'),
    url(r'^finance/local/(?P<pk>\d+)/$', LocalFinanceListView.as_view(), name='local_finance_list_view'),
    url(r'^finance/local/deep/(?P<pk>\d+)/$', LocalFinanceDeepListView.as_view(), name='local_finance_deep_list_view'),
    url(r'^tweets/(?P<pk>\d+)/$', TweetListView.as_view(), name='tweet_list_view'),
    url(r'^tweets/candidate/(?P<pk>\d+)/$', PopularTweetListView.as_view(), name='popular_tweet_list_view'),
    url(r'^video/(?P<pk>\d+)/$', VideoListView.as_view(), name='video_list_view'),
    url(r'^video/candidate/(?P<pk>\d+)/$', CandidateKeynoteView.as_view(), name='candidate_keynote_view'),
    url(r'^survey/(?P<pk>\d+)/$', DinnerPartyUpdateView.as_view(), name='survey_create_view'),
    # url(r'^survey/$', SurveyDetailView.as_view(), name='survey_detail_view'),
    url(r'^party/over/$', PartyOverView.as_view(), name='party_over_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
