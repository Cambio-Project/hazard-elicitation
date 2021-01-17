# Hazard Elicitation

## Setup

## Run

### Local

For debugging details set `DEBUG` in `source/hazard_elicitation/settings.py` to `True`.

> python source/manage.py runserver

The webserver will run at localhost on port 8000 by default.
[http://localhost:8000/ui](http://localhost:8000/ui)

### Production 

Make sure to set `DEBUG` in `source/hazard_elicitation/settings.py` to `False`.

> cd source
> python manage.py collectstatic --noinput
> daphne -b 0.0.0.0 -p 8000 hazard_elicitation.asgi:application

This runs a production ready asynchronous webserver at localhost on port 8000.

### Docker

Build the container yourself:
> docker build -t <container_name> .

Or retrieve the image from [DockerHub](https://hub.docker.com/repository/docker/styinx/hazard_elicitation_slim):

Then run the container:
> docker run -p 8000:8080 <container_name>

This runs the container at localhost on port 8000.
