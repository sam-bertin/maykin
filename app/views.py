from django.http import JsonResponse
from django.shortcuts import render
from .models import City, Hotel
from .import_data import import_city_and_hotel_data


# Create your views here.
def hotel_list(request):
    # TODO : Replace import with cron job
    import_city_and_hotel_data()
    cities = City.objects.all()
    hotels = Hotel.objects.all()
    return render(request, 'hotel_list.html', {'cities': cities, 'hotels': hotels})


def hotels_by_city(request):
    city_id = request.GET.get('city')
    if city_id:
        hotels = Hotel.objects.filter(city_id=city_id)
    else:
        hotels = Hotel.objects.all()
    data = [{'id': hotel.id, 'name': hotel.name, 'city': {'id': hotel.city_id, 'name': hotel.city.name},
             'code': hotel.code} for hotel in hotels]
    return JsonResponse(data, safe=False)
