from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.utils.html import format_html

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post

from . import views


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
        views.move_event_to_post(self.model)

    approve_event.short_description = "Mark selected stories as approved"


class Events2PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'queue', 'post_date', 'status_color', 'date_from', open_url]
    list_filter = ['date_from', 'status']
    list_editable=['queue']
    search_fields = ['title', 'post']
    actions = ['change_queue', 'post_date_order_by_queue']
    admin.ModelAdmin.save_on_top = True

    def get_ordering(self, request):
        return ['queue']

    #Order by queue and change post_time in this order
    def post_date_order_by_queue(self,request,queryset):
        query_post_date_ordered = Events2Post.objects.exclude(status='Posted').order_by('post_date')
        query_post_date_ordered_list = [pd.post_date for pd in query_post_date_ordered]
        query_queue_ordered = Events2Post.objects.exclude(status='Posted').order_by('queue')
        for i, event in enumerate(query_queue_ordered):
            event.post_date = query_post_date_ordered_list[0]
            query_post_date_ordered_list.pop(0)
            event.save()

    post_date_order_by_queue.acts_on_all = True

    #Change queue of events by round (1->2, 2->3, 3->1)
    def change_queue(self,request,queryset):
        len_que = (len(queryset))
        for i in range(len_que):
            u = i + 1
            if i == (len_que-1): u = 0
            queryset.filter(event_id=queryset[i].event_id).update(queue=queryset[u].queue)
        self.post_date_order_by_queue(request,queryset)
    change_queue.short_description ='Change event place'

admin.site.register(EventsNotApprovedNew, EventsAdmin)
admin.site.register(EventsNotApprovedOld, EventsAdmin)
admin.site.register(Events2Post, Events2PostAdmin)