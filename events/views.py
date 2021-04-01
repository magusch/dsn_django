from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse #TODO: delete

from .models import EventsNotApprovedNew, EventsNotApprovedOld, Events2Post, PostingTime

current_tz = timezone.get_current_timezone()
current_tz_int = timezone.get_default_timezone().normalize(timezone.now()).hour - timezone.now().hour

def index(request):
    latest_event_list = Events2Post.objects.order_by('-date_from')[:5]
    context = {
        'latest_event_list': latest_event_list,
    }
    return render(request, 'events/index.html', context)


def detail(request, event_id):
    event = get_object_or_404(Events2Post, pk=event_id)
    return render(request, 'events/detail.html', {'event': event})


def good_post_time(last_post_time):
    if last_post_time <= timezone.now():
        last_post_time = timezone.now()
    post_time_query_first = PostingTime.objects.filter(start_weekday__lte=last_post_time.weekday())\
        .filter(end_weekday__gte=last_post_time.weekday())\
        .filter(posting_time_hours__gte=last_post_time.hour+current_tz_int+1).first()
    if post_time_query_first:
        post_time = last_post_time.replace(hour=post_time_query_first.posting_time_hours-current_tz_int,
                                           minute=post_time_query_first.posting_time_minutes)
    else:
        next_day = last_post_time + timezone.timedelta(days=1)
        post_time = PostingTime.objects.filter(start_weekday__lte=next_day.weekday()).filter(
            end_weekday__gte=next_day.weekday()).order_by('posting_time_hours').first()
        post_time = next_day.replace(hour=post_time.posting_time_hours-current_tz_int, minute=post_time.posting_time_minutes)
    return post_time


# take posting time for last event
def last_post_date():
    last_post_event = Events2Post.objects.order_by('-post_date').first()
    if last_post_event:
        last_queue = Events2Post.objects.order_by('-queue').first().queue
        try:
            post_time = good_post_time(current_tz.normalize(last_post_event.post_date))
        except:
            post_time = last_post_event.post_date + timezone.timedelta(hours=2)
        return post_time, last_queue + 2

    post_time = empty_queryset()
    return post_time, 1


def empty_queryset():
    today = timezone.now() + timezone.timedelta(days=1)
    post_time = PostingTime.objects.filter(start_weekday__lte=today.weekday()).filter(end_weekday__gte=today.weekday()) \
        .order_by('posting_time_hours').first()
    post_time = today.replace(hour=post_time.posting_time_hours, minute=post_time.posting_time_minutes)
    return post_time


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


def delete_old_events(Events_model):
    today = timezone.now()
    Events_model.objects.filter(date_to__lt=today).delete()


def delete_event(request):
    delete_old_events(EventsNotApprovedNew)
    delete_old_events(EventsNotApprovedOld)
    delete_old_events(Events2Post)
    return HttpResponse("Good!!!")