FROM python:latest
LABEL authors="Daniel Mandelblat" email="danielmande@gmail.com"
ADD app /app
EXPOSE 80
RUN  pip install -r /app/requirements.txt
ENTRYPOINT ["python", "/app/manage.py", "runserver", "0.0.0.0:80"]