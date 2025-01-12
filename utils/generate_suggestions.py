
def generate_suggestions(queryset, search, user_location):
    context = {
        'search_suggestions': [],
        'cities_suggestions': [],
        'user_location': user_location,
        'search': search,
    }

    if not queryset:
        return context
    else:
        for obj in queryset:
            city = None
            for key, value in obj.items():
                if key == 'employer__city':
                    city = value
                elif key == 'employer__state_or_province':
                    city = f'{city}, {value}'
                    if city.title() not in context['cities_suggestions']:
                        context['cities_suggestions'].append(city.title())
                else:
                    if value.capitalize() not in context['search_suggestions']:
                        context['search_suggestions'].append(value.capitalize())
   
    # Perform one more filter
    # Filter down to closest match
    if search:
        search_sug = generate_search_suggestions(context['search_suggestions'], search)
        context['search_suggestions'] = search_sug

    if user_location:
        city_sug = generate_cities_suggestions(context['cities_suggestions'], user_location)
        context['cities_suggestions'] = city_sug

    return context


def generate_search_suggestions(search_suggestions, search):
    search_list = []
    searches = search.split(' ')

    for suggestion in search_suggestions:
        for searched in searches:

            if searched.lower() == suggestion.lower() or \
                searched.lower() in suggestion.lower():

                if suggestion not in search_list:
                    search_list.append(suggestion)
    return search_list

def generate_cities_suggestions(cities_suggestions, user_location):
    cities_list = []
    cities = user_location.split(' ')

    for city in cities_suggestions:
        for user_city in cities:

            if user_city.lower() in city.lower() or \
                user_city.lower() == city.lower():

                if city not in cities_list:
                    cities_list.append(city)
    return cities_list
    