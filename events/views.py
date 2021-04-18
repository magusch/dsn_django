from django.utils import timezone
from django.db.models import Q

from django.http import HttpResponse  # TODO: delete

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post

from . import utils


# Move events to table Events2posts,
# It's not save
def save_event(request):
    utils.move_event_to_post(EventsNotApprovedNew)
    utils.move_event_to_post(EventsNotApprovedOld)
    return HttpResponse("Good!!!")


def delete_event(request):
    utils.delete_old_events(EventsNotApprovedNew)
    utils.delete_old_events(EventsNotApprovedOld)
    utils.delete_old_events(Events2Post)
    return HttpResponse("Good!!!")


def fill_empty_post_time():
    criterion1 = Q(post_date__lte=timezone.now())
    criterion2 = Q(post_date__isnull=True)
    queryset = (
        Events2Post.objects.exclude(status="Posted")
        .filter(criterion1 | criterion2)
        .order_by("queue")
        .all()
    )
    utils.refresh_posting_time(self=None, request=None, queryset=queryset)


def run_all(request):
    if request.method == "GET":
        # move events to table Events2Post
        save_event(request=None)

        # If post_time is empty fill it with logic
        fill_empty_post_time()

        # Sort by queue and put post_time in this order
        utils.post_date_order_by_queue()

        # Delete Old events from all tables
        delete_event(request)

        return HttpResponse("Good!!!")
    else:
        return HttpResponse("BAD!!!")
