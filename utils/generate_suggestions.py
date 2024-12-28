from random import shuffle as random_shuffle


def generate_suggestions(queryset, search, user_location):
    context = {
        'user_location': user_location,
        'search': search,
    }

    search_suggestions = []
    cities_suggestions = []

    for obj in queryset:
        for key, value in obj.items():
            if key == 'employer__city':
                if value.lower() not in cities_suggestions:
                    cities_suggestions.append(value.lower())
            else:
                if value.lower() not in search_suggestions:
                    search_suggestions.append(value.lower())

    random_shuffle(search_suggestions)
    random_shuffle(cities_suggestions)

    context['search_suggestions'] = search_suggestions
    context['cities_suggestions'] = cities_suggestions

    if search:
        search_sug = generate_search_suggestions(search_suggestions, search)
        context['search_suggestions'] = search_sug
        context['cities_suggestions'] = None

    if user_location:
        city_sug = generate_cities_suggestions(cities_suggestions, user_location)
        context['cities_suggestions'] = city_sug
        context['search_suggestions'] = None

    return context


def generate_search_suggestions(search_suggestions, search):
    search_list = []
    searches = search.split(' ')

    for word in search_suggestions:
        if any(char.lower() in word for char in searches):
            search_list.append(word)
    return search_list or search_suggestions


def generate_cities_suggestions(cities_suggestions, user_location):
    cities_list = []
    cities = user_location.split(' ')

    for city in cities_suggestions:
        if any(c.lower() in city for c in cities):
            cities_list.append(city)
    return cities_list or cities_suggestions
    