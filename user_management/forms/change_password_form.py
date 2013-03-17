from django.forms import *

class Change_password_form(Form):
    old_pass = CharField(max_length=40, widget=PasswordInput, label="Current password")
    new_pass = CharField(max_length=40, widget=PasswordInput, label="New password")
    new_pass_repeat = CharField(max_length=40, widget=PasswordInput, label="Repeat")