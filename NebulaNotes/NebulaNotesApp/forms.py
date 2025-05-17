from datetime import date
from email.mime import image

from django import forms
from django.core.exceptions import ValidationError

from NebulaNotesApp.models import AstronomicalObject, AstronomicalObjectType, Galaxy, Event, User, Observation
from django.http import request


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(label='First Name (optional)', required=False)
    last_name = forms.CharField(label='Last Name (optional)', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise ValidationError("Passwords must match!")
        return password_confirm


class ObjectForm(forms.ModelForm):
    class Meta:
        model = AstronomicalObject
        fields = ['name', 'type', 'distance_from_earth','description', 'image', 'discovery_year', 'galaxy']


class ObjectTypeForm(forms.ModelForm):
    class Meta:
        model = AstronomicalObjectType
        fields = ['name']


class GalaxyForm(forms.ModelForm):
    class Meta:
        model = Galaxy
        fields = ['name','type','description', 'image']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'related_objects']


class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['location', 'notes', 'astronomical_object', 'event', 'observation_date']
        exclude = ['user']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance