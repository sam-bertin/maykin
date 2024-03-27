import csv
import os
import requests
from .models import City, Hotel
from apscheduler.schedulers.background import BackgroundScheduler


def get_auth_info():
    auth_info = {
        'username': os.environ.get('CSV_USERNAME'),
        'password': os.environ.get('CSV_PASSWORD')
    }
    return auth_info


def import_city_and_hotel_data():
    # URL infos
    city_url = os.environ.get('CSV_CITY_URL')
    hotel_url = os.environ.get('CSV_HOTEL_URL')

    # Gather the authentication info
    auth_info = get_auth_info()
    auth = (auth_info['username'], auth_info['password'])

    # Add authentication to the request
    city_response = requests.get(city_url, auth=auth)
    hotel_response = requests.get(hotel_url, auth=auth)

    #  Handle the error if the response is not successful
    if city_response.status_code != 200:
        raise requests.HTTPError(f"Failed to retrieve data from {city_url}")
    if hotel_response.status_code != 200:
        raise requests.HTTPError(f"Failed to retrieve data from {hotel_url}")

    # Parse the CSV data
    city_reader = csv.reader(city_response.text.splitlines(), delimiter=';')
    hotel_reader = csv.reader(hotel_response.text.splitlines(), delimiter=';')

    # Import the data into Django database
    for row in city_reader:
        _, created = City.objects.get_or_create(
            code=row[0],
            defaults={'name': row[1]}
        )

    for row in hotel_reader:
        city = City.objects.get(code=row[0])
        Hotel.objects.get_or_create(
            city=city,
            code=row[1],
            name=row[2]
        )


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(import_city_and_hotel_data, 'cron', hour=0, minute=0)
    scheduler.start()


if __name__ == '__main__':
    start_scheduler()
