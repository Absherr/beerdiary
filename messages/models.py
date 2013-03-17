from django.db import models
from beerdiary.models import User_profile
from django import forms

reasons = (
    ('new_beer', "New beer"),
    ('new_brewery', "New brewery"),
    ('new_country', "New country"),
    ('changes', 'Change of parameters'),
    ('bug','Found bug'),
    ('report','Report comment/review'),
    ('other','Other'),
)

class Message(models.Model):
    author = models.ForeignKey(User_profile, blank=True, null=True)
    reason = models.CharField(max_length=40, choices=reasons)
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now= True)

class MessageForm(forms.ModelForm):
    hash = forms.CharField(max_length=32, widget=forms.HiddenInput, required=False)
    captcha = forms.CharField(max_length=5)

    class Meta:

        model = Message
        exclude = ('author','date')

