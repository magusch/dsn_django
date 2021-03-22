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
    list_display = ['title', 'queue', 'post_date', 'status_color', 'date_from', open_url]
    list_filter = ['date_from', 'status']
    search_fields = ['title', 'post']
    actions = ['change_queue']
    admin.ModelAdmin.save_on_top=True

    def get_ordering(self, request):
        return ['queue', 'post_date']

    def change_queue(self,request,queryset):
        len_que = (len(queryset))
        for i in range(len_que):
            u = i + 1
            if i == (len_que-1): u = 0
            queryset.filter(event_id=queryset[i].event_id).update(queue=queryset[u].queue)
    change_queue.short_description ='Change event place'

    #def refresh(self,request):


admin.site.register(EventsNotApprovedNew, EventsAdmin)
admin.site.register(EventsNotApprovedOld, EventsAdmin)
admin.site.register(Events2Post, Events2PostAdmin)