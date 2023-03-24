from django import forms
from .models import Venue


class VenueForm(forms.ModelForm):
    """Form definition for Venue."""

    class Meta:
        """Meta definition for Venueform."""

        model = Venue
        fields = ('__all__')

        widgets = {
            'location': forms.Select(attrs={'class': 'form-control form-select bg-light bg-gradient'})
        }
