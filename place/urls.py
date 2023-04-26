from django.urls import path

from . import views


urlpatterns = [
    path("place_address/", views.place_address, name="place_address"),
]