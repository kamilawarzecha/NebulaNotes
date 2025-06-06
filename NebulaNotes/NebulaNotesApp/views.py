from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.shortcuts import render

from NebulaNotesApp.forms import UserLoginForm, ObjectForm, ObjectTypeForm, GalaxyForm, EventForm, UserCreateForm, ObservationForm

from NebulaNotesApp.models import AstronomicalObject, AstronomicalObjectType, Galaxy, Event, Observation


User = get_user_model()

class Custom404View(View):
    """ A view that handles 404 errors"""
    def get(self, request, *args, **kwargs):
        return render(request, 'nebulanotes_app/404.html', status=404)

class UserLoginView(View):
    """ A view that displays the login form and handles the login action"""
    template_name = 'nebulanotes_app/login.html'
    form_class = UserLoginForm

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, context)


class UserLogoutView(View):
    """ A view that handles the logout action"""
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class UserCreateView(CreateView):
    """ A view that handles the creation of a new user"""
    model = User
    form_class = UserCreateForm
    template_name = 'nebulanotes_app/register.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request, user)
        return super().form_valid(form)


class HomeView(View):
    """ A view that displays the home page"""
    def get(self, request, *args, **kwargs):
        return render(request, 'nebulanotes_app/home.html')


class ObjectCreateView(CreateView):
    """ A view that displays the form for creating a new astronomical object"""
    model = AstronomicalObject
    form_class = ObjectForm
    template_name = 'nebulanotes_app/astronomicalobject_create.html'
    success_url = reverse_lazy("list-objects")


