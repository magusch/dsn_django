from django.urls import path

from . import views


urlpatterns = [
    path("check_event_status/", views.check_event_status, name="check_event_status"),
    path("move_approved_events/", views.move_approved_events, name="move_approved_events"),
    path("remove_old_events/", views.remove_old_events, name="remove_old_events"),
    path("fill_empty_post_time/", views.fill_empty_post_time, name="fill_empty_post_time"),
    path("update_all/", views.update_all, name="update_all"),
]
