from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

SENTIMENT_TYPE_CHOICES = (
    ('0', 'Offensive'),
    ('1', 'Adult'),
    ('2', 'Racy'),
    ('3', 'Mature'),
)

POST_TYPE_CHOICES = (
    ('0', 'image'),
    ('1', 'text'),
)

POST_CATEGORY_CHOICES = (
    ('0','i_to_a'),
    ('1','t_to_a'),
)

TAG_CHOICES = (
    ('0','generic'),
    ('1','account'),
)
class UserTag(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    tagname = models.CharField(max_length=250)
    tag_type = models.CharField(max_length=1, choices=TAG_CHOICES, null=True)

    def  __str__(self):
        return self.user.username + self.tagname + str(self.tag_type)

class UserPost(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    postid = models.CharField(max_length=250)
    post_category = models.CharField(max_length=1,choices=POST_CATEGORY_CHOICES,null=True)
    sentiment_score = models.FloatField(default=0.0)
    tagname = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.user.username + self.postid + self.post_category

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
    count = models.IntegerField(default=0)
    def __str__(self):
        return "" + str(self.user.username) + "    -->    " + str(self.sentiment_type)



