from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'events', views.EventViewSet)

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
    path("transfer_posted_events_to_site/", views.transfer_posted_events_to_site, name="transfer_posted_events_to_site"),

    path("", views.event_list, name="event_list"),
    path("<int:id>", views.event_full, name="event_full"),

    path("remake_post/<int:id>", views.remake_post, name="remake_post"),
    path("remake_post/", views.remake_post, name="remake_post_empty"),

    #REST API
    path("api/", include(router.urls)),

]