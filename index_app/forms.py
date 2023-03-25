from django import forms
from .models import Venue,Speaker


class VenueForm(forms.ModelForm):
    """Form definition for Venue."""

    class Meta:
        """Meta definition for Venueform."""

        model = Venue
        fields = ('__all__')

        widgets = {
            'location': forms.Select(attrs={'class': 'form-control form-select bg-light bg-gradient'})
        }

class SpeakerForm(forms.ModelForm):
    """Form definition for Speaker."""

    class Meta:
        """Meta definition for Speakerform."""

        model = Speaker
        fields = ('__all__')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-select bg-light bg-gradient'}),
            'role': forms.TextInput(attrs={'class': 'form-control form-select bg-light bg-gradient'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control form-select bg-light bg-gradient'})
        }
