from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import booking.models as bkm

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Please enter your First name.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# Chnage to tag form
class EditTagForm(forms.ModelForm):
    class Meta:
        model = bkm.Tag
        fields = '__all__'


class FacilityForm(forms.ModelForm):
    class Meta:
        model = bkm.Facility
        fields = '__all__'
        widgets = {'admin': forms.HiddenInput(), 'longitude': forms.HiddenInput(), 'latitude': forms.HiddenInput()}
        exclude = ('admin', 'longitude', 'latitude',)


class FacilityTagForm(forms.Form):
    new_tags = forms.CharField(max_length=200)
    remove_tags = forms.CharField(max_length=200)


class SearchForm(forms.Form):
    sports_tag = forms.ModelChoiceField(queryset=bkm.Tag.objects.all().order_by('id'))
    location = forms.CharField(min_length=3, max_length=100)
    distance = forms.ChoiceField(choices=(
        (1, "1"),
        (2, "2"),
        (5, "5"),
        (10, "10"),
        (15, "15"),
        (20, "20"),
        (25, "25")))


class BookingForm(forms.Form):
    timeslot = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField()
