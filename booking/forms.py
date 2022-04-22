from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from booking.models import Tag


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Please enter your First name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EditTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

