from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _



class Tag(models.Model):
    tagname = models.CharField(max_length=250, blank=True, unique=True)
    no_of_post = models.IntegerField(default=0)
    def __str__(self):
        return self.tagname

class BlockedPost(models.Model):
    post_id = models.CharField(max_length=250, blank=True, unique=True)
    def __str__(self):
        return self.post_id

class Post(models.Model):
    post_id = models.CharField(max_length=250, blank=True, unique=True)
    sentiments = models.FloatField(default=0.5)

    def __str__(self):
        return "Post Id is :  " + self.post_id + "    -->    " + str(self.sentiments)


