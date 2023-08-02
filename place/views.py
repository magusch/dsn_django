import json

# from django.shortcuts import render
# from django.contrib.admin.views.decorators import staff_member_required
# from django.shortcuts import redirect
from django.http import HttpResponse


from . import utils

#@staff_member_required
def place_address(request):
    raw_address = None
    if request.method == "GET":
        if 'address' in request.GET:
            raw_address = request.GET['address']
    elif request.method == "POST":
        raw_address = request.POST['address']

    address = {"raw_address": raw_address}

    if raw_address:
        place_by_keywords = utils.address_from_places(raw_address)
        if place_by_keywords:
            place = place_by_keywords[0]
            address.update({
                "response_code": 200,
                "address": place.place.place_name,
                "address_for_post": f"{place.place.markdown_address()}"
            })
        else:
            address.update({
                "response_code": 402,
                })
    else:
        address.update({
            "response_code": 400
        })

    return HttpResponse(json.dumps(address))