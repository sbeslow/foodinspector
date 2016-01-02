import requests
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from food_inspector.restaurant_finder import find_restaurant_in_db


def home(request):
    return render_to_response('home.html')


@csrf_exempt
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


def retrieve_inspection_report(restaurant):

    payload = {'inspection_id': '1592111'}
    r = requests.get("https://data.cityofchicago.org/resource/4ijn-s7e5.json",
                     params=payload)

    if r.status_code != 200:
        print("STATUS CODE: " + r.status)

    print(r.text)
    return render_to_response('home.html')
