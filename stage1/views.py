from django.http import JsonResponse
from django.contrib.gis.geoip2 import GeoIP2
import requests
from decouple import config

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = get_client_ip(request)
    location = get_location(client_ip)
    temperature = get_weather(location)
    response_data = {
        "client_ip" : client_ip,
        "location" : location,
        "greeting" : f"Hello!, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    }
    return JsonResponse(response_data)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWADED_FOR')
    print(request.META)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(request.META)
    return ip

def get_location(ip):
    place  = GeoIP2()
    try:
        city = place.city(ip)['city']
        return city
    except Exception:
        city = 'Unknown Location'
        return city

def get_weather(city):

    weather_api_key = config('WEATHERSTACK_API_KEY')
    print(weather_api_key)
    weather_api_url = requests.get(f'http://api.weatherbit.io/v2.0/current?city={city}&key={weather_api_key}')
    if weather_api_url.status_code == 200:
        weather_response = weather_api_url.json()
        return weather_response['data'][0]['temp']
    else:
        return "N/A"
    


