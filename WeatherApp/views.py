from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import City
from .forms import CityForm


# Create your views here.


def CityWeatherView(request):
    url = "http://api.openweathermap.org/data/2.5/" \
          "weather?q={}&units=metric&units=imperial&appid=2028a73ec8dd9e755c59a0a7c541ebea"

    errmsg = ''
    msgclass = ''
    msg = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name'].capitalize()
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    errmsg = 'The city is not in the database!'
            else:
                errmsg = 'OOOPS!  Already added!!'
        if errmsg:
            msg = errmsg
            msgclass = 'is-danger'
        else:
            msg = 'Successfully added!'
            msgclass = 'is-success'

    form = CityForm()

    weather = []
    city = City.objects.all()
    for c in city:
        r = requests.get(url.format(c)).json()
        city_weather = {
            'city': c,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
            'country' : r['sys']['country'],
            'feels' : r['main']['feels_like']
        }
        weather.append(city_weather)
    context = {
        'weather': weather,
        'form': form,
        'msg': msg,
        'msgclass': msgclass,
    }

    return render(request, 'weather.html', context)


def city_delete(request, city_name):
    city = get_object_or_404(City, name=city_name)
    city.delete()
    return redirect('WeatherApp:city_weather')
