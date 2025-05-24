import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.contrib.auth.models import User
from NebulaNotesApp.models import AstronomicalObject, AstronomicalObjectType, Galaxy, Event, Observation
import datetime
from django.utils.timezone import make_aware

User = get_user_model()


@pytest.fixture
def test_user(db):
    """Creates a test user."""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def astronomical_objects(db):
    """Creates example astronomical objects for tests."""
    type1 = AstronomicalObjectType.objects.create(name="Planet")
    type2 = AstronomicalObjectType.objects.create(name="Star")

    obj1 = AstronomicalObject.objects.create(name="Mars", type=type1, distance_from_earth=0.0000158)
    obj2 = AstronomicalObject.objects.create(name="Sirius", type=type2, distance_from_earth=8.6)
    obj3 = AstronomicalObject.objects.create(name="Jupiter", type=type1, distance_from_earth=0.000082)

    return [obj1, obj2, obj3]


@pytest.fixture
def galaxies(db):
    """Creates example galaxies for tests."""
    galaxy1 = Galaxy.objects.create(name="Milky Way", type="Spiral")
    galaxy2 = Galaxy.objects.create(name="Andromeda", type="Elliptical")
    galaxy3 = Galaxy.objects.create(name="Triangulum", type="Irregular")

    return [galaxy1, galaxy2, galaxy3]


@pytest.fixture
def events(db):
    """Creates example events for tests."""
    event1 = Event.objects.create(name="Lunar Eclipse", date="2021-12-31", description="A total lunar eclipse visible worldwide")
    event2 = Event.objects.create(name="Christmas", date="2021-12-25", description="Merry Christmas!")

    return [event1, event2]


@pytest.fixture
def observations(db, astronomical_objects, events):
    """Creates example observations for tests."""
    obs1 = Observation.objects.create(user=User.objects.get(username="testuser"), astronomical_object=astronomical_objects[0], event=events[0], observation_date =make_aware(datetime.datetime(2024, 4, 15, 20, 0, 0)), location="test_location", notes="A beautiful planet")
    obs2 = Observation.objects.create(user=User.objects.get(username="testuser"), astronomical_object=astronomical_objects[1], event=events[0], observation_date=make_aware(datetime.datetime(2024, 4, 16, 22, 30, 0)), location="test_location", notes="A beautiful star")

    return [obs1, obs2]