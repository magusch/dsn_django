from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe


class PlaceAutocompleteWidget(forms.TextInput):
    def __init__(self, attrs=None):
        super(PlaceAutocompleteWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}
        attrs['class'] = 'place-autocomplete'
        html = super(PlaceAutocompleteWidget, self).render(name, value, attrs, renderer)
        return html + mark_safe('<div id="place-autocomplete-results" class="form-row"></div>')