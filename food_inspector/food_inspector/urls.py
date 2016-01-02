from django.conf.urls import url
from food_inspector.views import *


urlpatterns = [
    url(r'^$', home),
    url(r'^locate', locate_restaurant),
    url(r'^inspect/(?P<restaurant_id>\d+)$', retrieve_inspection_report),
]
