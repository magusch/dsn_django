from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.utils.html import format_html

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post


def open_url(obj):
    return format_html("<a href='%s'>%s</a>" % (obj.url, obj.url))
open_url.short_description = 'Url'


class EventsAdmin(admin.ModelAdmin):
    list_display = ['title', 'approved', 'date_from', open_url,  'was_old']
    list_filter = ['date_from']
    search_fields = ['title', 'post']
    actions = ['approve_event']

    def approve_event(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, ngettext(
            '%d event was successfully approved.',
            '%d events were successfully approved.',
            updated,
        ) % updated, messages.SUCCESS)

    approve_event.short_description = "Mark selected stories as approved"


class Events2PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_date', 'status', 'date_from', open_url]
    list_filter = ['date_from', 'status']
    search_fields = ['title', 'post']


admin.site.register(EventsNotApprovedNew, EventsAdmin)
admin.site.register(EventsNotApprovedOld, EventsAdmin)
admin.site.register(Events2Post, Events2PostAdmin)