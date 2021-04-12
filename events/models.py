from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class EventsNotApprovedNew(models.Model):  # Table 1 for events from escraper
    event_id = models.CharField(max_length=30)
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


class EventsNotApprovedOld(models.Model):  # Table 2
    event_id = models.CharField(max_length=30)
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


status_color={'ReadyToPost':'green', 'Posted':'red'}


class Events2Post(models.Model):  # Table events for posting
    event_id = models.CharField(max_length=30, default=f'event_{timezone.now().date()}')
    queue = models.IntegerField(default=10*timezone.now().weekday())
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
    post_date = models.DateTimeField("datetime for posting", blank=True, null=True)
    from_date = models.DateTimeField(
        "event from_date", default=(timezone.now() + timezone.timedelta(days=2))
    )
    to_date = models.DateTimeField(
        "event to_date", default=(timezone.now() + timezone.timedelta(days=2))
    )

    def __str__(self):
        return self.title

    def to_delete(self):
        return self.explored_date <= timezone.now() - timezone\
            .timedelta(days=2)

    def status_color(self):
        return format_html(f'<span style="color: {status_color[self.status]};">{self.status}</span>')

    #Events2Post.objects.all().update(queue=F('queue')+1)


weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class PostingTime(models.Model):
    start_weekday = models.IntegerField(default=4)
    end_weekday = models.IntegerField(default=6)
    posting_time_hours = models.IntegerField(default=13)
    posting_time_minutes = models.IntegerField(default=20)

    def __str__(self):
        if (0 <= self.start_weekday < 7) & (0 <= self.end_weekday < 7):
            posting = f"{weekdays[self.start_weekday]}-{weekdays[self.end_weekday]} " \
                      f"{self.posting_time_hours}:{self.posting_time_minutes:02}"
            return posting
        return f"{self.posting_time_hours}:{self.posting_time_minutes}"




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
