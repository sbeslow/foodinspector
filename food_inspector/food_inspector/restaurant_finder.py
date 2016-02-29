from django.db import connection
import re


def find_restaurant_in_db(restaurant_name):
    restaurant_trimmed = trim_name_for_stop_words(restaurant_name)
    print("Trimmed name is %s" % restaurant_trimmed)

    restaurants_from_db = likesounding_restaurants(restaurant_trimmed)

    buckets = {"1": [], "2": [], "3": []}
    for iter_restaurant in restaurants_from_db:
        iter_restaurant_trimmed = trim_name_for_stop_words(iter_restaurant["name"])
        print("Checking db restaurant %s" % restaurant_trimmed + " in " + iter_restaurant_trimmed)
        if restaurant_trimmed in iter_restaurant_trimmed:
            buckets["1"].append(iter_restaurant)
            print(iter_restaurant["name"] + " added to bucket 1")
        else:
            added = False
            for word_in_name in restaurant_trimmed.split(" "):
                if word_in_name in iter_restaurant_trimmed:
                    buckets["2"].append(iter_restaurant)
                    print(iter_restaurant["name"]  + " added to bucket 2")
                    added = True
                    break
            if added is False:
                buckets["3"].append(iter_restaurant)
                print(iter_restaurant["name"]  + " added to bucket 3")


    return buckets["1"] + buckets["2"] + buckets["3"]


def likesounding_restaurants(restaurant_name):
    cursor = connection.cursor()

    print("Searching database for: " + restaurant_name)

    # Forget about PEP8 for the next few lines
    query = "SELECT *, " +\
            "difference(food_inspector_restaurant.chi_name,%s) as diff, " +\
            "levenshtein(food_inspector_restaurant.chi_name, %s) as lev " +\
            "from food_inspector_restaurant where soundex(chi_name) = soundex(%s) " +\
            "order by diff, lev desc;"

    print("Searching database with: %s" % query)

    cursor.execute(query, (restaurant_name,restaurant_name,restaurant_name))
    results = dictfetchall(cursor)
    return results


def trim_name_for_stop_words(restaurant_name):
    stop_words = ['the', 'a', 'and', '&', '\'', ]

    clean_restaurant_name = re.sub('[^a-zA-Z0-9 \n\.]', ' ', restaurant_name.replace('\'', ''))
    clean_restaurant_name = re.sub(' +', ' ', clean_restaurant_name)
    trimmed_name = ''
    for word in clean_restaurant_name.split(" "):
        if word not in stop_words:
            trimmed_name += ' ' + word

    return trimmed_name.strip().upper()

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
