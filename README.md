# Hazard Elicitation

![Tests](https://github.com/Cambio-Project/hazard-elicitation/workflows/Tests/badge.svg)

[Live](https://hazardelicitation.eu-gb.mybluemix.net/ui/)

## Description

This project consists of 3 different applications:
- Architecture Extraction:
  - Can import and create a model from:
    - traces from Jaeger and Zipkin
    - a MiSim architecture
  - Can create a generic architecture description of services and operation as a graph
  - Can validate models and architecture
  - Can perform an automated hazard analysis
  - Can export a visualization of the architecture and the analysis
- Conversational Interface:
  - Provides a chatbot interface
  - Guides a user through the elicitation of resilience scenarios
- Hazard Elicitation:
  - Provides an import of the architecture visualization and analysis
  - Provides a resilience scenario template and export

## Setup

Have a look [here](https://github.com/Cambio-Project/hazard-elicitation/blob/master/docs/wiki/setup.md) 
on how to set up Django, DialogFlow, and Cloud Foundry.

## Run

### Local

For debugging details set `DEBUG` in `source/hazard_elicitation/settings.py` to `True`.

`python source/manage.py runserver`

The webserver will run at localhost on port 8000 by default.
[http://localhost:8000/ui](http://localhost:8000/ui)

### Production 

Make sure to set `DEBUG` in `source/hazard_elicitation/settings.py` to `False`.

```
cd source
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 8000 hazard_elicitation.asgi:application
```

This runs a production ready asynchronous webserver at localhost on port 8000.

### Docker

Build the container yourself:
` docker build -t <container_name> . `

Or retrieve the image from [DockerHub](https://hub.docker.com/repository/docker/styinx/hazard_elicitation_slim):

Then run the container:
`docker run -p 8000:8000 <container_name>`

This runs the container at localhost on port 8000.
