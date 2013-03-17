from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from taggit.models import Tag

class Marked_tag(models.Model):
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag)
    mark = models.FloatField(default=0)
    amount = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.user)+" "+str(self.tag.name)+" "+str(self.mark)+" "+str(self.amount)

admin.site.register(Marked_tag)