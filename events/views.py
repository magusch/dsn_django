import datetime
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse #TODO: delete

from .models import EventsNotApprovedNew,EventsNotApprovedOld, Events2Post


def index(request):
    latest_event_list = Events2Post.objects.order_by('-date_from')[:5]
    context = {
        'latest_event_list': latest_event_list,
    }
    return render(request, 'events/index.html', context)


def detail(request, event_id):
    event = get_object_or_404(Events2Post, pk=event_id)
    return render(request, 'events/detail.html', {'event': event})

#take posting time for last event
def last_post_date():  # TODO: to make normal function for making new posting time
    last_post_event = Events2Post.objects.order_by('-post_date').first()
    return (last_post_event.post_date + datetime.timedelta(hours=2), last_post_event.queue+2)


#Move Events form not approved table to table with approved Events2Post
def move_event_to_post(Events_model): #ToDO: remove from here
    event2post_list = ['event_id', 'title', 'post', 'image', 'url', 'price', 'address', 'explored_date', 'date_from', 'date_to']

    events = Events_model.objects.filter(approved=True)

    post_date, queue = last_post_date()
    for event in events.values(*event2post_list):
        Events2Post.objects.create(status='ReadyToPost', post_date=post_date, queue=queue, **event)
    events.delete()


# Move events to table Events2posts,
# It's not save
def save_event(request):
    move_event_to_post(EventsNotApprovedNew)
    move_event_to_post(EventsNotApprovedOld)
    return HttpResponse("Good!!!")

