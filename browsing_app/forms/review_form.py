from django.forms import *
from beerdiary.models import Review

class Review_form(ModelForm):
    class Meta:
        model = Review

        exclude = ('author','date','beer','averaged_mark')
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 3}),
            'flavour_review': Textarea(attrs={'cols': 40, 'rows': 3}),
            'aroma_review': Textarea(attrs={'cols': 40, 'rows': 3}),
            'appearance_review': Textarea(attrs={'cols': 40, 'rows': 3}),
            'palate_review': Textarea(attrs={'cols': 40, 'rows': 3})}