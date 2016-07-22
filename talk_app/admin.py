from django.contrib import admin

from talk_app.models import Tweet, DinnerParty, Candidate, Pundit, Question, Survey

# Register your models here.
admin.site.register(Tweet)
admin.site.register(DinnerParty)
admin.site.register(Candidate)
admin.site.register(Pundit)
admin.site.register(Question)
admin.site.register(Survey)
