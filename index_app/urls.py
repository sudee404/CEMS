from django.urls import path
from . import views

urlpatterns = [
    # General routes
	path('',views.index,name='index'),
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    # Event urls
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/add/", views.EventCreateView.as_view(), name="add-event"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("events/<int:pk>/post/", views.post_event, name="post-event"),
    path("events/<int:pk>/update/", views.EventUpdateView.as_view(), name="update-event"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="delete-event"),
    path("events/<int:pk>/add-guest/",views.add_guest,name='add-guest'),
    path("events/<int:pk>/ticket/<int:pke>/",views.get_ticket, name='get-ticket'),
    # Category urls
    path("category/add/", views.CategoryCreateView.as_view(), name="add-category"),
    path('profile/', views.profile, name='user-profile'),
    # Location urls
    path('locations/',views.LocationListView.as_view(),name='location-list'),
    path('locations/<int:pk>/',views.LocationDetailView.as_view(),name='location-detail'),
    # Location urls
    path('venues/add/', views.VenueCreateView.as_view(), name='add-venue'),
    path('venues/<int:pk>/update/', views.VenueUpdateView.as_view(), name='add-venue'),
    path('venues/<int:pk>/', views.VenueDetailView.as_view(),
         name='venue-detail'),   
    path('add-speaker/<int:pk>/',views.add_speaker,name='add-speaker'), 
    path('generate-report/<int:pk>/',views.generate_report,name='report'),

]
