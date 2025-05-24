from datetime import date
from django.utils.timezone import make_aware
import datetime

import pytest
from django.urls import reverse
from conftest import test_user, astronomical_objects, galaxies, events, observations
from NebulaNotesApp.models import Observation, AstronomicalObject, AstronomicalObjectType, Galaxy, Event


def test_404_page_loads(client):
    """Checks that the 404 page loads correctly."""
    response = client.get("/404/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_login_view(client, test_user):
    """Checks that the login view allows a user to log in."""
    response = client.post("/login/", {"username": "testuser", "password": "testpass"})
    assert response.status_code == 302
    assert response.url == "/"


@pytest.mark.django_db
def test_login_view_invalid_form(client):
    """Checks that the login view doesn't allow a user to log in with invalid data."""
    response = client.post("/login/", {"username": "xx", "password": "yy"})
    assert response.status_code == 200
    assert b"User does not exist!" in response.content


@pytest.mark.django_db
def test_login_view_invalid_credentials(client,test_user):
    """Checks that the login view doesn't allow a user to log in with invalid credentials."""
    response = client.post("/login/", {"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 200
    assert b"Password is incorrect!" in response.content


@pytest.mark.django_db
def test_logout_view(client, test_user):
    """Checks that the logout view allows a user to log out."""
    response = client.get("/logout/")
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_create_view(client):
    """Checks that the user create view allows a user to create a new user."""
    response = client.post("/register/", {"username": "newuser", "email": "email@test.com", "first_name":"Test", "last_name":"Test", "password": "testpass", "password_confirm": "testpass"})
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_create_view_invalid_form(client):
    """Checks that the user create view doesn't allow a user to create a new user with invalid data."""

    response = client.post("/register/", {
        "username": "",
        "email": "",
        "first_name":"",
        "last_name":"",
        "password": "testpass",
        "password_confirm": "testpass"})
    assert response.status_code == 200
    assert b"This field is required." in response.content

@pytest.mark.django_db
def test_user_create_view_password_missmatch(client):
    """Checks that the user create view doesn't allow a user to create a new view with mismatching passwords."""

    response = client.post("/register/", {
        "username": "testuser",
        "email": "user@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass",
        "password_confirm": "wrongpass"
    })
    assert response.status_code == 200
    assert b"Passwords must match!" in response.content


def test_home_page_loads(client):
    """Checks that the home page loads correctly."""
    response = client.get(reverse("home"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_object_create_view(client, astronomical_objects):
    """Checks that the object create view allows a user to create a new object."""
    obj_type = astronomical_objects[0].type
    response = client.post(reverse("create-object"), {"name": "test_object", "description": "test_description", "type": obj_type.id, "distance_from_earth": "0.0"})
    assert response.status_code == 302
    assert response.url == reverse("list-objects")
    assert AstronomicalObject.objects.filter(name="test_object").exists()


@pytest.mark.django_db
def test_object_create_view_invalid_form(client, astronomical_objects):
    """Checks that the object create view doesn't allow a user to create a new object with invalid data."""
    obj_type = astronomical_objects[0].type
    response = client.post(reverse("create-object"), {"name": "", "description": "", "type": obj_type.id, "distance_from_earth": ""})
    assert response.status_code == 200
    assert b"This field is required." in response.content


@pytest.mark.django_db
def test_object_create_view_with_image(client, astronomical_objects):
    """Checks that the object create view allows a user to create a new object with an image."""
    obj_type = astronomical_objects[0].type
    response = client.post(reverse("create-object"), {"name": "test_object", "description": "test_description", "type": obj_type.id, "distance_from_earth": "0.0", "image": "test_image.jpg"})
    assert response.status_code == 302
    assert response.url == reverse("list-objects")
    assert AstronomicalObject.objects.filter(name="test_object").exists()
#dopracować

@pytest.mark.django_db
def test_list_objects(client, astronomical_objects):
    """Checks that the object list view displays all astronomical objects."""

    response = client.get(reverse("list-objects"))
    assert response.status_code == 200
    assert len(response.context["objects"]) == len(astronomical_objects)
    view_objects = [
        obj.name for obj in response.context["objects"]
    ]
    assert view_objects == ["Mars", "Sirius", "Jupiter"]


@pytest.mark.django_db
def test_object_detail_view(client, astronomical_objects):
    """Checks that the object detail view displays the correct object."""
    mars = astronomical_objects[0]
    response = client.get(reverse("object-detail", args=[mars.id]))
    assert response.status_code == 200
    assert response.context["object"] == mars
    assert response.context["object"].name == "Mars"
    assert response.context["object"].type.name == "Planet"
    assert response.context["object"].distance_from_earth == 0.0000158


@pytest.mark.django_db
def test_object_detail_view_not_found(client, astronomical_objects):
    """Checks that the object detail view returns a 404 page if the object is not found."""
    response = client.get(reverse("object-detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_object_update_view(client, astronomical_objects):
    """Checks that the object update view allows a user to update an object."""
    mars = astronomical_objects[0]
    response = client.post(reverse("object-update", args=[mars.id]), {"name": "Mars", "description": "test_description", "type": mars.type.id, "distance_from_earth": "0.0"})
    assert response.status_code == 302
    assert response.url == reverse("object-detail", args=[mars.id])
    mars.refresh_from_db()
    assert mars.name == "Mars"
    assert mars.description == "test_description"
    assert mars.distance_from_earth == 0.0


@pytest.mark.django_db
def test_object_update_view_invalid_form(client, astronomical_objects):
    """Checks that the object update view doesn't allow a user to update an object with invalid data."""
    mars = astronomical_objects[0]
    response = client.post(reverse("object-update", args=[mars.id]), {"name": "", "description": "", "type": mars.type.id, "distance_from_earth": ""})
    assert response.status_code == 200
    assert b"This field is required." in response.content
    mars.refresh_from_db()
    assert mars.name == "Mars"
    assert mars.description == ""
    assert mars.distance_from_earth == 0.0000158


@pytest.mark.django_db
def test_object_delete_view(client, astronomical_objects):
    """Checks that the object delete view allows a user to delete an object."""
    mars = astronomical_objects[0]
    response = client.post(reverse("object-delete", args=[mars.id]))
    assert response.status_code == 302
    assert response.url == reverse("list-objects")
    assert not AstronomicalObject.objects.filter(name="Mars").exists()


@pytest.mark.django_db
def test_object_delete_view_not_found(client, astronomical_objects):
    """Checks that the object delete view returns a 404 page if the object is not found."""

    response = client.get(reverse("object-delete", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_object_type_create_view(client):
    """Checks that the object type create view allows a user to create a new object type."""
    response = client.post(reverse("create-object-type"), {"name": "test_type"})
    assert response.status_code == 302
    assert response.url == reverse("list-object-types")
    assert AstronomicalObjectType.objects.filter(name="test_type").exists()


@pytest.mark.django_db
def test_object_type_create_view_invalid_form(client):
    """Checks that the object type create view doesn't allow a user to create a new object type with invalid data."""
    response = client.post(reverse("create-object-type"), {"name": ""})
    assert response.status_code == 200
    assert b"This field is required." in response.content


@pytest.mark.django_db
def test_object_type_list_view(client, astronomical_objects):
    """Checks that the object type list view displays all object types."""

    response = client.get(reverse("list-object-types"))
    assert response.status_code == 200
    expected_types = AstronomicalObjectType.objects.all()

    assert len(response.context["object_types"]) == len(expected_types)

    view_types = [obj_type.name for obj_type in response.context["object_types"]]
    expected_type_names = [obj_type.name for obj_type in expected_types]

    assert view_types == expected_type_names


@pytest.mark.django_db
def test_object_type_detail_view(client, astronomical_objects):
    """Checks that the object type detail view displays the correct object type."""
    planet = astronomical_objects[0].type
    response = client.get(reverse("object-type-detail", args=[planet.id]))
    assert response.status_code == 200
    assert response.context["object_type"] == planet


@pytest.mark.django_db
def test_object_type_detail_view_not_found(client, astronomical_objects):
    """Checks that the object type detail view returns a 404 page if the object type is not found."""
    response = client.get(reverse("object-type-detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_object_type_update_view(client, astronomical_objects):
    """Checks that the object type update view allows a user to update an object type."""
    planet = astronomical_objects[0].type
    response = client.post(reverse("object-type-update", args=[planet.id]), {"name": "test_type"})
    assert response.status_code == 302
    assert response.url == reverse("object-type-detail", args=[planet.id])
    planet.refresh_from_db()
    assert planet.name == "test_type"


@pytest.mark.django_db
def test_object_type_update_view_invalid_form(client, astronomical_objects):
    """Checks that the object type update view doesn't allow a user to update an object type with invalid data."""
    planet = astronomical_objects[0].type
    response = client.post(reverse("object-type-update", args=[planet.id]), {"name": ""})
    assert response.status_code == 200
    assert b"This field is required." in response.content


@pytest.mark.django_db
def test_object_type_delete_view(client, astronomical_objects):
    """Checks that the object type delete view allows a user to delete an object type."""
    planet = astronomical_objects[0].type
    response = client.post(reverse("object-type-delete", args=[planet.id]))
    assert response.status_code == 302
    assert response.url == reverse("list-object-types")
    assert not AstronomicalObjectType.objects.filter(name="Planet").exists()


@pytest.mark.django_db
def test_object_type_delete_view_not_found(client, astronomical_objects):
    """Checks that the object type delete view returns a 404 page if the object type is not found."""
    response = client.get(reverse("object-type-delete", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_galaxy_create_view(client, galaxies):
    """Checks that the galaxy create view allows a user to create a new galaxy."""

    response = client.post(reverse("create-galaxy"), {
        "name": "test_galaxy",
        "description": "test_description",
        "type": "Spiral"
    })

    assert response.status_code == 302
    assert response.url == reverse("list-galaxies")

    assert Galaxy.objects.filter(name="test_galaxy").exists()


@pytest.mark.django_db
def test_galaxy_create_view_invalid_form(client, galaxies):
    """Checks that the galaxy create view doesn't allow a user to create a new galaxy with invalid data."""

    response = client.post(reverse("create-galaxy"), {
        "name": "",
        "description": "",
        "type": ""
    })
    assert response.status_code == 200
    assert b"This field is required." in response.content


@pytest.mark.django_db
def test_galaxy_list_view(client, galaxies):
    """Checks that the galaxy list view displays all galaxies."""

    response = client.get(reverse("list-galaxies"))
    assert response.status_code == 200
    assert len(response.context["galaxies"]) == len(galaxies)
    view_galaxies = [
        galaxy.name for galaxy in response.context["galaxies"]
    ]
    assert view_galaxies == ["Milky Way", "Andromeda", "Triangulum"]


@pytest.mark.django_db
def test_galaxy_detail_view(client, galaxies):
    """Checks that the galaxy detail view displays the correct galaxy."""
    milky_way = galaxies[0]
    response = client.get(reverse("galaxy-detail", args=[milky_way.id]))
    assert response.status_code == 200
    assert response.context["galaxy"] == milky_way


@pytest.mark.django_db
def test_galaxy_detail_view_not_found(client, galaxies):
    """Checks that the galaxy detail view returns a 404 page if the galaxy is not found."""
    response = client.get(reverse("galaxy-detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_galaxy_update_view(client, galaxies):
    """Checks that the galaxy update view allows a user to update a galaxy."""
    milky_way = galaxies[0]
    response = client.post(reverse("galaxy-update", args=[milky_way.id]), {
        "name": "Milky Way",
        "description": "test_description",
        "type": "Other"
    })
    assert response.status_code == 302
    assert response.url == reverse("galaxy-detail", args=[milky_way.id])
    milky_way.refresh_from_db()
    assert milky_way.name == "Milky Way"
    assert milky_way.description == "test_description"
    assert milky_way.type == "Other"


@pytest.mark.django_db
def test_galaxy_update_view_invalid_form(client, galaxies):
    """Checks that the galaxy update view doesn't allow a user to update a galaxy with invalid data."""
    milky_way = galaxies[0]
    response = client.post(reverse("galaxy-update", args=[milky_way.id]), {
        "name": "",
        "description": "",
        "type": ""
    })
    assert response.status_code == 200
    assert b"This field is required." in response.content
    milky_way.refresh_from_db()
    assert milky_way.name == "Milky Way"
    assert milky_way.description == ""
    assert milky_way.type == "Spiral"


@pytest.mark.django_db
def test_galaxy_delete_view(client, galaxies):
    """Checks that the galaxy delete view allows a user to delete a galaxy."""
    milky_way = galaxies[0]
    response = client.post(reverse("galaxy-delete", args=[milky_way.id]))
    assert response.status_code == 302
    assert response.url == reverse("list-galaxies")
    assert not Galaxy.objects.filter(name="Milky Way").exists()


@pytest.mark.django_db
def test_galaxy_delete_view_not_found(client, galaxies):
    """Checks that the galaxy delete view returns a 404 page if the galaxy is not found."""
    response = client.get(reverse("galaxy-delete", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_event_create_view(client, events):
    """Checks that the event create view allows a user to create a new event."""
    response = client.post(reverse("create-event"), {
        "name": "test_event",
        "description": "test_description",
        "date": "2001-01-01"
    })
    assert response.status_code == 302
    assert response.url == reverse("list-events")
    assert Event.objects.filter(name="test_event").exists()

@pytest.mark.django_db
def test_event_create_view_with_related_objects(client, events, astronomical_objects):
    """Checks that the event create view allows a user to create a new event with related objects."""
    response = client.post(reverse("create-event"), {
        "name": "test_event",
        "description": "test_description",
        "date": "2001-01-01",
        "related_objects": astronomical_objects[0].id,
    })
    assert response.status_code == 302
    assert response.url == reverse("list-events")
    assert Event.objects.filter(name="test_event").exists()

@pytest.mark.django_db
def test_event_create_view_invalid_form(client, events):
    """Checks that the event create view doesn't allow a user to create a new event with invalid data."""
    response = client.post(reverse("create-event"), {
        "name": "",
        "description": "",
        "date": "",
        "related_objects": "",
    })
    assert response.status_code == 200
    assert b"This field is required." in response.content


@pytest.mark.django_db
def test_event_list_view(client, events):
    """Checks that the event list view displays all events."""
    response = client.get(reverse("list-events"))
    assert response.status_code == 200
    assert len(response.context["events"]) == len(events)
    view_events = [
        event.name for event in response.context["events"]
    ]
    assert view_events == ["Christmas", "Lunar Eclipse"]


@pytest.mark.django_db
def test_event_list_view_sorted_asc(client, events):
    """Checks that the event list view sorts events in ascending order by date."""
    response = client.get(reverse("list-events"), {"sort": "asc"})

    assert response.status_code == 200
    view_events = [event.name for event in response.context["events"]]

    expected_order = ["Christmas", "Lunar Eclipse"]
    assert view_events == expected_order


@pytest.mark.django_db
def test_event_list_view_sorted_desc(client, events):
    """Checks that the event list view sorts events in descending order by date."""
    response = client.get(reverse("list-events"), {"sort": "desc"})

    assert response.status_code == 200
    view_events = [event.name for event in response.context["events"]]

    expected_order = ["Lunar Eclipse", "Christmas"]
    assert view_events == expected_order


@pytest.mark.django_db
def test_event_detail_view(client, events):
    """Checks that the event detail view displays the correct event."""
    lunar_eclipse = events[0]
    response = client.get(reverse("event-detail", args=[lunar_eclipse.id]))
    assert response.status_code == 200
    assert response.context["event"] == lunar_eclipse


@pytest.mark.django_db
def test_event_detail_view_not_found(client, events):
    """Checks that the event detail view returns a 404 page if the event is not found."""
    response = client.get(reverse("event-detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_event_update_view(client, events, astronomical_objects):
    """Checks that the event update view allows a user to update an event."""
    lunar_eclipse = events[0]
    response = client.post(reverse("event-update", args=[lunar_eclipse.id]), {
        "name": "Lunar Eclipse",
        "description": "test_description",
        "date": "2001-01-01",
        "related_objects": astronomical_objects[0].id,
    })
    assert response.status_code == 302
    assert response.url == reverse("event-detail", args=[lunar_eclipse.id])
    lunar_eclipse.refresh_from_db()
    assert lunar_eclipse.name == "Lunar Eclipse"
    assert lunar_eclipse.description == "test_description"
    assert lunar_eclipse.date == date(2001, 1, 1)


@pytest.mark.django_db
def test_event_update_view_invalid_form(client, events):
    """Checks that the event update view doesn't allow a user to update an event with invalid data."""
    lunar_eclipse = events[0]
    response = client.post(reverse("event-update", args=[lunar_eclipse.id]), {
        "name": "",
        "description": "",
        "date": "",
        "related_objects": "",
    })
    assert response.status_code == 200
    assert b"This field is required." in response.content
    lunar_eclipse.refresh_from_db()
    assert lunar_eclipse.name == "Lunar Eclipse"
    assert lunar_eclipse.description == "A total lunar eclipse visible worldwide"
    assert lunar_eclipse.date == date(2021, 12, 31)


@pytest.mark.django_db
def test_event_delete_view(client, events):
    """Checks that the event delete view allows a user to delete an event."""
    lunar_eclipse = events[0]
    response = client.post(reverse("event-delete", args=[lunar_eclipse.id]))
    assert response.status_code == 302
    assert response.url == reverse("list-events")
    assert not Event.objects.filter(name="Lunar Eclipse").exists()


@pytest.mark.django_db
def test_event_delete_view_not_found(client, events):
    """Checks that the event delete view returns a 404 page if the event is not found."""
    response = client.get(reverse("event-delete", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_observation_create_view(client, test_user, observations, astronomical_objects, events):
    """Checks that the observation create view allows a logged-in user to create a new observation."""

    client.login(username=test_user.username, password="testpass")

    aware_date = make_aware(datetime.datetime(2021, 12, 31, 12, 0, 0))

    response = client.post(reverse("create-observation"),{
        "user": test_user.id,
        "location": "test_location",
        "notes": "test_notes",
        "observation_date": aware_date,
        "astronomical_object": astronomical_objects[0].id,
        "event": events[0].id,

    })
    assert response.status_code == 302
    assert response.url == reverse("list-observations")

    assert Observation.objects.filter(notes="test_notes").exists()


@pytest.mark.django_db
def test_observation_create_view_invalid_form(client, test_user, observations):
    """Checks that the observation create view doesn't allow a logged-in user to create a new observation with invalid data."""
    client.login(username=test_user.username, password="testpass")
    response = client.post(reverse("create-observation"),{
        "user": test_user.id,
        "location": "",
        "notes": "",
        "observation_date": "",
        "astronomical_object": "",
        "event": "",
    })
    assert response.status_code == 200


@pytest.mark.django_db
def test_observation_list_view(client, test_user, observations):
    """Checks that the observation list view displays all observations."""
    client.login(username=test_user.username, password="testpass")
    response = client.get(reverse("list-observations"))
    assert response.status_code == 200
    assert len(response.context["observations"]) == len(observations)
    view_observations = [ observation.notes for observation in response.context["observations"] ]
    assert view_observations == ["A beautiful planet", "A beautiful star"]


@pytest.mark.django_db
def test_observation_detail_view(client, test_user, observations):
    """Checks that the observation detail view displays the correct observation."""
    client.login(username=test_user.username, password="testpass")
    observation = observations[0]
    response = client.get(reverse("observation-detail", args=[observation.id]))
    assert response.status_code == 200
    assert response.context["observation"] == observation


@pytest.mark.django_db
def test_observation_detail_view_not_found(client, test_user, observations):
    """Checks that the observation detail view returns a 404 page if the observation is not found."""
    client.login(username=test_user.username, password="testpass")
    response = client.get(reverse("observation-detail", args=[999]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_observation_update_view(client, test_user, observations, astronomical_objects, events):
    """Checks that the observation update view allows a logged-in user to update an observation."""
    client.login(username=test_user.username, password="testpass")
    observation = observations[0]
    response = client.post(reverse("observation-update", args=[observation.id]),{
        "user": test_user.id,
        "location": "test_location",
        "notes": "test_notes",
        "observation_date": "2001-01-01",
        "astronomical_object": astronomical_objects[0].id,
        "event": events[0].id,
    })
    assert response.status_code == 302
    assert response.url == reverse("observation-detail", args=[observation.id])
    observation.refresh_from_db()
    assert observation.notes == "test_notes"


@pytest.mark.django_db
def test_observation_update_view_invalid_form(client, test_user, observations):
    """Checks that the observation update view doesn't allow a logged-in user to update an observation with invalid data."""
    client.login(username=test_user.username, password="testpass")
    observation = observations[0]
    response = client.post(reverse("observation-update", args=[observation.id]),{
        "user": test_user.id,
        "location": "",
        "notes": "",
    })
    assert response.status_code == 200
    assert b"This field is required." in response.content
    observation.refresh_from_db()
    assert observation.notes == "A beautiful planet"


@pytest.mark.django_db
def test_observation_delete_view(client, test_user, observations):
    """Checks that the observation delete view allows a logged-in user to delete an observation."""
    client.login(username=test_user.username, password="testpass")
    observation = observations[0]
    response = client.post(reverse("observation-delete", args=[observation.id]))
    assert response.status_code == 302
    assert response.url == reverse("list-observations")
    assert not Observation.objects.filter(notes="A beautiful planet").exists()


@pytest.mark.django_db
def test_observation_delete_view_not_found(client, test_user, observations):
    """Checks that the observation delete view returns a 404 page if the observation is not found."""
    client.login(username=test_user.username, password="testpass")
    response = client.get(reverse("observation-delete", args=[999]))
    assert response.status_code == 404
