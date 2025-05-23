"""
URL configuration for NebulaNotes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from NebulaNotesApp.views import (
    HomeView,
    UserLoginView,
    UserLogoutView,
    UserCreateView,
    ObjectCreateView,
    ObjectsListView,
    ObjectDetailView,
    ObjectDeleteView,
    ObjectUpdateView,
    ObjectTypeCreateView,
    ObjectTypesListView,
    ObjectTypesDetailView,
    ObjectTypeUpdateView,
    ObjectTypeDeleteView,
    GalaxyCreateView,
    GalaxiesListView,
    GalaxyDetailView,
    GalaxyUpdateView,
    GalaxyDeleteView,
    EventCreateView,
    EventsListView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    ObservationCreateView,
    ObservationsListView,
    ObservationDetailView,
    ObservationUpdateView,
    ObservationDeleteView,
    Custom404View

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name="home"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('register/', UserCreateView.as_view(), name="register"),
    path('object/create', ObjectCreateView.as_view(), name="create-object"),
    path('objects/list', ObjectsListView.as_view(), name="list-objects"),
    path('object/<int:pk>', ObjectDetailView.as_view(), name="object-detail"),
    path('object/<int:pk>/delete', ObjectDeleteView.as_view(), name="object-delete"),
    path('object/<int:pk>/update', ObjectUpdateView.as_view(), name="object-update"),
    path('type/create', ObjectTypeCreateView.as_view(), name="create-object-type"),
    path('types/list', ObjectTypesListView.as_view(), name="list-object-types"),
    path('type/<int:pk>', ObjectTypesDetailView.as_view(), name="object-type-detail"),
    path('type/<int:pk>/update', ObjectTypeUpdateView.as_view(), name="object-type-update"),
    path('type/<int:pk>/delete', ObjectTypeDeleteView.as_view(), name="object-type-delete"),
    path('galaxy/create', GalaxyCreateView.as_view(), name="create-galaxy"),
    path('galaxies/list', GalaxiesListView.as_view(), name="list-galaxies"),
    path('galaxy/<int:pk>', GalaxyDetailView.as_view(), name="galaxy-detail"),
    path('galaxy/<int:pk>/update', GalaxyUpdateView.as_view(), name="galaxy-update"),
    path('galaxy/<int:pk>/delete', GalaxyDeleteView.as_view(), name="galaxy-delete"),
    path('event/create', EventCreateView.as_view(), name="create-event"),
    path('events/list', EventsListView.as_view(), name="list-events"),
    path('event/<int:pk>', EventDetailView.as_view(), name="event-detail"),
    path('event/<int:pk>/update', EventUpdateView.as_view(), name="event-update"),
    path('event/<int:pk>/delete', EventDeleteView.as_view(), name="event-delete"),
    path('observation/create', ObservationCreateView.as_view(), name="create-observation"),
    path('observations/list', ObservationsListView.as_view(), name="list-observations"),
    path('observation/<int:pk>', ObservationDetailView.as_view(), name="observation-detail"),
    path('observation/<int:pk>/update', ObservationUpdateView.as_view(), name="observation-update"),
    path('observation/<int:pk>/delete', ObservationDeleteView.as_view(), name="observation-delete"),



]

handler404 = Custom404View.as_view()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)