from django.forms import *
from beerdiary.models import Country

class Country_form(ModelForm):

    class Meta:
        model = Country