class ObjectsListView(ListView):
    """ A view that displays a filtered list of astronomical objects """
    model = AstronomicalObject
    template_name = 'nebulanotes_app/astronomicalobject_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.GET.get('type', '')

        if type_id:
            queryset = queryset.filter(type__id=type_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = AstronomicalObjectType.objects.all()
        return context


class ObjectDetailView(DetailView):
    """ A view that displays a single astronomical object"""
    model = AstronomicalObject
    template_name = 'nebulanotes_app/astronomicalobject_detail.html'

    def get_object(self):
        return get_object_or_404(AstronomicalObject, pk=self.kwargs['pk'])


class ObjectUpdateView(UpdateView):
    """ A view that displays a single astronomical object and lets the user update information about it"""
    model = AstronomicalObject
    template_name = 'nebulanotes_app/astronomicalobject_update.html'
    context_object_name = 'object'
    form_class = ObjectForm

    def get_success_url(self):
        return reverse_lazy("object-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self):
        return get_object_or_404(AstronomicalObject, pk=self.kwargs['pk'])


class ObjectDeleteView(DeleteView):
    """ A view that displays a single astronomical object and lets the user delete it"""
    model = AstronomicalObject
    template_name = 'nebulanotes_app/astronomicalobject_delete.html'
    success_url = reverse_lazy("list-objects")

    def get_object(self):
        return get_object_or_404(AstronomicalObject, pk=self.kwargs["pk"])


class ObjectTypeCreateView(CreateView):
    """ A view that displays the form for creating a new astronomical object type"""

    model = AstronomicalObjectType
    form_class = ObjectTypeForm
    template_name = 'nebulanotes_app/object_type_create.html'
    success_url = reverse_lazy("list-object-types")

    def form_valid(self, form):
        messages.success(self.request, "Object type was saved to the database!")
        return super().form_valid(form)


class ObjectTypesListView(ListView):
    """ A view that displays a list of astronomical object types"""
    model = AstronomicalObjectType
    template_name = 'nebulanotes_app/object_type_list.html'
    context_object_name = 'object_types'


class ObjectTypesDetailView(DetailView):
    """ A view that displays a single astronomical object type and its objects"""
    model = AstronomicalObjectType
    template_name = 'nebulanotes_app/object_type_detail.html'
    context_object_name = 'object_type'

    def get_object_or_404(self):
        return get_object_or_404(AstronomicalObjectType, pk=self.kwargs['pk'])


class ObjectTypeUpdateView(UpdateView):
    """ A view that displays a single astronomical object type and lets the user update its name"""
    model = AstronomicalObjectType
    template_name = 'nebulanotes_app/object_type_update.html'
    context_object_name = 'object_type'
    form_class = ObjectTypeForm

    def get_success_url(self):
        return reverse_lazy("object-type-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object_or_404(self):
        return get_object_or_404(AstronomicalObjectType, pk=self.kwargs['pk'])

class ObjectTypeDeleteView(DeleteView):
    """ A view that displays a single astronomical object type and lets the user delete it"""
    model = AstronomicalObjectType
    template_name = 'nebulanotes_app/object_type_delete.html'
    context_object_name = 'object_type'
    success_url = reverse_lazy("list-object-types")

    def get_object_or_404(self):
        return get_object_or_404(AstronomicalObjectType, pk=self.kwargs['pk'])


class GalaxyCreateView(CreateView):
    """ A view that displays the form for creating a new galaxy"""
    model = Galaxy
    form_class = GalaxyForm
    template_name = 'nebulanotes_app/galaxy_create.html'
    success_url = reverse_lazy("list-galaxies")

    def form_valid(self, form):
        messages.success(self.request, "Galaxy was saved to the database!")
        return super().form_valid(form)


class GalaxiesListView(ListView):
    """ A view that displays a list of galaxies"""
    model = Galaxy
    template_name = 'nebulanotes_app/galaxy_list.html'
    context_object_name = 'galaxies'


class GalaxyDetailView(DetailView):
    """ A view that displays a single galaxy and its objects"""
    model = Galaxy
    template_name = 'nebulanotes_app/galaxy_detail.html'
    context_object_name = 'galaxy'

    def get_object_or_404(self):
        return get_object_or_404(Galaxy, pk=self.kwargs['pk'])


class GalaxyUpdateView(UpdateView):
    """ A view that displays a single galaxy and lets the user update its name"""
    model = Galaxy
    template_name = 'nebulanotes_app/galaxy_update.html'
    context_object_name = 'galaxy'
    form_class = GalaxyForm

    def get_success_url(self):
        return reverse_lazy("galaxy-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object_or_404(self):
        return get_object_or_404(Galaxy, pk=self.kwargs['pk'])


class GalaxyDeleteView(DeleteView):
    """ A view that displays a single galaxy and lets the user delete it"""
    model = Galaxy
    template_name = 'nebulanotes_app/galaxy_delete.html'
    context_object_name = 'galaxy'
    success_url = reverse_lazy("list-galaxies")

    def get_object_or_404(self):
        return get_object_or_404(Galaxy, pk=self.kwargs['pk'])

class EventCreateView(CreateView):
    """ A view that displays the form for creating a new event"""
    model = Event
    form_class = EventForm
    template_name = 'nebulanotes_app/event_create.html'

    success_url = reverse_lazy("list-events")


class EventsListView(ListView):
    """ A view that displays a list of events"""
    model = Event
    template_name = 'nebulanotes_app/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_order = self.request.GET.get("sort", "asc")  # oldest first

        if sort_order == "desc":
            queryset = queryset.order_by("-date")  # newest first
        else:
            queryset = queryset.order_by("date")  # oldest first

        return queryset

class EventDetailView(DetailView):
    """ A view that displays a single event and its objects"""
    model = Event
    template_name = 'nebulanotes_app/event_detail.html'
    context_object_name = 'event'

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['pk'])


class EventUpdateView(UpdateView):
    """ A view that displays a single event and lets the user update its name"""
    model = Event
    template_name = 'nebulanotes_app/event_update.html'
    context_object_name = 'event'
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['pk'])


class EventDeleteView(DeleteView):
    """ A view that displays a single event and lets the user delete it"""
    model = Event
    template_name = 'nebulanotes_app/event_delete.html'
    context_object_name = 'event'

    def get_object(self):
        return get_object_or_404(Event, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy("list-events")


class ObservationCreateView(LoginRequiredMixin, CreateView):
    """ A view that displays the form for creating a new observation"""
    model = Observation
    form_class = ObservationForm
    template_name = 'nebulanotes_app/observation_create.html'
    success_url = reverse_lazy("list-observations")

    def form_valid(self, form):
        observation = form.save(commit=False)
        observation.user = self.request.user
        observation.save()
        return super().form_valid(form)


class ObservationsListView(LoginRequiredMixin, ListView):
    """ A view that displays a list of observations"""
    model = Observation
    template_name = 'nebulanotes_app/observation_list.html'
    context_object_name = 'observations'

    def get_queryset(self):
        return Observation.objects.filter(user=self.request.user).order_by("observation_date")


class ObservationDetailView(LoginRequiredMixin, DetailView):
    """ A view that displays a single observation and its objects"""
    model = Observation
    template_name = 'nebulanotes_app/observation_detail.html'
    context_object_name = 'observation'

    def get_object_or_404(self):
        return get_object_or_404(Observation, pk=self.kwargs['pk'])

class ObservationUpdateView(LoginRequiredMixin, UpdateView):
    """ A view that displays a single observation and lets the user update it"""
    model = Observation
    template_name = 'nebulanotes_app/observation_update.html'
    context_object_name = 'observation'
    form_class = ObservationForm

    def get_success_url(self):
        return reverse_lazy("observation-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_object_or_404(self):
        return get_object_or_404(Observation, pk=self.kwargs['pk'])


class ObservationDeleteView(LoginRequiredMixin, DeleteView):
    """ A view that displays a single observation and lets the user delete it"""
    model = Observation
    template_name = 'nebulanotes_app/observation_delete.html'
    context_object_name = 'observation'
    success_url = reverse_lazy("list-observations")

    def get_object_or_404(self):
        return get_object_or_404(Observation, pk=self.kwargs['pk'])
