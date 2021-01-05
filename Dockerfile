FROM python:3.8-slim

WORKDIR .
COPY source/ .
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8080", "hazard_elicitation.asgi"]