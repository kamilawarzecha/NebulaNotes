from datetime import date, datetime
from django.utils.timezone import now

# from django.forms import fields, forms
# from formset.widgets import DateTimeInput
from django import forms
from django.core.exceptions import ValidationError

from NebulaNotesApp.models import AstronomicalObject, AstronomicalObjectType, Galaxy, Event, User, Observation
from django.http import request


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = User.objects.filter(username=username)
            if not user.exists():
                self.add_error("username", "User does not exist!")
            else:
                user = user.first()
                if not user.check_password(password):
                    self.add_error("password", "Password is incorrect!")



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
        fields = ['name', 'type', 'distance_from_earth','description', 'discovery_year', 'galaxy']


class ObjectTypeForm(forms.ModelForm):
    class Meta:
        model = AstronomicalObjectType
        fields = ['name']


class GalaxyForm(forms.ModelForm):
    class Meta:
        model = Galaxy
        fields = ['name','type','description']


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})    )
    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'related_objects']


def validate_past_date(value):
    """Date validator to check if the date is in the past."""
    if value > now():
        raise ValidationError("You can't select a future date.")

class ObservationForm(forms.ModelForm):
    observation_date = forms.DateTimeField(
    widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
    input_formats=['%Y-%m-%dT%H:%M'],
    validators=[validate_past_date]
    )

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