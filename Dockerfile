FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x start_scheduler.sh

# Exposer le port 8000
EXPOSE 8000

# Define environment variables
ENV DEBUG=1
ENV SECRET_KEY=mysecretkey
ENV ALLOWED_HOSTS=['*']
ENV CSV_USERNAME=python-demo
ENV CSV_PASSWORD=claw30_bumps
ENV CSV_CITY_URL=http://rachel.maykinmedia.nl/djangocase/city.csv
ENV CSV_HOTEL_URL=http://rachel.maykinmedia.nl/djangocase/hotel.csv

# Execute the command to start the server
CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

# Execute the command to start the scheduler
CMD bash -c "./start_scheduler.sh"

