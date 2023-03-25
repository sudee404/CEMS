from django.conf import settings
from django.db import IntegrityError
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.pdfdoc import PDFInfo
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import FileResponse, JsonResponse, HttpResponse
from index_app.forms import SpeakerForm, VenueForm
from .models import Event, Category, Guest, Venue, Location
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os

User = get_user_model()
script_dir = os.path.dirname(os.path.abspath(__file__))
media_root = settings.MEDIA_ROOT


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
        events = Event.objects.filter(draft=False,
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


@login_required
def profile(request):
    context = {}
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            user = User.objects.get(id=request.user.id)
            if query == 'image':
                # Update user's profile image
                image_file = request.FILES.get('profile')
                user.avatar = image_file
                user.save()
                return redirect('user-profile')
            elif query == 'details':
                # Update user's other details
                username = request.POST.get('username')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return redirect('user-profile')
        except Exception as e:
            print(e)
            context['error'] = e
    
    return render(request, 'index_app/profile.html', context)


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


# Detail
class VenueDetailView(generic.DetailView):
    model = Venue


#################################################
########### Venue related views #################
#################################################


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
        form = SpeakerForm(request.POST, request.FILES)
        form.instance.event = event

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect': event.get_absolute_url()})
        else:
            errors = {'errors': form.errors}
            return JsonResponse(errors, status=400)

    # Handle GET requests
    return HttpResponseRedirect(reverse('event-detail', args=(pk,)))


def generate_report(request, pk):

    event = Event.objects.get(id=pk)
    return generate_report_file(event)


def generate_report_file(event):
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Set up the document
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    doc.title = 'Event Report'

    # Define a centered heading style
    centered_heading1 = ParagraphStyle('Centered', alignment=TA_CENTER)
    centered_heading1.fontName = 'Helvetica-Bold'
    centered_heading1.fontSize = 20
    centered_heading1.leading = 20
    centered_heading1.underline = 1

    # Define a centered heading2 style
    centered_heading2 = ParagraphStyle('Centered H2', alignment=TA_CENTER)
    centered_heading2.fontName = 'Helvetica-Bold'
    centered_heading2.textColor = 'blue'
    centered_heading2.fontSize = 16
    centered_heading2.leading = 20

    # Define a centered heading3 style
    centered_heading3 = ParagraphStyle('H#', alignment=TA_LEFT)
    centered_heading3.fontName = 'Helvetica-Bold'
    centered_heading3.textColor = 'black'
    centered_heading3.fontSize = 16
    centered_heading3.leading = 20

    # Define a  heading2 style
    heading2 = ParagraphStyle('H2', alignment=TA_LEFT)
    heading2.fontName = 'Helvetica-Bold'
    heading2.textColor = 'red'
    heading2.fontSize = 16
    heading2.leading = 20

    # Define a event description style
    desc_style = ParagraphStyle('Description', alignment=TA_LEFT)
    desc_style.fontName = 'Helvetica'
    desc_style.fontSize = 14
    desc_style.leading = 20

    # Create the table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Create table data
    # Speakers
    speaker_data = [['Name', 'Role']]
    for speaker in event.speaker_set.all():
        speaker_data.append([speaker.name, speaker.role])

    # Guests
    guest_data = [['Username', 'Email', 'Attended']]
    for guest in event.guest_set.all():
        user = guest.user
        guest_data.append([user.username, user.email, guest.scanned])

    # Add the tables to the document and save it
    # Speakers
    speaker_table = Table(speaker_data, colWidths=[
                          2*inch, 3*inch, 1.5*inch, 1.5*inch])
    speaker_table.setStyle(table_style)

    # Guests
    guest_table = Table(guest_data, colWidths=[
                        2*inch, 3*inch, 1.5*inch, 1.5*inch])
    guest_table.setStyle(table_style)

    # Load logo and event poster
    logo_reader = os.path.join(media_root, 'default.png')
    poster_reader = event.poster

    # Add elements to the page
    elements = []

    # Title
    elements.append(Paragraph("Event Report", centered_heading1))
    elements.append(Spacer(1, 0.5*inch))

    elements.append(Paragraph(f'Title : {event.title}', centered_heading2))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f'Venue : {event.venue}', centered_heading2))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(
        Paragraph(f"Start Date : {event.start_date}", centered_heading2))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(
        Paragraph(f"End Date : {event.end_date}", centered_heading2))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(
        Paragraph(f"Host Name: {event.host.get_full_name()}", centered_heading3))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(
        Paragraph(f"Host Email: {event.host.email}", centered_heading3))
    elements.append(Spacer(1, 0.3*inch))

    # Description
    if event.description:
        elements.append(Paragraph("Event Description", heading2))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(event.description, desc_style))
        elements.append(Spacer(1, 0.5*inch))

    # Add event poster
    # Add a page break to move to the second page
    elements.append(PageBreak())
    elements.append(Paragraph('Event poster', centered_heading1))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Image(poster_reader, width=500, height=300))

    if event.speaker_set.all:
        # Speakers Table
        elements.append(PageBreak())
        elements.append(Paragraph("Event Speakers", heading2))
        elements.append(Paragraph(
            'Event was graced with the presence of the following speakers', desc_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(speaker_table)
        elements.append(Spacer(1, 0.5*inch))

    if event.guest_set.all:
        # Guest Table
        elements.append(PageBreak())
        elements.append(Paragraph("Event Guests", heading2))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(
            'Event was attended by the following', desc_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(guest_table)
        elements.append(Spacer(1, 0.5*inch))

    # Build document
    doc.build(elements)

    # Seek to the beginning and return the buffer as the PDF file
    buffer.seek(0)

    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="event_report.pdf"'

    return response
