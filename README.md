# Maykin Assignement

## Prerequisites

- Python 3.12
- pip 
- Django 5.0.3
- APScheduler 3.10.4
- Virtualenv (recommended)

## Installation

1. Clone the repository

```
git clone https://github.com/sam-bertin/maykin.git
```
2. Create a virtual environment
```
python -m venv venv
```
3. Activate the virtual environment
- On Windows :

```
.\env\Scripts\activate
```

- On macOS et Linux :

```
source env/bin/activate
```
4. Install the requirements

```
pip install -r requirements.txt
```


5. Create a config.ini file in the root directory of the project with the following content:
```
[authentication]
username = <your_username>  # Username for the CSV authentication
password = <your_password> # Password for the CSV authentication

[urls]
city_url = http://<hostname>/city.csv
hotel_url = http://<hostname>/hotel.csv
```

6. Apply the migrations

```
python manage.py migrate
```

7. Create a superuser (optional)

```
python manage.py createsuperuser
```

8. Run the server

```
python manage.py runserver
```

9. Start the scheduler (optional)
- On Windows :

```
.\start_scheduler.bat      
```

- On macOS et Linux :

```
.\start_scheduler.sh
```
