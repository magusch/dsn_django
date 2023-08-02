from django.contrib import admin
from .models import Place, PlaceKeyword, TestEventPlace

class PlaceAdmin(admin.ModelAdmin):
    list_display = [str,'place_name', 'place_url', 'url_to_address']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        PlaceKeyword.objects.create(place_id=obj.id, place_keyword=obj.place_name)


admin.site.register(Place, PlaceAdmin)
admin.site.register(PlaceKeyword)
admin.site.register(TestEventPlace)
