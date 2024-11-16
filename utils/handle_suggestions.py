import random

def generate_suggestions(values, search, city):
    context = {
        'city': city,
        'search': search,
    }

    search_suggestions = []
    cities_suggestions = []

    for obj in values:
        for key, value in obj.items():
            if key == 'employer__city':
                if value.lower() not in cities_suggestions:
                    cities_suggestions.append(value.lower())
            else:
                if value.lower() not in search_suggestions:
                    search_suggestions.append(value.lower())

    random.shuffle(search_suggestions)
    random.shuffle(cities_suggestions)

    context['search_suggestions'] = search_suggestions
    context['cities_suggestions'] = cities_suggestions
   
    if search:
        search_sug = generate_search_suggestions(search_suggestions, search)
        context['search_suggestions'] = search_sug
        context['cities_suggestions'] = []

    if city:
        city_sug = generate_cities_suggestions(cities_suggestions, city)
        context['cities_suggestions'] = city_sug
        context['search_suggestions'] = []

    return context


def generate_search_suggestions(search_suggestions, search):
    searches_list = []
    searches = search.split(' ')

    for chars in search_suggestions:
        if any(word.lower() in chars for word in searches):
            searches_list.append(chars)

    return searches_list or search_suggestions


def generate_cities_suggestions(cities_suggestions, city):
    cities_list = []
    cities = city.split(' ')

    for city_obj in cities_suggestions:
        if any(obj.lower() in city_obj for obj in cities):
            cities_list.append(city_obj)

    return cities_list or cities_suggestions
    