from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=25)
    website = models.URLField()
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    affiliation = models.CharField(max_length=20)  # choices to come


class Pundit(models.Model):
    name = models.CharField(max_length=25)
    website = models.URLField()
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    employer = models.CharField(max_length=30)
    affiliation = models.CharField(max_length=20)  # choices to come


class Profile(models.Model):
    user = models.OneToOneField('auth.User')
    friends = models.IntegerField(null=True, blank=True)
    friend_mix = models.CharField(max_length=30, null=True, blank=True)  # choices to come
    occupation = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    registered = models.CharField(max_length=20)  # choices to come
    affiliation = models.CharField(max_length=20)  # choices to come


class Question(models.Model):
    question_type = models.CharField(max_length=30)  # choices to come.
    intensity = models.IntegerField()  # pick list of 1-5
    wonk_level = models.IntegerField()  # pick list of 1-3
    category = models.CharField(max_length=30)


class DinnerParty(models.Model):
    name = models.CharField(max_length=30)
    host = models.ForeignKey('auth.User')
    pundit = models.ForeignKey(Pundit)
    candidate = models.ForeignKey(Candidate)


class Survey(models.Model):
    dinner = models.ForeignKey(DinnerParty)
    host = models.ForeignKey('auth.User')
    discussion_level = models.IntegerField()
    change_mind = models.BooleanField()
    made_choice = models.BooleanField()
    top_area = models.CharField(max_length=30)  # choices to come


class Tweet(models.Model):
    twt_id = models.IntegerField()
    username = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    created_at = models.TextField()
    text = models.TextField()
    retweet_count = models.IntegerField(null=True)
    favorite_count = models.IntegerField(null=True)

    class Meta:
        ordering = ['-created_at']
