FROM python:3.8-slim

WORKDIR .
COPY requirements.txt .
COPY source/ .

RUN apt-get update && apt-get install -y --no-install-recommends gcc python-dev
RUN pip install -r ./software_architecture_extraction/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get purge -y --auto-remove gcc python-dev

EXPOSE 8000
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate", "--run-syncdb"]
CMD ["python", "manage.py", "collectstatic", "--noinput"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "hazard_elicitation.asgi:application"]