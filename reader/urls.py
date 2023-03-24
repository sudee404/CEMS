from django.urls import path
from . import views
urlpatterns = [
    path('reader/<int:pk>/',views.reader,name='reader'),
    path('reader/<int:pk>/guest/',views.validate_guest,name='validate-guest'),
    
]