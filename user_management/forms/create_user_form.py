from django.forms import *

class Create_user_form(Form):
    username = CharField(max_length=50)
    password = CharField(max_length=30, widget=PasswordInput)
    email = EmailField()

    city = CharField(max_length=40, required=False)
    age = IntegerField(required=False)

