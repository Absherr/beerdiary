from django.forms import *
from beerdiary.models import Beer

class Beer_form(ModelForm):

    class Meta:
        model = Beer
        exclude=('community_mark','amount_of_marks')
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 3}),
        }
