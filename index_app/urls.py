from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/add/", views.EventCreateView.as_view(), name="add-event"),
]
