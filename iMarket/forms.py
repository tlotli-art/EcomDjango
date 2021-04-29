from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

#Class to create customise our django user creation form
class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    #Class to customise the fields within the form
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']

   

