from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.utils.html import format_html

import markdown

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post, PostingTime, Parameter, Event


from . import utils

from .helper.post_helper import PostHelper


def open_url(obj):
    return format_html("<a href='%s' target='_blank'>%s</a>" % (obj.url, obj.url))


open_url.short_description = "URL"


class EventsAdmin(admin.ModelAdmin):
    change_list_template = "events/change_list_not_approved.html"

    list_display = ["title", "approved", "from_date_color", open_url, "was_old"]
    list_filter = ["from_date", "explored_date"]
    search_fields = ["title", "post"]
    actions = ["approve_event"]
    ordering = ["-explored_date", "-from_date"]

    def approve_event(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully approved.",
                "%d events were successfully approved.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
        utils.move_event_to_post(self.model)

    approve_event.short_description = "Mark selected stories as approved"


class Events2PostAdmin(admin.ModelAdmin):
    change_list_template = "events/change_list_approved.html"
    change_form_template = "events/change_form.html"
    list_display = [
        "title",
        "queue",
        "post_date",
        "from_date_color",
        open_url,
        "status_color",
    ]
    #exclude = ["full_text"]
    list_filter = ["status"]
    list_editable = ["queue", "post_date"]
    search_fields = ["title", "post"]
    actions = [
        "change_status_to_ReadyToPost",
        "change_status_to_Spam",
        "clear_post_time",
        "change_queue",
        'update_post_text_for_posting',
        'transfer_events_to_site',
        utils.post_date_order_by_queue,
        utils.refresh_posting_time,
    ]
    admin.ModelAdmin.save_on_top = True
    admin.ModelAdmin.actions_on_bottom = True
    admin.ModelAdmin.actions_selection_counter = True
    admin.ModelAdmin.actions_selection_counter = True
    readonly_fields = ("markdown_post_view_model",)
    include = ( "markdown_post_view_model")

    class Media:
        js = ("js/post_to_markdown.js"
            ,'admin/js/post_to_markdown.js',
              "post_to_markdown.js")

    def markdown_post_view(self, instance):
        html_image = f"<div style='width:325px;'><img src='{instance.image}' width='325px'>"
        html_post = markdown.markdown(instance.post
                                      .replace('*','**')
                                      .replace("\n", "<br>")
                                      .replace('_','*')
                                      )
        return format_html(html_image+html_post + '</div>')

    def get_ordering(self, request):
        return ["status", "queue"]


    def change_status_to_ReadyToPost(self, request, queryset):
        updated = queryset.update(status="ReadyToPost")
        self.message_user(
            request,
            ngettext(
                "%d event was changed on ReadyToPost.",
                "%d events were changed on ReadyToPost.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def change_status_to_Spam(self, request, queryset):
        updated = queryset.update(status="Spam")
        self.message_user(
            request,
            ngettext(
                "%d event was changed on Posted.",
                "%d events were changed on Posted.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    utils.post_date_order_by_queue.acts_on_all = True

    # empty post_time
    def clear_post_time(self, request, queryset):
        queryset.update(post_date=None)

    # Change queue of events by round (1->2, 2->3, 3->1)
    def change_queue(self, request, queryset):
        len_que = len(queryset)
        for i in range(len_que):
            u = i + 1
            if i == (len_que - 1):
                u = 0
            queryset.filter(event_id=queryset[i].event_id).update(
                queue=queryset[u].queue
            )
        utils.post_date_order_by_queue(self, request, queryset)

    change_queue.short_description = "Change event place"

    def update_post_text_for_posting(self, request, queryset):
        events = queryset.all()

        for event in events:
            event.remake_post(save=True)


    def transfer_events_to_site(self, request, queryset):
        updated = utils.move_event_to_site(self.model)
        self.message_user(
            request,
            ngettext(
                "%d event was successfully transfered to site version.",
                "%d events were successfully transfered to site version.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )




weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class PostingTimesAdmin(admin.ModelAdmin):

    list_filter = ["start_weekday"]
    ordering = ["start_weekday", "posting_time_hours"]
    list_editable = ["posting_time_hours", "posting_time_minutes"]

    def weekdays(self):
        if (0 <= self.start_weekday < 7) & (0 <= self.end_weekday < 7):
            return f"{weekdays[self.start_weekday]}-{weekdays[self.end_weekday]}"
        if self.start_weekday < 0:  # we can add special postingtime for special date
            return f"day – {self.start_weekday*-1}"

    def timepost(self):
        return f"{self.posting_time_hours}:{self.posting_time_minutes:02}"

    list_display = [weekdays, timepost, "posting_time_hours", "posting_time_minutes"]


class ParametersAdmin(admin.ModelAdmin):
    list_display = ['site', 'parameter_name', 'value', 'commentary']
    list_editable = ['value', 'commentary']
    actions = ["copy",]

    def copy(self, request, queryset):
        for object in queryset:
            object.id = None
            object.save()
    copy.short_description = "Duplicate selected record"


admin.site.register(EventsNotApprovedNew, EventsAdmin)
admin.site.register(EventsNotApprovedOld, EventsAdmin)
admin.site.register(PostingTime, PostingTimesAdmin)
admin.site.register(Events2Post, Events2PostAdmin)
admin.site.register(Parameter, ParametersAdmin)
admin.site.register(Event)
