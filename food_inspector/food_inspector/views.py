import requests
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse
from food_inspector.restaurant_finder import find_restaurant_in_db
from food_inspector.models import Restaurant
from django.template import RequestContext


def home(request):
    return render_to_response('home.html', {},
                              context_instance=RequestContext(request))


def locate_restaurant(request):
    name_input = request.POST.get("restaurantName")

    restaurants_found = find_restaurant_in_db(name_input)
    restaurants = []
    for restaurant in restaurants_found:
        address = restaurant["address"].title() + " " + \
            restaurant["city"].title() + ", " + \
            restaurant["zip_code"]
        restaurants.append(
            {"id": restaurant["id"],
             "name": restaurant["name"].lower().title(),
             "address": address})
    print("RESTAURANTS: ")
    print(restaurants)
    return render_to_response('choose_restaurant.html',
                              {"restaurants": restaurants})


def retrieve_inspection_report(request, restaurant_id):

    try:
        restaurant = Restaurant.objects.get(
            id=restaurant_id
        )
    except:
        return HttpResponse("There was an error trying to find restaurant")

    print("SEARCHING " + restaurant.name)
    payload = {'dba_name': restaurant.name}
    r = requests.get("https://data.cityofchicago.org/resource/4ijn-s7e5.json",
                     params=payload)

    if r.status_code != 200:
        print("STATUS CODE: " + r.status)
        return HttpResponse("Failed to retrieve this restaurant")

    print(r.text)
    inspection_reports = json.loads(r.text)
    if len(inspection_reports) == 0:
        return HttpResponse("Unable to find any inspection reports")

    most_recent_report = inspection_reports[0]
    print("MOST RECENT")
    print(most_recent_report)
    data = {"restaurant": {"name": restaurant.name,
            "address": restaurant.address}}
    if "violations" in most_recent_report:
        violations = most_recent_report["violations"].split('|')
    else:
        violations = []
    # print(violations)
    inspection = most_recent_report
    # print(inspection)
    inspection["violations"] = violations
    data["inspection"] = inspection
    print(r.text)
    return render_to_response('inspection_report.html', data)
