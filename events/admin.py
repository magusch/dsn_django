from django.contrib import admin

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post


class EventsAdmin(admin.ModelAdmin):
    list_display = ["title", "approved", "date_from", "was_old"]
    list_filter = ["date_from"]
    search_fields = ["title", "post"]


class Events2PostAdmin(admin.ModelAdmin):
    list_display = ["title", "post_date", "status", "date_from", "url"]
    list_filter = ["date_from", "status"]
    search_fields = ["title", "post"]


admin.site.register(EventsNotApprovedNew, EventsAdmin)
admin.site.register(EventsNotApprovedOld, EventsAdmin)
admin.site.register(Events2Post, Events2PostAdmin)
