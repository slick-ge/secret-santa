FROM python:3.8

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./api.py api.py
COPY ./secret_santas_functions.py secret_santas_functions.py
CMD ["python", "api.py"]

