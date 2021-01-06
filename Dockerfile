FROM python:3.8-slim

WORKDIR .
COPY requirements.txt .
COPY keys.json .
COPY source/ .

RUN apt-get update && apt-get install -y --no-install-recommends gcc python-dev
RUN pip install -r requirements.txt
RUN apt-get purge -y --auto-remove gcc python-dev
RUN python manage.py migrate
RUN python manage.py collectstatic

EXPOSE 8080
ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8080", "hazard_elicitation.asgi:application"]