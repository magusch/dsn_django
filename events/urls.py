from django.urls import path

from . import views


urlpatterns = [
    path("move_approved_events/", views.move_approved_events, name="move_approved_events"),
    path("remove_old_events/", views.remove_old_events, name="remove_old_events"),
    path("update_all/", views.update_all, name="update_all"),
]
