import json

import markdown

from django.utils import timezone
from django.http import HttpResponse  # TODO: delete
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template import loader

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post, Parameter, Event

from . import utils, models

from urllib.parse import urlparse

def event_post_html(request, event_id):
    event = get_object_or_404(Events2Post, pk=event_id)
    # image = f"<img src='{event.image}'>"
    # html = image + markdown.markdown(event.post)
    return HttpResponse(event.markdown_post_view_model())

def all_events(request):
    all_events = Events2Post.objects.filter(status="Posted")
    template = loader.get_template('index.html')
    context = {
        'all_events': all_events,
    }
    return HttpResponse(template.render(context, request))


def event_list(request):
    events = Event.objects.all()
    template = loader.get_template('events/event_list.html')
    context = {
        'events': events
    }
    return HttpResponse(template.render(context, request))


def event_full(request, id):
    event = get_object_or_404(Event, pk=id)
    template = loader.get_template('events/event_full.html')
    context = {
        'event': event
    }
    return HttpResponse(template.render(context, request))


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
    if 'HTTP_REFERER' in request.META:
        response = redirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponse('Ok')

    return response


@staff_member_required
def remove_old_events(request):
    utils.delete_old_events(EventsNotApprovedNew)
    utils.delete_old_events(EventsNotApprovedOld)
    utils.delete_old_events(Events2Post)
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
            Events2Post.objects.filter(status="ReadyToPost")
            .order_by("queue")
            .all()
        )

        utils.refresh_posting_time(None, request, queryset=queryset)

        if 'HTTP_REFERER' in request.META:
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

    if 'HTTP_REFERER' in request.META:
        response = redirect(request.META['HTTP_REFERER'])
    else:
        response = HttpResponse('Ok')

    return response


@csrf_exempt
@staff_member_required
def get_parameters(request):
    if request.method == "GET":
        prms = Parameter.objects

        if 'site' in request.GET:
            prms = prms.filter(site=request.GET['site'])

        if 'name' in request.GET:
            prms = prms.filter(parameter_name=request.GET['name'])

        params_in_db = []
        for row in prms.values():
            params_in_db.append(row)
        return HttpResponse(json.dumps(params_in_db))

# From post text to html
@staff_member_required
def markdown_to_html(request):
    html = ''
    if request.method == "POST":
        if 'text' in request.POST:
            html = markdown.markdown(request.POST['text'])
    if request.method == "GET":
        if 'text' in request.GET:
            html = markdown.markdown(request.GET['text'])
    return HttpResponse(html)