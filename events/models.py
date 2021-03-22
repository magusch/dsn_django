import datetime

from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class EventsNotApprovedNew(models.Model):  # Table 1 for events from escraper
    event_id = models.IntegerField()
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=250)
    post = models.TextField(default="", blank=True)
    image = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True)
    price = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=200, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    date_from = models.DateTimeField(
        "event date_from", default=(timezone.now() + datetime.timedelta(days=2))
    )
    date_to = models.DateTimeField(
        "event date_to",
        blank=True,
        default=(timezone.now() + datetime.timedelta(days=2)),
    )

    def __str__(self):
        return self.title

    def was_old(self):
        return self.explored_date <= timezone.now() - datetime.timedelta(days=2)


class EventsNotApprovedOld(models.Model):  # Table 2
    event_id = models.IntegerField()
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=250)
    post = models.TextField(default="", blank=True)
    image = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True)
    price = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=200, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    date_from = models.DateTimeField(
        "event date_from", default=timezone.now() + datetime.timedelta(days=2)
    )
    date_to = models.DateTimeField(
        "event date_to",
        blank=True,
        default=(timezone.now() + datetime.timedelta(days=2)),
    )

    def __str__(self):
        return self.title

    def was_old(self):
        return self.date_to <= timezone.now()

def last_post_date(self):  # TODO: to make normal function for making new posting time
        last_post_event = self.objects.order_by('-post_date').first()
        return (last_post_event.post_date + datetime.timedelta(hours=2))

status_color={'ReadyToPost':'green', 'Posted':'red'}

class Events2Post(models.Model):  # Table events for posting
    event_id = models.IntegerField()
    queue = models.IntegerField(default=1)
    title = models.CharField(max_length=250)
    post = models.TextField(default="", blank=True)
    image = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True)
    status = models.CharField(
        max_length=15,
        choices=(("ReadyToPost", "Ready To Post"), ("Posted", "Posted")),
        default="ReadyToPost",
    )
    price = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=200, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    post_date = models.DateTimeField("datetime for posting", blank=True)
    date_from = models.DateTimeField(
        "event date_from", default=(timezone.now() + datetime.timedelta(days=2))
    )
    date_to = models.DateTimeField(
        "event date_to", default=(timezone.now() + datetime.timedelta(days=2))
    )

    def __str__(self):
        return self.title

    def to_delete(self):
        return self.explored_date <= timezone.now() - datetime.timedelta(days=2)

    def status_color(self):
        return format_html(f'<span style="color: {status_color[self.status]};">{self.status}</span>')








# class ChannelEvents(models.Model):
#     post_id = models.IntegerField()
#     title = models.CharField(max_length=250)
#     date_from = models.DateTimeField('event date_from')
#     price = models.CharField(max_length=150)
#
#     def __str__(self):
#         return self.title
#
#
# class Events(models.Model):
#     event_id = models.IntegerField()
#     title = models.CharField(max_length=250)
#     post = models.TextField(default='', blank=True)
#     price = models.CharField(max_length=150, blank=True)
#     address = models.CharField(max_length=200, blank=True)
#     date_from = models.DateTimeField('event date_from')
#     date_to = models.DateTimeField('event date_to')
#     pub_datetime = models.DateTimeField('published date and time', default=timezone.now)
#
#     def __str__(self):
#         return self.title
#
#     def was_published_recently(self):
#         return self.pub_datetime >= timezone.now() - datetime.timedelta(days=1)
