from django.urls import path

from . import views


urlpatterns = [
    path("place_address/", views.place_address, name="place_address"),
    path("find_place/", views.find_place, name="find_place"),
    path("place-autocomplete/", views.find_place, name="place-autocomplete"),
    path("all_places/", views.all_places, name="all_places"),
]