from django.urls import path
from . import views

urlpatterns = [
    # General routes
	path('',views.index,name='index'),
    path('dashboard/<int:pk>/', views.dashboard, name='dashboard'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    # Event urls
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/add/", views.EventCreateView.as_view(), name="add-event"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path("events/<int:pk>/update/", views.EventUpdateView.as_view(), name="update-event"),
    path("events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="delete-event"),
    path("events/<int:pk>/add-guest/",views.add_guest,name='add-guest'),

    # Category urls
    path("category/add/", views.CategoryCreateView.as_view(), name="add-category"),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user-profile'),
    

]
