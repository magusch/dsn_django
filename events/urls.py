from django.urls import path

from . import views


urlpatterns = [
    path("save/", views.save_event, name="save_event"),
    path("delete/", views.delete_event, name="delete_event"),
    path("run/", views.run_all, name="run"),
]
