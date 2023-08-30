from django.urls import path

from . import views


urlpatterns = [
    path("check_event_status/", views.check_event_status, name="check_event_status"),
    path("count_events_by_day/", views.count_events_by_day, name="count_events_by_day"),
    path("move_approved_events/", views.move_approved_events, name="move_approved_events"),
    path("remove_old_events/", views.remove_old_events, name="remove_old_events"),
    path("fill_empty_post_time/", views.fill_empty_post_time, name="fill_empty_post_time"),
    path("update_all/", views.update_all, name="update_all"),
    path("parameters_for_channel/", views.get_parameters, name="parameters_for_channel"),
    #path("<int:event_id>", views.event_post_html, name="event_post_html"),
    path("markdown_to_html/", views.markdown_to_html, name="markdown_to_html"),
    path("markdown_all_events/", views.all_events, name="all_events"),

    path("", views.event_list, name="event_list"),
    path("<int:id>", views.event_full, name="event_full"),
]