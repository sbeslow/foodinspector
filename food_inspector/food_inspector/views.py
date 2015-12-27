from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render_to_response('home.html')


@csrf_exempt
def searchName(request):
    restaurant_name = request.POST.get("restaurantName")
    print("Restaurant name: " + restaurant_name)
 
    return render_to_response('home.html')
