from django.shortcuts import render
from index_app.models import Event, Guest
# Create your views here.


def reader(request, pk):
    event = Event.objects.get(pk=pk)

    context = {
        'event': event,
    }
    return render(request, 'reader.html', context=context)


def validate_guest(request, pk):
    code = request.GET.get('text')
    event = Event.objects.get(pk=pk)
    exists = Guest.objects.filter(ticket__iexact=code, event_id=pk).exists()
    scanned = False
    if exists:
        guest = Guest.objects.get(ticket__iexact=code, event_id=pk)
        if guest.scanned:
            scanned = True
        else:
            guest.scanned = True
            guest.save()

    context = {
        'event': event,
        'exists': exists,
        'validate': True,
        'scanned': scanned,
    }
    return render(request, 'reader.html', context=context)

