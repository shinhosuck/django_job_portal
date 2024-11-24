from geoip2 import database



def get_user_ip(request):
    remote_addr = request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    
    exclude = ['127.0.0.1', '35.173.69.207', '192.168.1.155']
    default = '175.176.7.162'

    ip = ''

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = remote_addr

    if ip in exclude:
        ip = default

    return get_user_location(request, ip)
    

def get_user_location(request, ip):
    host = request.get_host()
    path = None 

    if host == 'djjobportal.pythonanywhere.com':
        path = '/home/djjobportal/django_job_portal/geolite2-city/GeoLite2-City.mmdb'
    else:
        path = 'geolite2-city/GeoLite2-City.mmdb'

    reader = database.Reader(path)
    response = reader.city(ip)

    location = {
        'user': request.user.username,
        'country': response.country.iso_code,
        'city': response.city.name,
        'state': response.subdivisions.most_specific.iso_code
    }

    return location