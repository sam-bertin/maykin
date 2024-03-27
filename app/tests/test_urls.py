from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TestURLs(TestCase):
    @patch('app.views.import_city_and_hotel_data')
    def test_hotel_list_url(self, mock_import):
        url = reverse('hotel_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_hotels_by_city_url(self):
        url = reverse('hotels_by_city')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_hotel_create_url(self):
        url = reverse('hotel_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirects to login, assuming login is required

    def test_hotel_update_url(self):
        hotel_pk = 1
        url = reverse('hotel_update', args=[hotel_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirects to login, assuming login is required

    def test_hotel_delete_url(self):
        hotel_pk = 1
        url = reverse('hotel_delete', args=[hotel_pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirects to login, assuming login is required

    def test_manager_view_url(self):
        url = reverse('manager_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirects to login, assuming login is required

    def test_login_url(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405) # Method not allowed because user is not logged in
