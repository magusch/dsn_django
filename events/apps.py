from django.apps import AppConfig


class EventsConfig(AppConfig):
    name = "events"


def move_event_to_post():
    event2post_list = [
        "event_id",
        "title",
        "post",
        "image",
        "url" "price",
        "address",
        "explored_date",
        "date_from",
        "date_to",
    ]
    from events.models import EventsNotApprovedNew, Events2Post

    events = EventsNotApprovedNew.objects.filter(approved=True).values(*event2post_list)

    for event in events:
        Events2Post.objects.create(
            status="ReadyToPost", post_date=event["date_from"], **event
        )
    events.delete()
