
from django.conf.urls import url
from django.contrib import admin


from talk_app.views import IndexView, DinnerPartyCreateView, DinnerPartyListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^party/create/$', DinnerPartyCreateView.as_view(), name='dinner_party_create_view'),
    url(r'^party/view/$', DinnerPartyListView.as_view(), name='dinner_party_list_view'),


]
