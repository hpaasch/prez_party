from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.staticfiles.templatetags.staticfiles import static


REGISTERED = 'I am currently registered to vote'
NEVER_REGISTERED = 'I have never been registered'
NOT_CURRENT = 'I was registered but am not now'
NOT_ACCURATE = 'Registered but not fully accurate'
CONSERVATIVE = 'Conservative'
PROGESSIVE = 'Progressive'
MIXED = 'Mixed'
OTHER = 'Other'
DEMOCRAT = 'Democrat'
INDEPENDENT = 'Independent'
REPUBLICAN = 'Republican'
LIBERTARIAN = 'Libertarian'
GREENPARTY = 'GreenParty'
DEEP = 'Deep'
MEDIUM = 'Medium'
SHALLOW = 'Shallow'
VALUES = 'Values'
POLICY = 'Policy'
PERSONAL_QUALITIES = 'Personal qualities'


class Candidate(models.Model):
    AFFILIATION_CHOICES = (
        (DEMOCRAT, 'Democrat'),
        (REPUBLICAN, 'Republican'),
        (LIBERTARIAN, 'Libertarian'),
        (GREENPARTY, 'GreenParty'),
        )
    name = models.CharField(max_length=25)
    website = models.URLField()
    video_one = models.CharField(max_length=50, null=True, blank=True)
    video_two = models.CharField(max_length=50, null=True, blank=True)
    video_three = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    affiliation = models.CharField(choices=AFFILIATION_CHOICES, max_length=20)
    office = models.CharField(max_length=20)
    twt_username = models.CharField(max_length=20, default='BarackObama')

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('talk_app/img/flagA.jpg')
        # return 'http://firstviewconsultants.com/beetletheme/wp-content/uploads/2015/08/US-flag.jpg'

class Pundit(models.Model):
    AFFILIATION_CHOICES = (
        (DEMOCRAT, 'Democrat'),
        (INDEPENDENT, 'Independent'),
        (REPUBLICAN, 'Republican'),
        (LIBERTARIAN, 'Libertarian'),
        (GREENPARTY, 'GreenParty'),
        )
    name = models.CharField(max_length=25)
    website = models.URLField()
    video_one = models.CharField(max_length=50, null=True, blank=True)
    video_two = models.CharField(max_length=50, null=True, blank=True)
    video_three = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    employer = models.CharField(max_length=30)
    affiliation = models.CharField(choices=AFFILIATION_CHOICES, max_length=20)
    twt_username = models.CharField(max_length=20, default='BarackObama')

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return static('talk_app/img/flagA.jpg')
        # return 'http://firstviewconsultants.com/beetletheme/wp-content/uploads/2015/08/US-flag.jpg'

class Profile(models.Model):
    AFFILIATION_CHOICES = (
        (DEMOCRAT, 'Democrat'),
        (INDEPENDENT, 'Independent'),
        (REPUBLICAN, 'Republican'),
        (LIBERTARIAN, 'Libertarian'),
        (GREENPARTY, 'GreenParty'),
        )
    REGISTERED_CHOICES = (
        (REGISTERED, 'I am currently registered to vote'),
        (NEVER_REGISTERED, 'I have never been registered'),
        (NOT_CURRENT, 'I was registered but am not now'),
        (NOT_ACCURATE, 'Registered but not fully accurate'),
        )
    user = models.OneToOneField('auth.User')
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    occupation = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    registered_to_vote = models.CharField(choices=REGISTERED_CHOICES, default='', max_length=50)
    affiliation = models.CharField(choices=AFFILIATION_CHOICES, max_length=20, null=True, blank=True)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        # return 'http://firstviewconsultants.com/beetletheme/wp-content/uploads/2015/08/US-flag.jpg'
        return static('talk_app/img/flagA.jpg')


class DinnerParty(models.Model):
    DISCUSSION_CHOICES = (
        (DEEP, 'Deep'),
        (MEDIUM, 'Medium'),
        (SHALLOW, 'Shallow'),
        )
    TOPIC_CHOICES = (
        (VALUES, 'Values'),
        (POLICY, 'Policy'),
        (PERSONAL_QUALITIES, 'Personal qualities'),
        )
    AFFILIATION_CHOICES = (
        (DEMOCRAT, 'Democrat'),
        (INDEPENDENT, 'Independent'),
        (REPUBLICAN, 'Republican'),
        (LIBERTARIAN, 'Libertarian'),
        (GREENPARTY, 'GreenParty'),
        (MIXED, 'Mixed'),
        )
    party_name = models.CharField(max_length=30)
    host = models.ForeignKey('auth.User')
    pundit = models.ForeignKey(Pundit)
    candidate = models.ForeignKey(Candidate)
    friend_names = models.CharField(max_length=80, null=True, blank=True)
    friend_mix = models.CharField(choices=AFFILIATION_CHOICES, default=MIXED, max_length=20)
    question_one = models.CharField(choices=DISCUSSION_CHOICES, max_length=60, null=True)
    question_two = models.CharField(choices=TOPIC_CHOICES, max_length=60, null=True)
    question_three = models.TextField(max_length=200, null=True)
    question_four = models.TextField(max_length=200, null=True)
    question_five = models.TextField(max_length=200, null=True)
    question_six = models.TextField(max_length=200, null=True)
    question_seven = models.TextField(max_length=200, null=True)

    def __str__(self):
        return str(self.party_name)


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

@receiver(post_save, sender='auth.User')
def create_user_profile(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')

    if created:
        Profile.objects.create(user=instance)
