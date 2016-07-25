from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=25)
    website = models.URLField()
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    affiliation = models.CharField(max_length=20)
    office = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Pundit(models.Model):
    name = models.CharField(max_length=25)
    website = models.URLField()
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    employer = models.CharField(max_length=30)
    affiliation = models.CharField(max_length=20)  # choices to come

    def __str__(self):
        return self.name

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
    intensity = models.CharField(max_length=20)
    wonk_level = models.CharField(max_length=20)
    category = models.CharField(max_length=30)
    text = models.TextField(null=True, blank=True)


class DinnerParty(models.Model):
    name = models.CharField(max_length=30, verbose_name='Give your party a name')
    host = models.ForeignKey('auth.User')
    pundit = models.ForeignKey(Pundit)
    candidate = models.ForeignKey(Candidate)

    def __str__(self):
        return self.name


class Survey(models.Model):
    dinner = models.ForeignKey(DinnerParty)
    host = models.ForeignKey('auth.User')
    discussion_level = models.IntegerField()
    change_mind = models.BooleanField()
    changed = models.TextField(null=True, blank=True)
    made_choice = models.BooleanField()
    chose = models.TextField(null=True, blank=True)
    top_area = models.CharField(max_length=30)  # choices to come

    def __str__(self):
        return self.dinner

class Tweet(models.Model):
    twt_id = models.BigIntegerField()
    username = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    created_at = models.TextField()
    text = models.TextField()
    retweet_count = models.IntegerField(null=True)
    favorite_count = models.IntegerField(null=True)
    popular = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.username


class USFinance(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=30)
    party = models.CharField(max_length=5)
    total = models.FloatField()
    as_of = models.CharField(max_length=10)
    cash_on_hand = models.FloatField()
    candidate_name = models.CharField(max_length=30)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-cash_on_hand']


class StateFinance(models.Model):
    full_name = models.CharField(max_length=30)
    candidate = models.CharField(max_length=30)
    party = models.CharField(max_length=3)
    total = models.FloatField()
    contribution_count = models.IntegerField()
    state = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name


class ZIPFinance(models.Model):
    full_name = models.CharField(max_length=30)
    candidate = models.CharField(max_length=30)
    party = models.CharField(max_length=3)
    total = models.FloatField()
    contribution_count = models.IntegerField()
    zip_code = models.IntegerField()

    def __str__(self):
        return self.full_name
