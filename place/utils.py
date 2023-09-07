from django.db.models import F, Value, CharField

from .models import PlaceKeyword, Place


def address_from_places(raw_address):
    places_by_keyword = PlaceKeyword.objects.annotate(querystring=Value(raw_address.lower(), output_field=CharField())) \
        .filter(querystring__icontains=F('place_keyword'))

    return places_by_keyword


def place_orm_object(place_id):
    return Place.objects.filter(id=place_id).first()
