from django.forms import *

class Edit_info_form(Form):
    city = CharField(required=False)
    age = IntegerField(required=False)