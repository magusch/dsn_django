from django.urls import path

from . import views

app_name = "events"
urlpatterns = [
    path("", views.index, name="index"),
    path("save/", views.save_event, name="save_event"),
    path("<int:event_id>/", views.detail, name="detail"),
]
