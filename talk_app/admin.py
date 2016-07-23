from django.contrib import admin

from talk_app.models import Tweet, DinnerParty, Candidate, Pundit, Question, Survey, USFinance, StateFinance, ZIPFinance


class StateFinanceAdmin(admin.ModelAdmin):
        list_display = ['full_name', 'state', 'total']


class USFinanceAdmin(admin.ModelAdmin):
        list_display = ['name', 'party', 'total']


class TweetAdmin(admin.ModelAdmin):
        list_display = ['username', 'popular', 'created_at']
        search_fields = ['username']


admin.site.register(Tweet, TweetAdmin)
admin.site.register(DinnerParty)
admin.site.register(Candidate)
admin.site.register(Pundit)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(USFinance, USFinanceAdmin)
admin.site.register(StateFinance, StateFinanceAdmin)
admin.site.register(ZIPFinance)
