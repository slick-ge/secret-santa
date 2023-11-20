FROM python:3.8

WORKDIR /app

COPY ./API/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./API/api.py api.py
CMD ["python", "api.py"]

