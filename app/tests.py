import requests
from django.test import TestCase
from .models import City, Hotel
from app.import_data import import_city_and_hotel_data, get_config


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

