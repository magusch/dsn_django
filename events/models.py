from django.db import models
from django.utils import timezone
from django.utils.html import format_html

import random


class EventsNotApprovedNew(models.Model):  # Table 1 for events from escraper
    event_id = models.CharField(max_length=30)
    approved = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=500)
    post = models.TextField(default="", blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    from_date = models.DateTimeField(
        "event date_from", default=(timezone.now() + timezone.timedelta(days=2))
    )
    to_date = models.DateTimeField(
        "event to_date",
        blank=True,
        default=(timezone.now() + timezone.timedelta(days=2)),
    )

    def __str__(self):
        return self.title

    def was_old(self):
        return self.explored_date <= timezone.now() - timezone.timedelta(days=2)

    def from_date_color(self):
        if (self.from_date - timezone.now()).days < 3:
            return format_html(
                f'<span style="color: Orange;">{self.from_date.ctime()}</span>'
            )
        else:
            return format_html(
                f'<span style="color: Green;">{self.from_date.ctime()}</span>'
            )


class EventsNotApprovedOld(models.Model):  # Table 2
    event_id = models.CharField(max_length=30)
    approved = models.BooleanField(default=False)
    title = models.CharField(max_length=500)
    post = models.TextField(default="", blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    from_date = models.DateTimeField(
        "event from_date", default=timezone.now() + timezone.timedelta(days=2)
    )
    to_date = models.DateTimeField(
        "event to_date",
        blank=True,
        default=(timezone.now() + timezone.timedelta(days=2)),
    )

    def __str__(self):
        return self.title

    def was_old(self):
        return self.to_date <= timezone.now()

    def from_date_color(self):
        if (self.from_date - timezone.now()).days < 2:
            return format_html(
                f'<span style="color: Orange;">{self.from_date.ctime()}</span>'
            )
        else:
            return format_html(
                f'<span style="color: Green;">{self.from_date.ctime()}</span>'
            )


status_color = {"ReadyToPost": "green", "Posted": "red", "ForFuture": 'blue', "Spam": "red", "Scrape": "purple"}


def last_queue():
    q = Events2Post.objects.order_by("-queue").first()
    if q:
        return q.queue + 2


monthes = ['января', 'февраля', "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
           "декабря"]


class Events2Post(models.Model):  # Table events for posting
    event_id = models.CharField(max_length=30, default=f"event{random.randint(1, 99)}_{timezone.now().date()}")
    queue = models.IntegerField(default=last_queue)
    title = models.CharField(max_length=500)

    default_events_date = timezone.now() + timezone.timedelta(days=3)

    month = monthes[default_events_date.month - 1]

    default_post_text = f"* {month}*  фестиваль *«ааааа»*\n\n\n\n*Где:*\n*Когда:*\n*Вход:*"
    post = models.TextField(default=default_post_text, blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=15,
        choices=(("ReadyToPost", "Ready To Post"), ("Posted", "Posted"), ("ForFuture", "For Future"),
                 ("Spam", "Spam"), ("Scrape", "Scrape It")),
        default="ReadyToPost",
    )
    price = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=500, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    post_date = models.DateTimeField("datetime for posting", blank=True, null=True)
    from_date = models.DateTimeField(
        "event from_date", default=default_events_date
    )
    to_date = models.DateTimeField(
        "event to_date", default=default_events_date
    )

    def __str__(self):
        return self.title

    def to_delete(self):
        return self.explored_date <= timezone.now() - timezone.timedelta(days=2)

    def status_color(self):
        return format_html(
            f'<span style="color: {status_color[self.status]};">{self.status}</span>'
        )

    def from_date_color(self):
        if self.status == 'ForFuture':
            return format_html(
                f'<span style="color: Blue;">{self.from_date.ctime()}</span>'
            )
        elif self.status == 'Posted' or self.status == 'Spam' or self.from_date < timezone.now():
            return format_html(
                f'<span style="color: Red;">{self.from_date.ctime()}</span>'
            )
        elif self.status == 'Scrape':
            return format_html(
                f'<span style="color: Purple;">{self.from_date.ctime()}</span>'
            )
        elif (self.from_date - timezone.now()).days < 3:
            return format_html(
                f'<span style="color: Orange;">{self.from_date.ctime()}</span>'
            )
        else:
            return format_html(
                f'<span style="color: Green;">{self.from_date.ctime()}</span>'
            )

    # Events2Post.objects.all().update(queue=F('queue')+1)


weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class PostingTime(models.Model):
    start_weekday = models.IntegerField(default=4)
    end_weekday = models.IntegerField(default=6)
    posting_time_hours = models.IntegerField(default=13)
    posting_time_minutes = models.IntegerField(default=20)

    def __str__(self):
        if (0 <= self.start_weekday < 7) & (0 <= self.end_weekday < 7):
            posting = (
                f"{weekdays[self.start_weekday]}-{weekdays[self.end_weekday]} "
                f"{self.posting_time_hours}:{self.posting_time_minutes:02}"
            )
            return posting
        return f"{self.posting_time_hours}:{self.posting_time_minutes}"


class Parameter(models.Model):  # Table events for posting
    site = models.CharField(max_length=500)
    parameter_name = models.CharField(max_length=500)
    value = models.CharField(max_length=500)
    commentary = models.CharField(max_length=500, null=True)
    def __str__(self):
        return (self.site + self.parameter_name)

# class Events(models.Model):
#     event_id = models.IntegerField()
#     title = models.CharField(max_length=250)
#     post = models.TextField(default='', blank=True)
#     price = models.CharField(max_length=150, blank=True)
#     address = models.CharField(max_length=200, blank=True)
#     from_date = models.DateTimeField('event from_date')
#     to_date = models.DateTimeField('event to_date')
#     pub_datetime = models.DateTimeField('published date and time', default=timezone.now)
#
#     def __str__(self):
#         return self.title
#
#     def was_published_recently(self):
#         return self.pub_datetime >= timezone.now() - datetime.timedelta(days=1)
