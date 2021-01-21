FROM python:3.8-slim

WORKDIR .
COPY requirements.txt .
COPY source/ .

RUN apt-get update && apt-get install -y --no-install-recommends gcc python-dev
RUN pip install -r requirements.txt
RUN apt-get purge -y --auto-remove gcc python-dev
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000
ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "hazard_elicitation.asgi:application"]