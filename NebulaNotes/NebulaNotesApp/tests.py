import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
# from NebulaNotesApp.models import Observation


@pytest.mark.django_db
class TestObservationsListView:
    def setup_method(self):
        """Create a test user and log them in"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

    def test_redirect_if_not_logged_in(self, client):
        """Redirect to login if the user isn't logged in"""
        response = client.get(reverse("list-observations"))
        assert response.status_code == 302  # Redirect to login
        assert "/login/?next=" in response.url

    def test_access_for_logged_in_user(self, client):
        """If the user is logged in, they should be able to access the page"""
        client.login(username="testuser", password="testpass")
        response = client.get(reverse("list-observations"))
        assert response.status_code == 200
        assert "observation_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestObservationsCreateView:
    def setup_method(self):
        """Create a test user and log them in"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

    def test_redirect_if_not_logged_in(self, client):
        """Redirect to login if the user isn't logged in"""
        response = client.get(reverse("list-observations"))
        assert response.status_code == 302
        assert "observation_list.html" in [t.name for t in response.templates]