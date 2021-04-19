from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse  # TODO: delete
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post

from . import utils, models


@staff_member_required
def check_event_status(request):
    return HttpResponse("Pass")


@staff_member_required
def move_approved_events(request):
    utils.move_event_to_post(EventsNotApprovedNew)
    utils.move_event_to_post(EventsNotApprovedOld)
    return HttpResponse("Ok")


@staff_member_required
def remove_old_events(request):
    utils.delete_old_events(EventsNotApprovedNew)
    utils.delete_old_events(EventsNotApprovedOld)
    utils.delete_old_events(Events2Post)
    return HttpResponse("Ok")


@staff_member_required
def fill_empty_post_time(request):
    criterion1 = Q(post_date__lte=timezone.now())
    criterion2 = Q(post_date__isnull=True)
    queryset = (
        Events2Post.objects.exclude(status="Posted")
        .filter(criterion1 | criterion2)
        .order_by("queue")
        .all()
    )
    utils.refresh_posting_time(self=None, request=None, queryset=queryset)

    return HttpResponse("Ok")


@staff_member_required
def update_all(request):
    # move events to table Events2Post
    move_approved_events(request)

    # If post_time is empty fill it with logic
    fill_empty_post_time(request)

    # Sort by queue and put post_time in this order
    utils.post_date_order_by_queue()

    # Delete Old events from all tables
    remove_old_events(request)

    return HttpResponse("Ok")
