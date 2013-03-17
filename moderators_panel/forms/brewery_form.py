from django.forms import *
from beerdiary.models import Brewery

class Brewery_form(ModelForm):

    class Meta:
        model = Brewery
