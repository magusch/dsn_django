from django import forms
from .models import EventsNotApprovedProposed

class EventAddForm(forms.ModelForm):
    class Meta:
        model = EventsNotApprovedProposed
        fields = ['title', 'full_text', 'address', 'from_date', 'to_date', 'place', 'price']