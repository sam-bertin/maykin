from django.contrib.auth.models import User
from django.test import TestCase
from app.models import City, Hotel, Manager


class TestCityModel(TestCase):
    def setUp(self):
        self.city = City.objects.create(code='PAR', name='Paris')

    def test_string_representation(self):
        self.assertEqual(str(self.city), 'Paris')


class TestHotelModel(TestCase):
    def setUp(self):
        self.city = City.objects.create(code='PAR', name='Paris')
        self.hotel = Hotel.objects.create(city=self.city, code='H1', name='Hotel 1')

    def test_string_representation(self):
        self.assertEqual(str(self.hotel), 'Hotel 1')


class TestManagerModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.city = City.objects.create(code='PAR', name='Paris')
        self.manager = Manager.objects.create(user=self.user, city=self.city)

    def test_string_representation(self):
        self.assertEqual(str(self.manager), 'testuser')

