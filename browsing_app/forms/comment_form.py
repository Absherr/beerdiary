from django.forms import *
from beerdiary.models import Comment

class Comment_form(ModelForm):
    class Meta:
        model = Comment
        exclude = ('author','date','beer')
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 3}),}