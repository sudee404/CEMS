from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
    path("events/", views.EventListView.as_view(), name="event-list"),
    path("events/add/", views.EventCreateView.as_view(), name="add-event"),
    path("category/add/", views.CategoryCreateView.as_view(), name="add-category"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='user-profile'),
    path('dashboard/<int:pk>/',views.dashboard,name='dashboard'),
    path('gallery/',views.gallery,name='gallery'),
    path('contact/', views.contact, name='contact'),

]
