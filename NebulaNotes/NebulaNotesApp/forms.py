from datetime import date
from email.mime import image

from django import forms
from django.core.exceptions import ValidationError

from NebulaNotesApp.models import AstronomicalObject, AstronomicalObjectType, Galaxy, Event


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ObjectForm(forms.ModelForm):
    class Meta:
        model = AstronomicalObject
        fields = ['name', 'type', 'distance_from_earth','description', 'image', 'discovery_date', 'galaxy']


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