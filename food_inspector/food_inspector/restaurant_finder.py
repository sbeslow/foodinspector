from django.db import connection


def find_restaurant_in_db(restaurant_name):
    cursor = connection.cursor()
    print("RESTAURANT IS: " + restaurant_name)

    query = "SELECT *"
    query += ",difference(food_inspector_restaurant.name,'%s') as diff, " % restaurant_name
    query += "levenshtein(food_inspector_restaurant.name, '%s') as lev " % restaurant_name
    query += "from food_inspector_restaurant where soundex(name) = soundex('%s') " % restaurant_name
    query += "order by diff, lev desc;"

    print(query)

    cursor.execute(query)
    results = dictfetchall(cursor)
    return results


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
