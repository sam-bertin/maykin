FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN python3 -m venv venv

RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/start_scheduler.sh

EXPOSE 8000

CMD bash -c "source venv/bin/activate && python manage.py migrate && python manage.py createsuperuser --noinput && python manage.py runserver 0.0.0.0:8000 && ./start_scheduler.sh"

