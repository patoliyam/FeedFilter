from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

SENTIMENT_TYPE_CHOICES = (
    ('0', 'Obscene'),
    ('1', 'Adult'),
    ('2', 'Racy'),
    ('3', 'Other'),
)

POST_TYPE_CHOICES = (
    ('0', 'image'),
    ('1', 'text'),
)

class Tag(models.Model):
    tagname = models.CharField(max_length=250, blank=True, unique=True)
    no_of_post = models.IntegerField(default=0)
    def __str__(self):
        return self.tagname

class BlockedPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post_id = models.CharField(max_length=250, null=True)
    post_type = models.CharField(max_length=1, choices=POST_TYPE_CHOICES, null=True)
    text_or_url = models.CharField(max_length=2000, null=True)
    def __str__(self):
        return self.post_id

class Stats(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    sentiment_type = models.CharField(max_length=1, choices=SENTIMENT_TYPE_CHOICES, null=True)
    count_0 = models.IntegerField(default=0)
    count_1 = models.IntegerField(default=0)
    count_2 = models.IntegerField(default=0)
    count_3 = models.IntegerField(default=0)
    def __str__(self):
        return "Post Id is :  " + str(self.user.username) + "    -->    " + str(self.sentiment_type)

