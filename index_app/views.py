from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView
from django.contrib.auth import get_user_model
from .models import Event


# Create your views here.

def index(request):
    context = {}
    context['upcoming'] = Event.objects.all()

    return render(request,'index.html',context)

def dashboard(request,pk):
    return render(request,'dashboard.html',{})

def gallery(request):
    return render(request,'gallery.html',{})

def contact(request):
    return render(request, 'contacts.html', {})


class EventCreateView(CreateView):
    model = Event
    fields = ('__all__')

class EventListView(ListView):
    model = Event


class EventDetailView(DetailView):
    model = Event




class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "index_app/profile.html"
