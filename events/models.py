import re

from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import random

import markdown

from place.models import Place

from .helper.post_helper import PostHelper
from .helper.post_checker import PostChecker

class EventsNotApprovedNew(models.Model):  # Table 1 for events from escraper
    event_id = models.CharField(max_length=30)
    approved = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=500)
    post = models.TextField(default="", blank=True)
    full_text = models.TextField(default="", blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    explored_date = models.DateTimeField(
        "published date and time",
    )
    from_date = models.DateTimeField(
        "event date_from",
    )
    to_date = models.DateTimeField(
        "event to_date",
        blank=True,
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
    full_text = models.TextField(default="", blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    explored_date = models.DateTimeField(
        "published date and time",
    )
    from_date = models.DateTimeField(
        "event from_date",
    )
    to_date = models.DateTimeField(
        "event to_date",
        blank=True,
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


def random_event_id():
    return f"event{random.randint(1, 99)}_{timezone.now().date()}"


def default_event_date():
    return timezone.now() + timezone.timedelta(days=3)


class Events2Post(models.Model):  # Table events for posting
    event_id = models.CharField(max_length=30, default=random_event_id)
    queue = models.IntegerField(default=last_queue)
    title = models.CharField(max_length=500)

    month = monthes[default_event_date().month - 1]

    default_post_text = f"* {month}*  фестиваль *«ааааа»*\n\n\n\n*Где:*\n*Когда:*\n*Вход:*"
    post = models.TextField(default=default_post_text, blank=True)
    full_text = models.TextField(default="", blank=True, null=True)
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

    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    explored_date = models.DateTimeField(
        "published date and time", default=timezone.now
    )
    post_date = models.DateTimeField("datetime for posting", blank=True, null=True)
    from_date = models.DateTimeField(
        "event from_date", default=default_event_date
    )
    to_date = models.DateTimeField(
        "event to_date", default=default_event_date
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

    def markdown_post_view_model(self):
        html_image = f"<div id='markdown_post' style='width:325px;'><img src='{self.image}' width='325px'>"
        html_post = markdown.markdown(self.post
                                      .replace('*','**')
                                      .replace("\n", "<br>")
                                      .replace('_','*')
                                      )
        return format_html(html_image+html_post + '</div>')

    def address_markdown(self):
        return self.place.markdown_address()

    def remake_post(self, save=False):
        remaked_post = PostHelper(self).post_markdown()
        self.post = remaked_post
        if save: 
            self.save()
        return remaked_post

    def post_check(self):
        result_checker = PostChecker(self.post).result

        result_brief = ''
        for key in result_checker.keys():
            result_brief += key
        return result_brief


    def clean(self):
        error_message = ''
        # post size validation
        maximum_characters = 2000

        if len(self.post) > maximum_characters:
            error_message += f"Post text is too biig. It has {len(self.post)} characters " \
                             f"but it should have a maximum of {maximum_characters}"

        if error_message != '':
            raise ValidationError(_(error_message))


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


class Event(models.Model):
    event_id = models.CharField(max_length=30, default=random_event_id)
    title = models.CharField(max_length=500)
    post = models.TextField(default="", blank=True)
    full_text = models.TextField(default="", blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True)
    price = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    #category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    pub_datetime = models.DateTimeField('published date and time', default=timezone.now)
    from_date = models.DateTimeField("event from_date", default=default_event_date)
    to_date = models.DateTimeField("event to_date", default=default_event_date)

    def __str__(self):
        return self.title

