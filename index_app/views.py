from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from index_app.forms import SpeakerForm, VenueForm
from .models import Event, Category, Guest, Venue, Location
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

User = get_user_model()
script_dir = os.path.dirname(os.path.abspath(__file__))


#################################################
################ Global views ###################
#################################################

def index(request):
    context = {}
    context['upcoming'] = Event.objects.all()

    return render(request, 'index.html', context)


@login_required(login_url='login')
def dashboard(request, pk):
    context = {}
    mode = request.GET.get('mode')
    my_user = User.objects.get(id=pk)
    # Retrieve categories
    categories = Category.objects.all()
    event_dict = {}

    if mode and mode == 'guest':
        events = Event.objects.filter(
            guest__user=my_user)

        for category in categories:
            events = events.filter(category=category)
            event_dict[category.name] = events

        context['event_dict'] = event_dict

        context['attendance'] = Guest.objects.filter(user=my_user)

        return render(request, 'dashboard_guest.html', context)

    for category in categories:
        events = Event.objects.filter(
            host=my_user)
        events = events.filter(category=category)
        if events:
            event_dict[category.name] = events

    context['event_dict'] = event_dict

    return render(request, 'dashboard_host.html', context)


def gallery(request):
    return render(request, 'gallery.html', {})


def contact(request):
    return render(request, 'contacts.html', {})


#################################################
########### Event related views #################
#################################################

# Create
class EventCreateView(generic.CreateView):
    """Creates an event object
    """
    model = Event
    fields = ('title', 'guests', 'description',
              'start_date', 'end_date', 'poster')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by('-pk')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            category_name = request.GET.get("category")
            category = Category.objects.get(name=category_name)
            event = form.save(commit=False)
            event.category = category
            event.host = request.user
            event.save()
            return JsonResponse({'status': 'success', 'msg': 'Event added successfully', 'url': event.get_absolute_url()})

        return JsonResponse({'status': 'error', 'errors': form.errors})

# Read


class EventListView(generic.ListView):
    """Returns a list of available events 
    """

    model = Event
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        query = self.request.GET.get("query")
        if query:
            context['query'] = query

        category = self.request.GET.get("category")
        if category:
            context['select_category'] = category

        return context

    def get_queryset(self):
        queryset = super().get_queryset().filter(draft=False)
        query = self.request.GET.get("query")
        category = self.request.GET.get('category')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        if category:
            queryset = queryset.filter(
                Q(category__name__iexact=category)
            )

        return queryset


class EventDetailView(generic.DetailView):
    """Returns a single event object
    """
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['attending'] = Guest.objects.filter(
                user=self.request.user, event_id=self.kwargs['pk'])
            context["owner"] = self.model.objects.filter(
                id=self.kwargs['pk'], host=self.request.user)
            context['speaker_form'] = SpeakerForm()

        return context


# Update
class EventUpdateView(generic.UpdateView):
    model = Event
    fields = ('title', 'guests', 'description',
              'start_date', 'end_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().order_by('-pk')
        context["event"] = self.model.objects.get(id=self.kwargs['pk'])

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            event = form.save(commit=False)
            event.category = Category.objects.get(
                name=request.GET.get("category"))
            event.host = request.user
            event.save()
            return JsonResponse({'status': 'success', 'msg': 'Event updated successfully', 'url': event.get_absolute_url()})
        return JsonResponse({'status': 'error', 'errors': form.errors})


# Delete
class EventDeleteView(generic.DeleteView):
    model = Event
    success_url = 'event-list'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)

# Tickets


@login_required(login_url='signin')
def get_ticket(request, pk, pke):
    guest = Guest.objects.get(user_id=pk, event__id=pke)
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.setPageSize((400, 570))

    # Add a background color
    p.setFillColorRGB(0.95, 0.95, 0.95)
    p.rect(0, 0, 400, 570, fill=True)

    # Add a border
    p.setLineWidth(2)
    p.rect(0, 0, 400, 570)

    # Add the title
    p.setFont("Times-Bold", 24)
    p.setFillColorRGB(0.1, 0, 1)
    p.drawString(140, 530, 'Event Ticket')

    # Add the ticket information
    p.setFont("Helvetica", 18)
    p.setFillColorRGB(0.4, 0.4, 0.4)
    p.drawString(
        40, 500, f'{guest.event.title[:30] if len(guest.event.title) > 30 else guest.event}...')

    p.setFont("Helvetica", 18)
    p.setFillColorRGB(10.6, 0.6, 0.6)
    p.drawString(40, 470, f"Guest : {guest.user.email}")

    p.setFont("Helvetica", 18)
    p.setFillColorRGB(0.8, 12.8, 0.8)
    p.drawString(40, 440, f'Date : {guest.event.start_date}')

    # Lets add qr_code image to pdf
    my_image = ImageReader(guest.qr_code)
    p.drawImage(my_image, x=25, y=60, width=350, height=350,
                preserveAspectRatio=True, mask='auto')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{guest.event}~{guest}.pdf')


#################################################
########### Category related views ##############
#################################################


class CategoryCreateView(generic.CreateView):
    model = Category
    fields = ('__all__')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})


#################################################
########### User related views #################
#################################################

class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "index_app/profile.html"


#################################################
########### Guest related views #################
#################################################
@login_required(login_url='login')
def add_guest(request, pk):
    event = Event.objects.get(id=pk)
    user = request.user
    try:
        guest = Guest.objects.create(user=user, event=event)
        guest.save()
        return redirect('event-detail', pk=pk)

    except:
        return redirect('event-detail', pk=pk,)


#################################################
########### Venue related views #################
#################################################

# Create


class VenueCreateView(generic.CreateView):
    model = Venue
    form_class = VenueForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locations"] = Location.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            response = super().form_valid(form)
            messages.success(request, "Venue created successfully.")
            return response
        else:
            messages.error(request, "There was an error creating the venue.")
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Venue created successfully.")
        return redirect('venue-detail', pk=self.object.pk)

    def get_success_url(self):
        return reverse_lazy('venue-detail', kwargs={'pk': self.object.pk})


# Update


class VenueUpdateView(generic.UpdateView):
    model = Venue


# List


class VenueListView(generic.ListView):
    model = Venue

# Detail


class VenueDetailView(generic.DetailView):
    model = Venue


#################################################
########### Venue related views #################
#################################################


class LocationCreateView(generic.CreateView):
    model = Location


class LocationListView(generic.ListView):
    model = Location
    paginate_by = 9


class LocationDetailView(generic.DetailView):
    model = Location


@login_required(login_url='login')
def post_event(request, pk):
    event = Event.objects.get(id=pk)
    event.draft = False
    event.save()
    return redirect('event-detail', pk=pk,)


@login_required(login_url='login')
def add_speaker(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        form = SpeakerForm(request.POST)
        if form.is_valid():
            form.instance.event = event
            form.save()
            return HttpResponseRedirect(event.get_absolute_url())
        else:
            return HttpResponseRedirect(event.get_absolute_url(),{'errors':form.errors})
