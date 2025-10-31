import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    appid = '7476f1fb3ad25e10688a3cb9a52cfac5'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'

    # Обработка формы
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            # Проверяем, есть ли город уже в базе
            if not City.objects.filter(name__iexact=new_city).exists():
                form.save()
        return redirect('index')

    form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name, appid)).json()

        if res.get('cod') != 200:
            city_info = {
                'city': city.name,
                'temp': 'не найдено',
                'icon': ''
            }
        else:
            city_info = {
                'city': city.name,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon']
            }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)
