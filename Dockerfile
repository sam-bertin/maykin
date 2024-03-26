FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Define environment variables
ENV DEBUG=1
ENV SECRET_KEY=mysecretkey
ENV ALLOWED_HOSTS=['*']
ENV CSV_USERNAME=$CSV_USERNAME
ENV CSV_PASSWORD=$CSV_PASSWORD
ENV CSV_CITY_URL=$CSV_CITY_URL
ENV CSV_HOTEL_URL=$CSV_HOTEL_URL

RUN python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD

CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"



