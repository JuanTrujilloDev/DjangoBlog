from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from functools import partial

from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed!')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20, validators=[alphanumeric])
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_username(self, *args, **kwargs):
        instance = self.instance # adding obj instance -> 
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if instance is not None: #excluding the qs where the pk is = the instance pk
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username has been used! Try another !")
        return username

    def clean_email(self, *args, **kwargs):
        instance = self.instance # adding obj instance -> 
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if instance is not None: #excluding the qs where the pk is = the instance pk
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email has been used! Try another !")
        return email



class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self, *args, **kwargs):
        instance = self.instance # adding obj instance -> 
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if instance is not None: #excluding the qs where the pk is = the instance pk
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This username has been used! Try another !")
        return username

    def clean_email(self, *args, **kwargs):
        instance = self.instance # adding obj instance -> 
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if instance is not None: #excluding the qs where the pk is = the instance pk
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email has been used! Try another !")
        return email

DateInput = partial(forms.DateInput, {'class':'datepicker'})

class ProfileUpdateForm(forms.ModelForm):
    birthday = forms.DateField(widget=DateInput(), label="Date format: yyyy-mm-dd", required=False)
    class Meta:
        model = Profile
        fields = ['image','bio', 'birthday']

    