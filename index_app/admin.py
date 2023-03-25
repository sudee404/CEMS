from django.contrib import admin
from .models import Event, Category,Guest,Location,Venue,Speaker


class EventInline(admin.StackedInline):
    model = Event
    extra = 1
    

class SpeakerInline(admin.StackedInline):
    model = Speaker
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [EventInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'start_date', 'end_date')
    list_filter = ('start_date',)
    inlines = [SpeakerInline]
    

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')
    

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'country')
    

@admin.register(Venue)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name','role', 'event')