from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import requests


def home(request):
    return render_to_response('home.html')


@csrf_exempt
def searchName(request):
    name_input = request.POST.get("restaurantName")
    restaurant_name = find_restaurant(name_input)

    payload = {'inspection_id': '1592111'}
    r = requests.get("https://data.cityofchicago.org/resource/4ijn-s7e5.json",
                     params=payload)

    if r.status_code != 200:
        print("STATUS CODE: " + r.status)

    print(r.text)
    return render_to_response('home.html')
