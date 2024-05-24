from django import forms
from .models import EventsNotApprovedOld as EventsNotApprovedProposed

class EventAddForm(forms.ModelForm):
    class Meta:
        model = EventsNotApprovedProposed
        fields = ['title','full_text', 'place', 'price']