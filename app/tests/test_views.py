from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from app.models import Manager, Hotel, City
from app.views import hotels_by_city


class TestHotelListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    # Here I'm tinkering by mocking up the import_city_and_hotel_data function as a function that does nothing to
    # avoid having to import the data for each test and ESPECIALLY because you're not supposed to import the data via
    # this view but rather via a cron job which calls the import_city_and_hotel_data function
    @patch('app.views.import_city_and_hotel_data')
    def test_hotel_list(self, mock_import_data):
        mock_import_data.return_value = None

        response = self.client.get('/hotels/')

        self.assertEqual(response.status_code, 200)


class TestHotelsByCityView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_hotels_by_city(self):
        request = self.factory.get(reverse('hotels_by_city'))
        request.GET = {'city': '1'}
        response = hotels_by_city(request)
        self.assertEqual(response.status_code, 200)


class TestManagerView(TestCase):
    def setUp(self):
        # Create a user for the tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create data for the tests
        self.city = City.objects.create(name='Test City')
        self.manager = Manager.objects.create(user=self.user, city=self.city)
        self.hotel1 = Hotel.objects.create(name='Hotel 1', city=self.city)
        self.hotel2 = Hotel.objects.create(name='Hotel 2', city=self.city)

    def test_manager_view(self):
        # Access the ManagerView view as the logged-in user
        response = self.client.get(reverse('manager_view'))

        # Assert that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains all hotels in the city of the manager
        self.assertIn('hotels', response.context)
        self.assertEqual(len(response.context['hotels']), 2)
        self.assertIn(self.hotel1, response.context['hotels'])
        self.assertIn(self.hotel2, response.context['hotels'])

        # Assert that the context contains the manager
        self.assertIn('manager', response.context)
        self.assertEqual(response.context['manager'], self.manager)

    @patch('app.views.import_city_and_hotel_data')
    def test_manager_view_no_manager(self, mock_import):
        # Create a user without a manager profile
        user_no_manager = User.objects.create_user(username='testuser2', password='testpassword')
        self.client.logout()
        self.client.login(username='testuser2', password='testpassword')

        # Access the ManagerView view as the logged-in user
        response = self.client.get(reverse('manager_view'))

        # Assert redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_manager_view_superuser(self):
        # Create a superuser for the tests
        superuser = User.objects.create_superuser(username='testsuperuser', password='testpassword')
        self.client.logout()
        self.client.login(username='testsuperuser', password='testpassword')

        # Create additional data for the tests
        city2 = City.objects.create(name='Test City 2')
        hotel3 = Hotel.objects.create(name='Hotel 3', city=city2)

        # Access the ManagerView view as the logged-in superuser
        response = self.client.get(reverse('manager_view'))

        # Assert that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the context contains all hotels in the database
        self.assertIn('hotels', response.context)
        self.assertEqual(len(response.context['hotels']), 3)
        self.assertIn(self.hotel1, response.context['hotels'])
        self.assertIn(self.hotel2, response.context['hotels'])
        self.assertIn(hotel3, response.context['hotels'])

        # Assert that the context contains the is_superuser variable
        self.assertIn('is_superuser', response.context)
        self.assertTrue(response.context['is_superuser'])


class TestHotelCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')
        self.city = City.objects.create(name='Test City')
        self.manager = Manager.objects.create(user=self.user, city=self.city)

    def test_hotel_create_view(self):
        response = self.client.get(reverse('hotel_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel_form.html')

    def test_hotel_create_valid_data(self):
        data = {'name': 'Test Hotel', 'code': 'TH123', 'city': self.city.id}
        response = self.client.post(reverse('hotel_create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Hotel.objects.count(), 1)
        hotel = Hotel.objects.get(name='Test Hotel')
        self.assertEqual(hotel.code, 'TH123')
        self.assertEqual(hotel.city, self.city)

    def test_hotel_create_invalid_data(self):
        data = {'name': '', 'code': '', 'city': self.city.id}
        response = self.client.post(reverse('hotel_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel_form.html')
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Hotel.objects.count(), 0)





