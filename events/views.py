import json

from django.utils import timezone
from django.http import HttpResponse  # TODO: delete
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post

from . import utils, models

from urllib.parse import urlparse


@staff_member_required
def check_event_status(request):
    return HttpResponse("Pass")

@staff_member_required
def count_events_by_day(request):
    answer = json.dumps(utils.count_events_by_day())
    return HttpResponse(answer)

@staff_member_required
def move_approved_events(request):
    utils.move_event_to_post(EventsNotApprovedNew)
    utils.move_event_to_post(EventsNotApprovedOld)
    if 'REMOTE_HOST' not in request.META or 'HTTP_REFERER' not in request.META:
        response = HttpResponse('Ok')
    elif 'HTTP_REFERER' in request.META:
        response = redirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponse('Ok')

    return response


@staff_member_required
def remove_old_events(request):
    utils.delete_old_events(EventsNotApprovedNew)
    utils.delete_old_events(EventsNotApprovedOld)
    utils.delete_old_events(Events2Post)
    print(request.META)
    if 'HTTP_REFERER' in request.META:
        response = redirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponse('Ok')
    return response


@csrf_exempt
@staff_member_required
def fill_empty_post_time(request):
    if request.method == "POST":
        print("")
        response = None
        #utils.refresh_posting_time(request=request)

    elif request.method == "GET":
        queryset = (
            Events2Post.objects.exclude(status="Posted")
            .order_by("queue")
            .all()
        )

        utils.refresh_posting_time(None, request, queryset=queryset)
        #response = HttpResponse("Ok")
        if 'REMOTE_HOST' not in request.META or 'HTTP_REFERER' not in request.META:
            response = HttpResponse('Ok')
        elif 'HTTP_REFERER' in request.META:
            response = redirect(request.META['HTTP_REFERER'])
        else:
            response = HttpResponse('Ok')

    return response


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

    if 'REMOTE_HOST' not in request.META or 'HTTP_REFERER' not in request.META:
        response = HttpResponse('Ok')
    elif 'HTTP_REFERER' in request.META:
        response = redirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponse('Ok')

    return response