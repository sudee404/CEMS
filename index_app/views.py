from django.shortcuts import render
from django.views.generic import ListView,CreateView
from .models import Event
# Create your views here.

def index(request):
    return render(request,'index.html',{})


class EventListView(ListView):
    model = Event


class EventCreateView(CreateView):
    model = Event
    fields = ('__all__')
