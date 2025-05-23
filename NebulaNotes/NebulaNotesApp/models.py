from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Galaxy(models.Model):
    TYPE_CHOICES = [

        ("Spiral", "Spiral"),
        ("Elliptical", "Elliptical"),
        ("Irregular", "Irregular"),
        ("Other", "Other")
    ]
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="galaxy_images/", blank=True, null=True)

    def __str__(self):
        return self.name



class AstronomicalObjectType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AstronomicalObject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    type = models.ForeignKey(AstronomicalObjectType, on_delete=models.CASCADE)
    distance_from_earth = models.FloatField(help_text="in light years")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="astronomy_images/", blank=True, null=True)
    discovery_year = models.IntegerField(null=True, blank=True)
    galaxy = models.ForeignKey(Galaxy, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_objects = models.ManyToManyField(AstronomicalObject, blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    related_objects = models.ManyToManyField(AstronomicalObject, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


class Observation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    astronomical_object = models.ForeignKey(AstronomicalObject, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    observation_date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Observation of  {self.astronomical_object.name} {self.event.name} made by {self.user.username}"
