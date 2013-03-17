from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models

from taggit.managers import TaggableManager
from taggit.models import Tag

class User_profile(models.Model):
    user = models.OneToOneField(User)
    city = models.CharField(max_length=40, blank = True, null=True)
    age = models.IntegerField(blank = True, null=True)

    def __unicode__(self):
        return self.user.username

class Beer_style(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Beer style"
        verbose_name_plural = "Beer styles"
        ordering = ['name']

class Country(models.Model):
    name=models.CharField(max_length=60)
    added = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name="Country"
        verbose_name_plural="Countries"
    def __unicode__(self):
        return self.name

class Brewery(models.Model):
    name = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    country = models.ForeignKey(Country)
    added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Brewery"
        verbose_name_plural = "Breweries"
        ordering = ['name']

class Beer (models.Model):
    name = models.CharField(max_length=30)
    brewery = models.ForeignKey(Brewery)
    abv = models.FloatField(blank = True, null = True)

    description = models.TextField(blank = True, null = True)
    beer_style = models.ForeignKey(Beer_style, blank=True, null =True)

    community_mark = models.FloatField(blank=True, null=True, default=0)
    amount_of_marks = models.IntegerField(blank=True, null=True, default=0)

    image = models.ImageField(upload_to="img/beer_img",blank=True, null=True)
    tags = TaggableManager()

    added = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name + ", " + self.brewery.name

    class Meta:
        ordering = ['name']

class Comment(models.Model):
    author = models.ForeignKey(User_profile)
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

    description = models.TextField()
    beer = models.ForeignKey(Beer)

    def __unicode__(self):
        return self.author.user.username + " (" + str(self.date)+ " " +str(self.time)+"): " + self.description

list_of_marks = [1,1.5,2,2.5,3,3.5,4,4.5,5]
list_of_choises=[]
for item in list_of_marks:
    list_of_choises.append((item,item))

class Review(models.Model):

    author = models.ForeignKey(User_profile)
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

    beer = models.ForeignKey(Beer)

    flavour_review = models.TextField()
    flavour_mark = models.FloatField(choices=list_of_choises)

    aroma_review = models.TextField()
    aroma_mark = models.FloatField(choices=list_of_choises)

    appearance_review = models.TextField()
    appearance_mark = models.FloatField(choices=list_of_choises)

    palate_review = models.TextField()
    palate_mark = models.FloatField(choices=list_of_choises)

    description = models.TextField()

    averaged_mark= models.FloatField()

    def __unicode__(self):
        return "REVIEW:" + self.author.user.username + " (" + str(self.date)+ " " +str(self.time)+"): " + self.description

class News(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    author = models.ForeignKey(User_profile)
    content = models.TextField()
    class Meta:
        verbose_name = "Piece of news"
        verbose_name_plural = "News"
    def __unicode__(self):
        return str(self.author) + " " + str(self.date) + " " + str(self.time) + " " + str(self.content[:20])+"..."

admin.site.register(User_profile)
admin.site.register(Beer_style)
admin.site.register(Country)
admin.site.register(Brewery)
admin.site.register(Beer)
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(News)
