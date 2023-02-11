from django.contrib import admin
from .models import Event, Category


class EventInline(admin.StackedInline):
    model = Event
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [EventInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'start_date', 'end_date')
    list_filter = ('start_date',)
    
