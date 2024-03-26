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
ENV CSV_USERNAME=<username>
ENV CSV_PASSWORD=<password>
ENV CSV_CITY_URL=<city_url>
ENV CSV_HOTEL_URL=<hotel_url>

# Execute the command to start the server
CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"



