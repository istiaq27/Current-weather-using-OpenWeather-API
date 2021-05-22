from django.urls import path
from .views import CityWeatherView, city_delete

app_name = 'WeatherApp'

urlpatterns = [
    path('', CityWeatherView, name='city_weather'),
    path('remove/<city_name>/', city_delete, name='city_remove'),
]
