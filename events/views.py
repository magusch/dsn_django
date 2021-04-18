from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from django.http import HttpResponse  # TODO: delete

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post, PostingTime

from . import utils

current_tz = timezone.get_current_timezone()
current_tz_int = (
    timezone.get_default_timezone().normalize(timezone.now()).hour - timezone.now().hour
)


def index(request):
    latest_event_list = Events2Post.objects.order_by("-from_date")[:5]
    context = {
        "latest_event_list": latest_event_list,
    }
    return render(request, "events/index.html", context)


def detail(request, event_id):
    event = get_object_or_404(Events2Post, pk=event_id)
    return render(request, "events/detail.html", {"event": event})


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
        utils.move_event_to_post(EventsNotApprovedNew)
        utils.move_event_to_post(EventsNotApprovedOld)

        # If post_time is empty fill it with logic
        fill_empty_post_time()

        # Sort by queue and put post_time in this order
        utils.post_date_order_by_queue()

        # Delete Old events from all tables
        utils.delete_old_events(EventsNotApprovedNew)
        utils.delete_old_events(EventsNotApprovedOld)
        utils.delete_old_events(Events2Post)

        return HttpResponse("Good!!!")
    else:
        return HttpResponse("BAD!!!")
