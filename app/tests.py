import requests
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from .models import City, Hotel
from app.import_data import import_city_and_hotel_data, get_config
from .views import hotel_list, hotels_by_city


class TestImportData(TestCase):
    def setUp(self):
        City.objects.all().delete()
        Hotel.objects.all().delete()

    # Test the import_city_and_hotel_data function
    # Kind of useless cause the data volume migth change overtime
    def test_import_data(self):
        import_city_and_hotel_data()

        cities = City.objects.all()
        hotels = Hotel.objects.all()

        self.assertEqual(len(cities), 6)
        self.assertEqual(len(hotels), 196)

        city = City.objects.get(code='AMS')
        self.assertEqual(city.name, 'Amsterdam')

        hotel = Hotel.objects.get(code='AMS01')
        self.assertEqual(hotel.name, 'Ibis Amsterdam Airport')
        self.assertEqual(hotel.city.code, 'AMS')


class TestHotelListView(TestCase):
    def setUp(self):
        City.objects.create(code='C1', name='City 1')
        Hotel.objects.create(code='H1', name='Hotel 1', city_id=1)
        Hotel.objects.create(code='H2', name='Hotel 2', city_id=1)

    def test_hotel_list(self):
        response = self.client.get(reverse('hotel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel_list.html')
        self.assertContains(response, 'Hotel 1')
        self.assertContains(response, 'Hotel 2')


class TestHotelsByCityView(TestCase):
    def setUp(self):
        City.objects.create(code='C1', name='City 1')
        City.objects.create(code='C2', name='City 2')
        Hotel.objects.create(code='H1', name='Hotel 1', city_id=1)
        Hotel.objects.create(code='H2', name='Hotel 2', city_id=1)
        Hotel.objects.create(code='H3', name='Hotel 3', city_id=2)

    def test_hotels_by_city_with_valid_city_id(self):
        request = RequestFactory().get(reverse('hotels_by_city') + '?city=1')
        response = hotels_by_city(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [
            {'id': 1, 'name': 'Hotel 1', 'city': {'id': 1, 'name': 'City 1'}, 'code': 'H1'},
            {'id': 2, 'name': 'Hotel 2', 'city': {'id': 1, 'name': 'City 1'}, 'code': 'H2'}
        ])

    def test_hotels_by_city_with_invalid_city_id(self):
        request = RequestFactory().get(reverse('hotels_by_city') + '?city=3')
        response = hotels_by_city(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    def test_hotels_by_city_without_city_id(self):
        request = RequestFactory().get(reverse('hotels_by_city'))
        response = hotels_by_city(request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [
            {'id': 1, 'name': 'Hotel 1', 'city': {'id': 1, 'name': 'City 1'}, 'code': 'H1'},
            {'id': 2, 'name': 'Hotel 2', 'city': {'id': 1, 'name': 'City 1'}, 'code': 'H2'},
            {'id': 3, 'name': 'Hotel 3', 'city': {'id': 2, 'name': 'City 2'}, 'code': 'H3'}
        ])
