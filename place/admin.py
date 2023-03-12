from django.contrib import admin
from .models import Place, PlaceKeyword, TestEventPlace

class PlaceAdmin(admin.ModelAdmin):
    list_display = [str,'place_name', 'place_url', 'url_to_address']

admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceKeyword)
admin.site.register(TestEventPlace)
